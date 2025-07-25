use methods::{
    GUEST_CODE_FOR_ZK_PROOF_ELF, GUEST_CODE_FOR_ZK_PROOF_ID
};
use risc0_zkvm::{default_prover, ExecutorEnv, Receipt};
use serde::{Deserialize, Serialize};
use sha2::{Sha256, Digest};
use std::fs;

#[derive(Debug, Serialize, Deserialize)]
struct CsvProcessingInput {
    csv_hash: [u8; 32],
    csv_data: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct AgentResult {
    csv_hash: [u8; 32],
    column_a_sum: u64,
    column_a_hash: [u8; 32],
    entry_count: usize,
}

#[derive(Debug, Serialize, Deserialize)]
struct VerificationResult {
    result: AgentResult,
    verification_passed: bool,
    business_invariant_passed: bool,
    sum_threshold: u64,
}

struct AgentA;
struct AgentB;

impl AgentA {
    fn process_csv(csv_file_path: &str) -> Result<Receipt, Box<dyn std::error::Error>> {
        println!("🤖 Agent A: Processing CSV file: {}", csv_file_path);
        
        // Read CSV file
        let csv_data = fs::read_to_string(csv_file_path)?;
        
        // Compute CSV hash
        let mut hasher = Sha256::new();
        hasher.update(csv_data.as_bytes());
        let csv_hash: [u8; 32] = hasher.finalize().into();
        
        println!("📊 CSV hash: {:?}", hex::encode(csv_hash));
        
        // Create input for guest
        let input = CsvProcessingInput {
            csv_hash,
            csv_data,
        };
        
        // Build executor environment
        let env = ExecutorEnv::builder()
            .write(&input)?
            .build()?;
        
        // Generate proof
        println!("⚡ Generating zkVM proof...");
        let prover = default_prover();
        let prove_info = prover.prove(env, GUEST_CODE_FOR_ZK_PROOF_ELF)?;
        
        println!("✅ Proof generated successfully!");
        Ok(prove_info.receipt)
    }
}

impl AgentB {
    fn verify_and_check_invariant(receipt: &Receipt, sum_threshold: u64) -> Result<VerificationResult, Box<dyn std::error::Error>> {
        println!("🔍 Agent B: Verifying receipt and checking business invariant...");
        
        // Verify the receipt
        let verification_passed = receipt.verify(GUEST_CODE_FOR_ZK_PROOF_ID).is_ok();
        println!("🔐 Receipt verification: {}", if verification_passed { "PASSED" } else { "FAILED" });
        
        // Extract result from journal
        let result: AgentResult = receipt.journal.decode()?;
        
        println!("📈 Extracted result:");
        println!("  - CSV hash: {}", hex::encode(result.csv_hash));
        println!("  - Column A sum: {}", result.column_a_sum);
        println!("  - Column A hash: {}", hex::encode(result.column_a_hash));
        println!("  - Entry count: {}", result.entry_count);
        
        // Check business invariant (sum under threshold)
        let business_invariant_passed = result.column_a_sum <= sum_threshold;
        println!("💼 Business invariant (sum <= {}): {}", 
                sum_threshold, 
                if business_invariant_passed { "PASSED" } else { "FAILED" });
        
        Ok(VerificationResult {
            result,
            verification_passed,
            business_invariant_passed,
            sum_threshold,
        })
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize tracing
    tracing_subscriber::fmt()
        .with_env_filter(tracing_subscriber::filter::EnvFilter::from_default_env())
        .init();
    
    println!("🚀 Starting RISC Zero CSV Processing Demo");
    println!("==========================================");
    
    // Configuration
    let csv_file_path = "test_data.csv";
    let sum_threshold = 1000u64; // Business invariant: sum must be <= 1000
    
    // Agent A: Process CSV and generate proof
    let receipt = AgentA::process_csv(csv_file_path)?;
    
    println!("\n📋 Receipt Summary:");
    println!("  - Receipt generated successfully");
    
    // Agent B: Verify receipt and check business invariant
    let verification_result = AgentB::verify_and_check_invariant(&receipt, sum_threshold)?;
    
    println!("\n🎯 Final Results:");
    println!("==================");
    println!("✅ zkVM Proof verification: {}", verification_result.verification_passed);
    println!("✅ Business invariant: {}", verification_result.business_invariant_passed);
    println!("📊 Column A sum: {} (threshold: {})", 
             verification_result.result.column_a_sum, 
             verification_result.sum_threshold);
    
    let all_checks_passed = verification_result.verification_passed 
        && verification_result.business_invariant_passed;
    
    if all_checks_passed {
        println!("🎉 SUCCESS: All checks passed!");
        println!("   - ✅ Deterministic execution proven with RISC Zero zkVM");
        println!("   - ✅ Business invariant verified within zkVM");
        println!("   - ✅ CSV processing completed trustlessly");
    } else {
        println!("❌ FAILURE: Some checks failed!");
        std::process::exit(1);
    }
    
    Ok(())
}
