use risc0_zkvm::{default_prover, ExecutorEnv, Receipt};
use sha2::{Digest, Sha256};
use std::fs;
use zkvm_verifier::{CsvProcessingInput, CsvProcessingOutput};

include!(concat!(env!("OUT_DIR"), "/methods.rs"));

fn main() -> anyhow::Result<()> {
    // Sample CSV data
    let csv_data = "column_a,column_b,column_c\n100,hello,world\n200,foo,bar\n150,test,data\n50,more,info";
    
    // Compute CSV hash
    let mut hasher = Sha256::new();
    hasher.update(csv_data.as_bytes());
    let csv_hash = format!("{:x}", hasher.finalize());
    
    println!("CSV Hash: {}", csv_hash);
    println!("CSV Data:\n{}", csv_data);
    
    let input = CsvProcessingInput {
        csv_hash: csv_hash.clone(),
        csv_data: csv_data.to_string(),
    };
    
    // Create executor environment
    let env = ExecutorEnv::builder()
        .write(&input)?
        .build()?;
    
    // Generate proof
    println!("Generating proof...");
    let prover = default_prover();
    let receipt = prover.prove(env, CSV_PROCESSOR_ELF)?;
    
    // Extract output
    let output: CsvProcessingOutput = receipt.journal.decode()?;
    
    println!("Proof generated successfully!");
    println!("Column A Sum: {}", output.column_a_sum);
    println!("SHA256 of Sum: {}", output.sha256_sum);
    println!("Under Threshold: {}", output.is_under_threshold);
    
    // Save receipt to file for verifier
    let receipt_bytes = bincode::serialize(&receipt)?;
    fs::write("receipt.bin", receipt_bytes)?;
    println!("Receipt saved to receipt.bin");
    
    // Verify the receipt locally
    receipt.verify(CSV_PROCESSOR_ID)?;
    println!("Receipt verified successfully by host!");
    
    Ok(())
}