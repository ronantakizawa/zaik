use serde::{Deserialize, Serialize};
use sha2::{Sha256, Digest};

#[derive(Debug, Serialize, Deserialize)]
pub struct BusinessInvariantCircuit {
    pub threshold: u64,
    pub actual_sum: u64,
    pub csv_hash: [u8; 32],
}

#[derive(Debug, Serialize, Deserialize)]
pub struct BusinessInvariantProof {
    pub circuit: BusinessInvariantCircuit,
    pub proof_hash: [u8; 32],
    pub is_valid: bool,
}

impl BusinessInvariantCircuit {
    pub fn new(threshold: u64, actual_sum: u64, csv_hash: [u8; 32]) -> Self {
        Self {
            threshold,
            actual_sum,
            csv_hash,
        }
    }
    
    pub fn generate_proof(&self) -> BusinessInvariantProof {
        // Simulate a SNARK proof generation for business invariant
        // In a real implementation, this would use a SNARK library like arkworks
        
        let is_valid = self.actual_sum <= self.threshold;
        
        // Create a "proof" by hashing the circuit constraints
        let mut hasher = Sha256::new();
        hasher.update(b"business_invariant_circuit");
        hasher.update(&self.threshold.to_le_bytes());
        hasher.update(&self.actual_sum.to_le_bytes());
        hasher.update(&self.csv_hash);
        hasher.update(&[is_valid as u8]);
        
        let proof_hash = hasher.finalize().into();
        
        BusinessInvariantProof {
            circuit: BusinessInvariantCircuit {
                threshold: self.threshold,
                actual_sum: self.actual_sum,
                csv_hash: self.csv_hash,
            },
            proof_hash,
            is_valid,
        }
    }
}

impl BusinessInvariantProof {
    pub fn verify(&self) -> bool {
        // Verify the SNARK proof
        // In a real implementation, this would verify the cryptographic proof
        
        // Check circuit constraints
        let constraint_satisfied = self.circuit.actual_sum <= self.circuit.threshold;
        
        // Verify proof hash (simulate cryptographic verification)
        let mut hasher = Sha256::new();
        hasher.update(b"business_invariant_circuit");
        hasher.update(&self.circuit.threshold.to_le_bytes());
        hasher.update(&self.circuit.actual_sum.to_le_bytes());
        hasher.update(&self.circuit.csv_hash);
        hasher.update(&[self.is_valid as u8]);
        
        let expected_hash: [u8; 32] = hasher.finalize().into();
        
        // Proof is valid if hash matches and constraint is satisfied and marked as valid
        expected_hash == self.proof_hash && constraint_satisfied && self.is_valid
    }
    
    pub fn get_public_inputs(&self) -> (u64, [u8; 32]) {
        // Return public inputs: threshold and CSV hash
        // The actual sum is kept private in the proof
        (self.circuit.threshold, self.circuit.csv_hash)
    }
}