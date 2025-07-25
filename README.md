# RISC Zero CSV Processing Agent

A deterministic AI agent implementation using RISC Zero zkVM that processes CSV data with cryptographic verification and custom business logic enforcement via SNARKs.

## Project Overview

This project implements the requirements:
- **#2 (RISC Zero/SP1 tiny deterministic verifier)**: Uses RISC Zero zkVM for deterministic execution proofs
- **#1 (custom post-condition SNARK)**: Implements custom SNARK for business invariant checking

### Agent Task

**Task**: Given a CSV hash `h`, compute the SHA256 sum of column A and return it.

**Architecture**:
- **Agent A**: Processes CSV data inside RISC Zero zkVM, generates execution proof
- **Agent B**: Verifies proof and validates business constraints
- **Custom SNARK**: Enforces business invariant (sum must be ≤ threshold)

## Features

✅ **Deterministic Execution**: No network calls, fully deterministic processing  
✅ **Full Execution Proof**: RISC Zero zkVM proves correct computation  
✅ **CSV Integrity**: SHA256 verification ensures data hasn't been tampered with  
✅ **Business Logic**: Custom SNARK enforces sum threshold constraints  
✅ **Agent Architecture**: Clear separation between processing (A) and verification (B)

## Project Structure

```
├── host/               # Host application (Agent A & B)
│   └── src/
│       ├── main.rs            # Main execution logic
│       └── snark_invariant.rs # Custom SNARK implementation
├── methods/            # RISC Zero methods
│   └── guest/          # Guest code (runs inside zkVM)
│       └── src/main.rs        # CSV processing logic
├── test_data.csv       # Sample CSV (sum=800, passes threshold)
├── test_data_large.csv # Large CSV (sum=1550, exceeds threshold)
├── run_demo.sh         # Demo script
└── run_ai_test.sh      # AI agent test script
```

## Quick Start

### Prerequisites

Install RISC Zero toolchain:
```bash
curl -L https://risczero.com/install | bash
rzup install
```

### Running the Demo

1. **Fast development testing** (dev mode):
```bash
./run_ai_test.sh
```

2. **Full cryptographic proofs**:
```bash
RISC0_DEV_MODE=0 cargo run --release
```

3. **Performance analysis**:
```bash
RISC0_DEV_MODE=1 RUST_LOG=info RISC0_INFO=1 cargo run --release
```

## How It Works

### Step 1: Agent A Processing
- Reads CSV file and computes SHA256 hash
- Sends CSV data + hash to RISC Zero guest program
- Guest verifies hash matches, parses column A, computes sum
- Generates cryptographic proof of execution

### Step 2: Agent B Verification  
- Verifies RISC Zero receipt cryptographically
- Extracts computation results from proof journal
- Checks business invariant (sum ≤ threshold)
- Optionally generates custom SNARK for additional constraints

### Step 3: Custom SNARK (Optional)
- Creates zero-knowledge proof that sum ≤ threshold
- Keeps actual sum private while proving constraint satisfaction
- Provides additional cryptographic guarantee beyond zkVM proof

## Test Data

- `test_data.csv`: Sum = 800 (passes threshold of 1000)
- `test_data_large.csv`: Sum = 1550 (exceeds threshold of 1000)

## Expected Output

```
🚀 Starting RISC Zero CSV Processing Demo
==========================================
🤖 Agent A: Processing CSV file: test_data.csv
📊 CSV hash: a1b2c3...
⚡ Generating zkVM proof...
✅ Proof generated successfully!

🔍 Agent B: Verifying receipt and checking business invariant...
🔐 Receipt verification: PASSED
📈 Extracted result:
  - CSV hash: a1b2c3...
  - Column A sum: 800
  - Column A hash: d4e5f6...
  - Entry count: 5
💼 Business invariant (sum <= 1000): PASSED
🔒 Generating custom SNARK for business invariant...
✨ SNARK proof generated!
🔐 SNARK verification: PASSED

🎯 Final Results:
==================
✅ zkVM Proof verification: true
✅ Business invariant: true
✅ Custom SNARK verification: true
🎉 SUCCESS: All checks passed!
   - ✅ Deterministic execution proven with RISC Zero zkVM
   - ✅ Business invariant enforced with custom SNARK
   - ✅ CSV processing completed trustlessly
```

## Technical Details

### Security Properties
- **Determinism**: All execution happens inside zkVM, no external dependencies
- **Integrity**: CSV hash verification prevents data tampering  
- **Completeness**: Full execution trace is cryptographically proven
- **Privacy**: Custom SNARK can hide sensitive values while proving constraints

### Future Enhancements
- Merkle-committed inputs for large datasets
- Optimistic rollback mechanisms
- Integration with blockchain verification
- More complex business logic constraints

## Development

Build and test:
```bash
cargo build --release
cargo test
./run_demo.sh
```

For development iteration, use dev mode to skip proof generation:
```bash
RISC0_DEV_MODE=1 cargo run --release
```

---

## Resources

- [RISC Zero Developer Docs](https://dev.risczero.com)
- [RISC Zero Examples](https://github.com/risc0/risc0/tree/main/examples)
- [RISC Zero zkVM Reference](https://docs.rs/risc0-zkvm)
