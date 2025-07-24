use ark_bn254::{Bn254, Fr};
use ark_groth16::{Groth16, Proof, ProvingKey, VerifyingKey};
use ark_r1cs_std::prelude::*;
use ark_relations::r1cs::ConstraintSystem;
use ark_std::rand::RngCore;
use anyhow::Result;

use crate::snark_circuit::ThresholdCheckCircuit;

pub struct SnarkProver {
    pub proving_key: ProvingKey<Bn254>,
    pub verifying_key: VerifyingKey<Bn254>,
}

impl SnarkProver {
    pub fn setup<R: RngCore>(rng: &mut R) -> Result<Self> {
        // Create a dummy circuit for setup
        let dummy_circuit = ThresholdCheckCircuit {
            sum: None,
            threshold: None,
            is_under_threshold: None,
        };

        // Generate the universal parameters
        let (proving_key, verifying_key) = Groth16::<Bn254>::circuit_specific_setup(dummy_circuit, rng)
            .map_err(|e| anyhow::anyhow!("Setup failed: {:?}", e))?;

        Ok(SnarkProver {
            proving_key,
            verifying_key,
        })
    }

    pub fn prove<R: RngCore>(
        &self,
        rng: &mut R,
        sum: u64,
        threshold: u64,
        is_under_threshold: bool,
    ) -> Result<Proof<Bn254>> {
        let circuit = ThresholdCheckCircuit {
            sum: Some(Fr::from(sum)),
            threshold: Some(Fr::from(threshold)),
            is_under_threshold: Some(Boolean::constant(is_under_threshold)),
        };

        let proof = Groth16::<Bn254>::prove(&self.proving_key, circuit, rng)
            .map_err(|e| anyhow::anyhow!("Proving failed: {:?}", e))?;

        Ok(proof)
    }

    pub fn verify(
        &self,
        proof: &Proof<Bn254>,
        threshold: u64,
        is_under_threshold: bool,
    ) -> Result<bool> {
        let public_inputs = vec![
            Fr::from(threshold),
            if is_under_threshold { Fr::from(1u64) } else { Fr::from(0u64) },
        ];

        let verified = Groth16::<Bn254>::verify(&self.verifying_key, &public_inputs, proof)
            .map_err(|e| anyhow::anyhow!("Verification failed: {:?}", e))?;

        Ok(verified)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use ark_std::test_rng;

    #[test]
    fn test_snark_proof_generation_and_verification() {
        let mut rng = test_rng();
        let prover = SnarkProver::setup(&mut rng).unwrap();

        // Test case: sum under threshold
        let sum = 500u64;
        let threshold = 1000u64;
        let is_under = true;

        let proof = prover.prove(&mut rng, sum, threshold, is_under).unwrap();
        let verified = prover.verify(&proof, threshold, is_under).unwrap();
        assert!(verified);

        // Test case: sum over threshold
        let sum = 1500u64;
        let threshold = 1000u64;
        let is_under = false;

        let proof = prover.prove(&mut rng, sum, threshold, is_under).unwrap();
        let verified = prover.verify(&proof, threshold, is_under).unwrap();
        assert!(verified);
    }
}