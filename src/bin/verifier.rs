use risc0_zkvm::Receipt;
use std::fs;
use zkvm_verifier::{CsvProcessingOutput, THRESHOLD};

include!(concat!(env!("OUT_DIR"), "/methods.rs"));

fn main() -> anyhow::Result<()> {
    println!("Agent B: Loading and verifying receipt...");
    
    // Load receipt from file
    let receipt_bytes = fs::read("receipt.bin")?;
    let receipt: Receipt = bincode::deserialize(&receipt_bytes)?;
    
    // Verify the receipt
    receipt.verify(CSV_PROCESSOR_ID)?;
    println!("✓ Receipt cryptographically verified!");
    
    // Extract and validate the output
    let output: CsvProcessingOutput = receipt.journal.decode()?;
    
    println!("Extracted results:");
    println!("  CSV Hash: {}", output.csv_hash);
    println!("  Column A Sum: {}", output.column_a_sum);
    println!("  SHA256 of Sum: {}", output.sha256_sum);
    println!("  Under Threshold ({}): {}", THRESHOLD, output.is_under_threshold);
    
    // Agent B's business logic validation
    let sum_value: u64 = output.column_a_sum.parse()?;
    let expected_threshold_check = sum_value < THRESHOLD;
    
    if output.is_under_threshold == expected_threshold_check {
        println!("✓ Business invariant validation passed!");
        
        // Additional custom validation (Agent B's acceptance criteria)
        if output.is_under_threshold {
            println!("✓ Agent B ACCEPTS: Sum is under threshold and properly verified");
            accept_task(&output);
        } else {
            println!("⚠ Agent B CONDITIONAL ACCEPT: Sum exceeds threshold but proof is valid");
            conditional_accept_task(&output);
        }
    } else {
        println!("✗ Agent B REJECTS: Business invariant validation failed!");
        reject_task(&output);
    }
    
    Ok(())
}

fn accept_task(output: &CsvProcessingOutput) {
    println!("🎉 Task accepted! Processing sum: {}", output.column_a_sum);
    // Here you would integrate with your business logic
}

fn conditional_accept_task(output: &CsvProcessingOutput) {
    println!("⚠️  Task conditionally accepted. Manual review may be required.");
    println!("   Sum {} exceeds threshold {}", output.column_a_sum, THRESHOLD);
    // Here you would flag for manual review or escalation
}

fn reject_task(output: &CsvProcessingOutput) {
    println!("❌ Task rejected due to validation failure.");
    // Here you would handle rejection logic
}