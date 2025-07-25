"""
Python wrapper for RISC Zero deterministic verifier
"""
import subprocess
import json
import hashlib
import os
import tempfile
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

@dataclass
class VerificationResult:
    success: bool
    csv_hash: str
    column_a_sum: int
    column_a_hash: str
    entry_count: int
    verification_passed: bool
    business_invariant_passed: bool
    snark_proof_valid: bool
    proof_hash: Optional[str] = None
    error_message: Optional[str] = None

class RISC0Verifier:
    """Python wrapper for the RISC Zero CSV processing verifier"""
    
    def __init__(self, project_root: Optional[str] = None):
        if project_root is None:
            project_root = Path(__file__).parent.parent.absolute()
        self.project_root = Path(project_root)
        self.rust_binary = self.project_root / "target" / "release" / "host"
        
    def ensure_binary_exists(self) -> bool:
        """Ensure the Rust binary is compiled"""
        if not self.rust_binary.exists():
            print("🔨 Compiling RISC Zero verifier...")
            result = subprocess.run(
                ["cargo", "build", "--release"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                env={**os.environ, "RISC0_DEV_MODE": "1"}
            )
            if result.returncode != 0:
                raise Exception(f"Failed to compile RISC Zero verifier: {result.stderr}")
        return True
    
    def compute_csv_hash(self, csv_content: str) -> str:
        """Compute SHA256 hash of CSV content"""
        return hashlib.sha256(csv_content.encode()).hexdigest()
    
    def create_temp_csv(self, csv_content: str) -> str:
        """Create a temporary CSV file"""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        temp_file.write(csv_content)
        temp_file.close()
        return temp_file.name
    
    def run_verification(
        self, 
        csv_content: str, 
        threshold: int = 1000,
        use_dev_mode: bool = True
    ) -> VerificationResult:
        """
        Run the RISC Zero verification on CSV content
        
        Args:
            csv_content: The CSV data as a string
            threshold: Business logic threshold for column A sum
            use_dev_mode: Whether to use RISC0_DEV_MODE for faster execution
        
        Returns:
            VerificationResult with all verification details
        """
        try:
            self.ensure_binary_exists()
            
            # Create temporary CSV file
            temp_csv_path = self.create_temp_csv(csv_content)
            
            try:
                # Modify the Rust code to use the temporary CSV file
                self._update_csv_path_in_rust(temp_csv_path, threshold)
                
                # Recompile with new CSV path
                env = {**os.environ}
                if use_dev_mode:
                    env["RISC0_DEV_MODE"] = "1"
                else:
                    env["RISC0_DEV_MODE"] = "0"
                
                # Run the verifier
                result = subprocess.run(
                    [str(self.rust_binary)],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    env=env
                )
                
                # Parse the output
                return self._parse_verification_output(
                    result.stdout, 
                    result.stderr, 
                    result.returncode,
                    csv_content
                )
                
            finally:
                # Clean up temporary file
                os.unlink(temp_csv_path)
                
        except Exception as e:
            return VerificationResult(
                success=False,
                csv_hash="",
                column_a_sum=0,
                column_a_hash="",
                entry_count=0,
                verification_passed=False,
                business_invariant_passed=False,
                snark_proof_valid=False,
                error_message=str(e)
            )
    
    def _update_csv_path_in_rust(self, csv_path: str, threshold: int):
        """Temporarily update the Rust code to use the provided CSV path"""
        host_main_path = self.project_root / "host" / "src" / "main.rs"
        
        # Read current content
        with open(host_main_path, 'r') as f:
            content = f.read()
        
        # Replace CSV path and threshold
        updated_content = content.replace(
            'let csv_file_path = "test_data.csv";',
            f'let csv_file_path = "{csv_path}";'
        ).replace(
            'let sum_threshold = 1000u64;',
            f'let sum_threshold = {threshold}u64;'
        )
        
        # Write updated content
        with open(host_main_path, 'w') as f:
            f.write(updated_content)
        
        # Recompile
        subprocess.run(
            ["cargo", "build", "--release"],
            cwd=self.project_root,
            capture_output=True,
            env={**os.environ, "RISC0_DEV_MODE": "1"}
        )
    
    def _parse_verification_output(
        self, 
        stdout: str, 
        stderr: str, 
        return_code: int,
        csv_content: str
    ) -> VerificationResult:
        """Parse the output from the RISC Zero verifier"""
        
        if return_code != 0 and "FAILURE" not in stdout:
            return VerificationResult(
                success=False,
                csv_hash="",
                column_a_sum=0,
                column_a_hash="",
                entry_count=0,
                verification_passed=False,
                business_invariant_passed=False,
                snark_proof_valid=False,
                error_message=f"Verifier failed: {stderr}"
            )
        
        try:
            # Extract information from output
            csv_hash = ""
            column_a_sum = 0
            column_a_hash = ""
            entry_count = 0
            verification_passed = False
            business_invariant_passed = False
            snark_proof_valid = False
            proof_hash = None
            
            lines = stdout.split('\n')
            for line in lines:
                if "CSV hash:" in line:
                    csv_hash = line.split('"')[1] if '"' in line else line.split(': ')[1]
                elif "Column A sum:" in line:
                    column_a_sum = int(line.split(': ')[1])
                elif "Column A hash:" in line:
                    column_a_hash = line.split(' ')[4]
                elif "Entry count:" in line:
                    entry_count = int(line.split(': ')[1])
                elif "Receipt verification: PASSED" in line:
                    verification_passed = True
                elif "Business invariant" in line and "PASSED" in line:
                    business_invariant_passed = True
                elif "Custom SNARK verification: true" in line:
                    snark_proof_valid = True
                elif "SNARK proof hash:" in line:
                    proof_hash = line.split(': ')[1]
            
            success = "SUCCESS: All checks passed!" in stdout
            
            return VerificationResult(
                success=success,
                csv_hash=csv_hash,
                column_a_sum=column_a_sum,
                column_a_hash=column_a_hash,
                entry_count=entry_count,
                verification_passed=verification_passed,
                business_invariant_passed=business_invariant_passed,
                snark_proof_valid=snark_proof_valid,
                proof_hash=proof_hash,
                error_message=None if success else "Verification failed"
            )
            
        except Exception as e:
            return VerificationResult(
                success=False,
                csv_hash=self.compute_csv_hash(csv_content),
                column_a_sum=0,
                column_a_hash="",
                entry_count=0,
                verification_passed=False,
                business_invariant_passed=False,
                snark_proof_valid=False,
                error_message=f"Failed to parse output: {str(e)}"
            )
    
    def verify_csv_data(self, csv_content: str, expected_sum: Optional[int] = None) -> Dict[str, Any]:
        """High-level verification function that returns a detailed report"""
        result = self.run_verification(csv_content)
        
        report = {
            "verification_successful": result.success,
            "risc0_proof_valid": result.verification_passed,
            "business_logic_satisfied": result.business_invariant_passed,
            "snark_proof_valid": result.snark_proof_valid,
            "csv_details": {
                "hash": result.csv_hash,
                "column_a_sum": result.column_a_sum,
                "column_a_hash": result.column_a_hash,
                "entry_count": result.entry_count
            },
            "proof_details": {
                "proof_hash": result.proof_hash,
                "deterministic_execution": result.verification_passed,
                "cryptographic_guarantees": result.snark_proof_valid
            }
        }
        
        if result.error_message:
            report["error"] = result.error_message
            
        if expected_sum is not None:
            report["sum_validation"] = {
                "expected": expected_sum,
                "actual": result.column_a_sum,
                "matches": expected_sum == result.column_a_sum
            }
        
        return report