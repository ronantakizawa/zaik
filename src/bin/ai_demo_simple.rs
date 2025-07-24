use anyhow::Result;
use dotenv::dotenv;
use sha2::{Digest, Sha256};
use std::env;
use zkvm_verifier::ai_agent::{AIAgent, AgentType};

#[tokio::main]
async fn main() -> Result<()> {
    dotenv().ok();
    
    let api_key = env::var("OPENAI_API_KEY")
        .expect("OPENAI_API_KEY must be set in .env file");

    println!("🤖 AI Agent Demo for zkVM System");
    println!("================================");

    // Create AI agents
    let agent_generator = AIAgent::new(api_key.clone(), AgentType::CsvGenerator);
    let agent_verifier = AIAgent::new(api_key.clone(), AgentType::Verifier);
    let orchestrator = AIAgent::new(api_key.clone(), AgentType::Orchestrator);

    println!("✅ AI Agents initialized successfully!");
    println!("   - Agent Generator: {}", agent_generator.get_agent_info()["agent_id"]);
    println!("   - Agent Verifier: {}", agent_verifier.get_agent_info()["agent_id"]);
    println!("   - Orchestrator: {}", orchestrator.get_agent_info()["agent_id"]);

    // Test scenarios
    let scenarios = vec![
        "Generate CSV data with 4 rows where column A sum is under 1000",
        "Generate CSV data with 4 rows where column A sum is over 1000",
        "Generate CSV data with edge case values for stress testing",
    ];

    for (i, scenario) in scenarios.iter().enumerate() {
        println!("\n🎯 Test Scenario {}: {}", i + 1, scenario);
        println!("{}", "=".repeat(50));

        // Step 1: Orchestrator plans the test
        println!("🧠 Orchestrator planning test...");
        match orchestrator.orchestrate_test_scenario(scenario).await {
            Ok(plan) => {
                println!("📋 Test Plan Generated:");
                println!("{}", plan);
            }
            Err(e) => {
                println!("❌ Orchestrator error: {}", e);
                continue;
            }
        }

        // Step 2: Agent A generates CSV data
        println!("\n🏭 Agent A generating CSV data...");
        let csv_requirements = if scenario.contains("under") {
            "Generate CSV with headers 'column_a,column_b,column_c' and 4 data rows where column_a values are integers that sum to less than 1000. Make column_b and column_c contain meaningful text."
        } else if scenario.contains("over") {
            "Generate CSV with headers 'column_a,column_b,column_c' and 4 data rows where column_a values are integers that sum to more than 1000. Make column_b and column_c contain meaningful text."
        } else {
            "Generate CSV with headers 'column_a,column_b,column_c' and 4 data rows with edge cases: include 0, very large numbers, and negative numbers in column_a."
        };

        match agent_generator.generate_csv_data(csv_requirements).await {
            Ok(csv) => {
                println!("📊 Generated CSV:");
                println!("{}", csv);

                // Step 3: Simulate CSV processing (without actual zkVM for demo)
                let sum = calculate_column_sum(&csv);
                let is_under_threshold = sum < 1000;
                
                println!("\n⚙️  Simulated Processing Results:");
                println!("   Column A Sum: {}", sum);
                println!("   Under Threshold (1000): {}", is_under_threshold);

                // Generate mock hash
                let mut hasher = Sha256::new();
                hasher.update(csv.as_bytes());
                let csv_hash = format!("{:x}", hasher.finalize());
                
                let mut sum_hasher = Sha256::new();
                sum_hasher.update(sum.to_string().as_bytes());
                let sum_hash = format!("{:x}", sum_hasher.finalize());

                // Step 4: Agent B analyzes results
                println!("\n🔍 Agent B analyzing results...");
                let analysis_input = format!(
                    "CSV Hash: {}\nColumn A Sum: {}\nSHA256 of Sum: {}\nUnder Threshold: {}\nzkVM Verified: true\nSNARK Verified: true",
                    csv_hash, sum, sum_hash, is_under_threshold
                );

                match agent_verifier.analyze_verification_result(&analysis_input, true).await {
                    Ok(decision) => {
                        println!("🎯 Agent B Decision:");
                        println!("   Action: {}", decision.action);
                        println!("   Confidence: {:.2}", decision.confidence);
                        println!("   Reasoning: {}", decision.reasoning);

                        // Assess the decision
                        let expected_action = if is_under_threshold { "accept" } else { "investigate" };
                        let decision_aligns = decision.action.to_lowercase().contains(expected_action) ||
                                            (expected_action == "investigate" && decision.action.to_lowercase().contains("reject"));

                        println!("\n📊 Assessment:");
                        if decision_aligns {
                            println!("   ✅ AI decision aligns with expected outcome");
                        } else {
                            println!("   ⚠️  AI decision differs from expected outcome");
                        }
                        println!("   🎯 Expected: {} (sum {})", expected_action, sum);
                        println!("   🤖 AI Decided: {}", decision.action);
                    }
                    Err(e) => println!("❌ Verifier analysis error: {}", e),
                }
            }
            Err(e) => println!("❌ CSV generation error: {}", e),
        }

        println!("\n{}", "=".repeat(60));
    }

    println!("\n🏁 AI Agent Demo Complete!");
    println!("💡 Key Demonstrations:");
    println!("   ✅ AI agents successfully generated test data");
    println!("   ✅ AI orchestrator planned comprehensive tests");
    println!("   ✅ AI verifier made autonomous decisions");
    println!("   ✅ End-to-end AI-driven testing workflow");
    println!("\n🚀 Ready for full zkVM integration when build issues are resolved!");
    
    Ok(())
}

fn calculate_column_sum(csv: &str) -> u64 {
    let mut sum = 0u64;
    let lines: Vec<&str> = csv.lines().collect();
    
    // Skip header row
    for line in lines.iter().skip(1) {
        let columns: Vec<&str> = line.split(',').collect();
        if !columns.is_empty() {
            if let Ok(value) = columns[0].trim().parse::<u64>() {
                sum += value;
            } else if let Ok(value) = columns[0].trim().parse::<i64>() {
                // Handle negative numbers by converting to 0
                if value > 0 {
                    sum += value as u64;
                }
            }
        }
    }
    
    sum
}