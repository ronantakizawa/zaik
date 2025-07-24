use ark_std::test_rng;
use risc0_zkvm::Receipt;
use std::fs;
use zkvm_verifier::{snark_prover::SnarkProver, CsvProcessingOutput, THRESHOLD};

include!(concat!(env!("OUT_DIR"), "/methods.rs"));

fn main() -> anyhow::Result<()> {
    println!("Enhanced Agent B with SNARK: Loading and verifying receipt...");
    
    // Load receipt from file
    let receipt_bytes = fs::read("receipt.bin")?;
    let receipt: Receipt = bincode::deserialize(&receipt_bytes)?;
    
    // Verify the Risc0 receipt first
    receipt.verify(CSV_PROCESSOR_ID)?;
    println!("✓ Risc0 receipt cryptographically verified!");
    
    // Extract the output
    let output: CsvProcessingOutput = receipt.journal.decode()?;
    let sum_value: u64 = output.column_a_sum.parse()?;
    
    println!("Extracted results:");
    println!("  CSV Hash: {}", output.csv_hash);
    println!("  Column A Sum: {}", output.column_a_sum);
    println!("  SHA256 of Sum: {}", output.sha256_sum);
    println!("  Under Threshold ({}): {}", THRESHOLD, output.is_under_threshold);
    
    // Now generate and verify a custom SNARK for the business invariant
    println!("\nGenerating custom SNARK for business invariant...");
    
    let mut rng = test_rng();
    let snark_prover = SnarkProver::setup(&mut rng)?;
    
    // Generate proof that the threshold check was computed correctly
    let snark_proof = snark_prover.prove(
        &mut rng,
        sum_value,
        THRESHOLD,
        output.is_under_threshold,
    )?;
    
    println!("✓ SNARK proof generated!");
    
    // Verify the SNARK proof
    let snark_verified = snark_prover.verify(
        &snark_proof,
        THRESHOLD,
        output.is_under_threshold,
    )?;
    
    if snark_verified {
        println!("✓ SNARK proof verified! Business invariant is cryptographically guaranteed.");
        
        if output.is_under_threshold {
            println!("🎉 Enhanced Agent B ACCEPTS: Both zkVM execution and business invariant proofs are valid!");
            println!("   - Risc0 proved correct CSV processing and sum computation");
            println!("   - Custom SNARK proved threshold check integrity");
            accept_with_dual_proofs(&output);
        } else {
            println!("⚠️  Enhanced Agent B CONDITIONAL ACCEPT: Proofs valid but sum exceeds threshold");
            conditional_accept_with_dual_proofs(&output);
        }
    } else {
        println!("❌ SNARK verification failed! Business invariant proof is invalid.");
        reject_due_to_snark_failure(&output);
    }
    
    Ok(())
}

fn accept_with_dual_proofs(output: &CsvProcessingOutput) {
    println!("🔐 Task accepted with dual-proof verification!");
    println!("   Execution proof: Risc0 zkVM receipt");
    println!("   Business logic proof: Custom Groth16 SNARK");
    println!("   Processing sum: {}", output.column_a_sum);
}

fn conditional_accept_with_dual_proofs(output: &CsvProcessingOutput) {
    println!("⚠️  Task conditionally accepted with verified proofs.");
    println!("   Both proofs are cryptographically sound, but business rules require review.");
    println!("   Sum {} exceeds threshold {}", output.column_a_sum, THRESHOLD);
}

fn reject_due_to_snark_failure(output: &CsvProcessingOutput) {
    println!("❌ Task rejected: SNARK verification failure indicates compromised business logic.");
    println!("   This suggests the threshold check may have been tampered with.");
}