use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct CsvProcessingInput {
    pub csv_hash: String,
    pub csv_data: String,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct CsvProcessingOutput {
    pub csv_hash: String,
    pub column_a_sum: String,
    pub sha256_sum: String,
    pub is_under_threshold: bool,
}

pub const THRESHOLD: u64 = 1000;

pub mod snark_circuit;
pub mod snark_prover;
pub mod ai_agent;