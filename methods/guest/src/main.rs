use risc0_zkvm::guest::env;
use sha2::{Sha256, Digest};
use serde::{Deserialize, Serialize};

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

fn main() {
    // Read the CSV processing input
    let input: CsvProcessingInput = env::read();
    
    // Verify the CSV hash matches what we received
    let mut hasher = Sha256::new();
    hasher.update(input.csv_data.as_bytes());
    let computed_hash = hasher.finalize();
    
    assert_eq!(computed_hash.as_slice(), &input.csv_hash, "CSV hash mismatch");
    
    // Parse CSV and process column A
    let mut column_a_sum: u64 = 0;
    let mut column_a_values = Vec::new();
    let mut entry_count = 0;
    
    // Simple CSV parsing (assumes first column is column A)
    for (i, line) in input.csv_data.lines().enumerate() {
        if i == 0 {
            // Skip header
            continue;
        }
        
        if let Some(first_field) = line.split(',').next() {
            if let Ok(value) = first_field.parse::<u64>() {
                column_a_sum += value;
                column_a_values.push(value.to_string());
                entry_count += 1;
            }
        }
    }
    
    // Compute SHA256 of column A values concatenated
    let column_a_concat = column_a_values.join(",");
    let mut hasher = Sha256::new();
    hasher.update(column_a_concat.as_bytes());
    let column_a_hash = hasher.finalize().into();
    
    // Create result
    let result = AgentResult {
        csv_hash: input.csv_hash,
        column_a_sum,
        column_a_hash,
        entry_count,
    };
    
    // Commit result to journal for verification
    env::commit(&result);
}
