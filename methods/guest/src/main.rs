use risc0_zkvm::guest::env;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

#[derive(Clone, Debug, Serialize, Deserialize)]
struct CsvProcessingInput {
    csv_hash: String,
    csv_data: String,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
struct CsvProcessingOutput {
    csv_hash: String,
    column_a_sum: String,
    sha256_sum: String,
    is_under_threshold: bool,
}

const THRESHOLD: u64 = 1000;

fn main() {
    let input: CsvProcessingInput = env::read();
    
    // Verify CSV hash matches the data
    let mut hasher = Sha256::new();
    hasher.update(input.csv_data.as_bytes());
    let computed_hash = format!("{:x}", hasher.finalize());
    
    assert_eq!(input.csv_hash, computed_hash, "CSV hash verification failed");
    
    // Parse CSV and sum column A
    let mut column_a_sum: u64 = 0;
    let lines: Vec<&str> = input.csv_data.lines().collect();
    
    // Skip header row (index 0)
    for line in lines.iter().skip(1) {
        let columns: Vec<&str> = line.split(',').collect();
        if !columns.is_empty() {
            if let Ok(value) = columns[0].trim().parse::<u64>() {
                column_a_sum += value;
            }
        }
    }
    
    // Compute SHA256 of the sum
    let sum_string = column_a_sum.to_string();
    let mut sum_hasher = Sha256::new();
    sum_hasher.update(sum_string.as_bytes());
    let sha256_sum = format!("{:x}", sum_hasher.finalize());
    
    // Check business invariant
    let is_under_threshold = column_a_sum < THRESHOLD;
    
    let output = CsvProcessingOutput {
        csv_hash: input.csv_hash,
        column_a_sum: sum_string,
        sha256_sum,
        is_under_threshold,
    };
    
    env::commit(&output);
}