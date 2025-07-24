use anyhow::Result;
use ark_std::test_rng;
use dotenv::dotenv;
use risc0_zkvm::{default_prover, ExecutorEnv, Receipt};
use sha2::{Digest, Sha256};
use std::{env, fs};
use zkvm_verifier::{
    ai_agent::{AIAgent, AgentType},
    snark_prover::SnarkProver,
    CsvProcessingInput, CsvProcessingOutput, THRESHOLD,
};

include!(concat!(env!("OUT_DIR"), "/methods.rs"));

#[tokio::main]
async fn main() -> Result<()> {
    dotenv().ok();
    
    let api_key = env::var("OPENAI_API_KEY")
        .expect("OPENAI_API_KEY must be set in .env file");

    println!("🤖 AI Agent Testing System for zkVM Verifier");
    println!("==============================================");

    // Create AI agents
    let agent_generator = AIAgent::new(api_key.clone(), AgentType::CsvGenerator);
    let agent_verifier = AIAgent::new(api_key.clone(), AgentType::Verifier);
    let orchestrator = AIAgent::new(api_key.clone(), AgentType::Orchestrator);

    // Test scenarios
    let scenarios = vec![
        "Generate CSV data with sum under threshold (should be accepted)",
        "Generate CSV data with sum over threshold (should trigger review)",
        "Generate CSV data with edge case values (test robustness)",
    ];

    for (i, scenario) in scenarios.iter().enumerate() {
        println!("\n🎯 Test Scenario {}: {}", i + 1, scenario);
        println!("------------------------------------------------");

        // Step 1: Orchestrator plans the test
        println!("🧠 Orchestrator planning test...");
        let test_plan = orchestrator.orchestrate_test_scenario(scenario).await?;
        println!("📋 Test Plan: {}", test_plan);

        // Step 2: Agent A generates CSV data
        println!("\n🏭 Agent A generating CSV data...");
        let csv_requirements = if scenario.contains("under threshold") {
            "Generate CSV with 4 rows, column_a values that sum to less than 1000"
        } else if scenario.contains("over threshold") {
            "Generate CSV with 4 rows, column_a values that sum to more than 1000"
        } else {
            "Generate CSV with 4 rows, column_a with edge case values (zeros, very large numbers)"
        };

        let generated_csv = agent_generator.generate_csv_data(csv_requirements).await?;
        println!("📊 Generated CSV:");
        println!("{}", generated_csv);

        // Step 3: Process through zkVM system
        println!("\n⚙️  Processing through zkVM system...");
        match process_csv_with_zkvm(&generated_csv).await {
            Ok((receipt, output)) => {
                println!("✅ zkVM processing completed successfully");
                println!("   Column A Sum: {}", output.column_a_sum);
                println!("   Under Threshold: {}", output.is_under_threshold);

                // Step 4: Generate SNARK proof
                println!("\n🔐 Generating SNARK proof...");
                let snark_result = generate_snark_proof(&output).await;
                let snark_verified = snark_result.is_ok();
                
                if snark_verified {
                    println!("✅ SNARK proof generated and verified");
                } else {
                    println!("❌ SNARK proof failed: {:?}", snark_result.err());
                }

                // Step 5: Agent B analyzes results
                println!("\n🔍 Agent B analyzing verification results...");
                let analysis_input = format!(
                    "CSV Hash: {}\nColumn A Sum: {}\nSHA256 of Sum: {}\nUnder Threshold: {}\nSNARK Verified: {}",
                    output.csv_hash, output.column_a_sum, output.sha256_sum, 
                    output.is_under_threshold, snark_verified
                );

                let decision = agent_verifier.analyze_verification_result(&analysis_input, snark_verified).await?;
                
                println!("🎯 Agent B Decision:");
                println!("   Action: {}", decision.action);
                println!("   Confidence: {:.2}", decision.confidence);
                println!("   Reasoning: {}", decision.reasoning);

                // Step 6: Final assessment
                assess_test_result(&decision, &output, scenario);
            }
            Err(e) => {
                println!("❌ zkVM processing failed: {}", e);
                
                // Let Agent B analyze the failure
                let failure_analysis = agent_verifier
                    .analyze_verification_result(&format!("zkVM processing failed: {}", e), false)
                    .await?;
                
                println!("🔍 Agent B Failure Analysis:");
                println!("   Action: {}", failure_analysis.action);
                println!("   Reasoning: {}", failure_analysis.reasoning);
            }
        }

        println!("\n" + "=".repeat(60).as_str());
    }

    println!("\n🏁 AI Agent Testing Complete!");
    Ok(())
}

async fn process_csv_with_zkvm(csv_data: &str) -> Result<(Receipt, CsvProcessingOutput)> {
    // Compute CSV hash
    let mut hasher = Sha256::new();
    hasher.update(csv_data.as_bytes());
    let csv_hash = format!("{:x}", hasher.finalize());

    let input = CsvProcessingInput {
        csv_hash: csv_hash.clone(),
        csv_data: csv_data.to_string(),
    };

    // Create executor environment
    let env = ExecutorEnv::builder()
        .write(&input)?
        .build()?;

    // Generate proof
    let prover = default_prover();
    let receipt = prover.prove(env, CSV_PROCESSOR_ELF)?;

    // Extract output
    let output: CsvProcessingOutput = receipt.journal.decode()?;

    // Verify the receipt
    receipt.verify(CSV_PROCESSOR_ID)?;

    Ok((receipt, output))
}

async fn generate_snark_proof(output: &CsvProcessingOutput) -> Result<()> {
    let mut rng = test_rng();
    let snark_prover = SnarkProver::setup(&mut rng)?;
    
    let sum_value: u64 = output.column_a_sum.parse()?;
    
    let snark_proof = snark_prover.prove(
        &mut rng,
        sum_value,
        THRESHOLD,
        output.is_under_threshold,
    )?;
    
    let verified = snark_prover.verify(
        &snark_proof,
        THRESHOLD,
        output.is_under_threshold,
    )?;
    
    if verified {
        Ok(())
    } else {
        Err(anyhow::anyhow!("SNARK verification failed"))
    }
}

fn assess_test_result(decision: &zkvm_verifier::ai_agent::AgentDecision, output: &CsvProcessingOutput, scenario: &str) {
    println!("\n📊 Test Assessment:");
    
    let sum_value: u64 = output.column_a_sum.parse().unwrap_or(0);
    let expected_under_threshold = sum_value < THRESHOLD;
    
    // Check if AI decision aligns with expected outcome
    let decision_correct = match scenario {
        s if s.contains("under threshold") => {
            expected_under_threshold && decision.action == "accept"
        }
        s if s.contains("over threshold") => {
            !expected_under_threshold && (decision.action == "investigate" || decision.action == "reject")
        }
        _ => true, // Edge case scenarios are more flexible
    };
    
    if decision_correct {
        println!("   ✅ AI Agent decision aligns with expected outcome");
    } else {
        println!("   ⚠️  AI Agent decision differs from expected outcome");
    }
    
    println!("   📈 Sum: {} (Threshold: {})", sum_value, THRESHOLD);
    println!("   🎯 Expected Under Threshold: {}", expected_under_threshold);
    println!("   🤖 AI Confidence: {:.2}", decision.confidence);
}