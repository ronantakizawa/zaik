use ark_ff::PrimeField;
use ark_r1cs_std::prelude::*;
use ark_relations::r1cs::{ConstraintSynthesizer, ConstraintSystemRef, SynthesisError};

#[derive(Clone)]
pub struct ThresholdCheckCircuit<F: PrimeField> {
    pub sum: Option<F>,
    pub threshold: Option<F>,
    pub is_under_threshold: Option<Boolean<F>>,
}

impl<F: PrimeField> ConstraintSynthesizer<F> for ThresholdCheckCircuit<F> {
    fn generate_constraints(self, cs: ConstraintSystemRef<F>) -> Result<(), SynthesisError> {
        // Allocate the sum as a private witness
        let sum = FpVar::new_witness(cs.clone(), || {
            self.sum.ok_or(SynthesisError::AssignmentMissing)
        })?;

        // Allocate the threshold as a public input
        let threshold = FpVar::new_input(cs.clone(), || {
            self.threshold.ok_or(SynthesisError::AssignmentMissing)
        })?;

        // Allocate the result as a public output
        let is_under_threshold = Boolean::new_input(cs.clone(), || {
            self.is_under_threshold.ok_or(SynthesisError::AssignmentMissing)
        })?;

        // Constraint: if sum < threshold, then is_under_threshold should be true
        // if sum >= threshold, then is_under_threshold should be false
        
        // Check if sum < threshold
        let sum_lt_threshold = sum.is_cmp(&threshold, std::cmp::Ordering::Less, false)?;
        
        // Enforce that is_under_threshold equals (sum < threshold)
        is_under_threshold.enforce_equal(&sum_lt_threshold)?;

        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use ark_bn254::Fr;
    use ark_relations::r1cs::ConstraintSystem;

    #[test]
    fn test_threshold_circuit_under() {
        let cs = ConstraintSystem::<Fr>::new_ref();
        
        let sum = Fr::from(500u64);
        let threshold = Fr::from(1000u64);
        let is_under = Boolean::constant(true);
        
        let circuit = ThresholdCheckCircuit {
            sum: Some(sum),
            threshold: Some(threshold),
            is_under_threshold: Some(is_under),
        };
        
        circuit.generate_constraints(cs.clone()).unwrap();
        assert!(cs.is_satisfied().unwrap());
    }

    #[test]
    fn test_threshold_circuit_over() {
        let cs = ConstraintSystem::<Fr>::new_ref();
        
        let sum = Fr::from(1500u64);
        let threshold = Fr::from(1000u64);
        let is_under = Boolean::constant(false);
        
        let circuit = ThresholdCheckCircuit {
            sum: Some(sum),
            threshold: Some(threshold),
            is_under_threshold: Some(is_under),
        };
        
        circuit.generate_constraints(cs.clone()).unwrap();
        assert!(cs.is_satisfied().unwrap());
    }
}