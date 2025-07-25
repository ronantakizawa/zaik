#!/bin/bash

echo "🤖 AI Agent Test Script"
echo "======================="
echo

echo "This script demonstrates the AI agent task:"
echo "Given a CSV hash h, compute the SHA256 sum of column A and return it"
echo

echo "🔍 Inspecting CSV files:"
echo "File: test_data.csv"
cat test_data.csv
echo
echo "File: test_data_large.csv"  
cat test_data_large.csv
echo

echo "📊 Expected behavior:"
echo "1. Agent A processes CSV inside RISC Zero zkVM"
echo "2. Computes SHA256 hash of CSV content for verification"
echo "3. Parses column A values and computes sum"
echo "4. Generates cryptographic proof of execution"
echo "5. Agent B verifies proof and checks business invariant"
echo "6. Optional: Custom SNARK enforces sum <= threshold constraint"
echo

echo "🏃 Running with dev mode for faster testing..."
RISC0_DEV_MODE=1 cargo run --release

echo
echo "🔒 For full cryptographic proofs, run:"
echo "RISC0_DEV_MODE=0 cargo run --release"
echo
echo "⚡ To see execution statistics:"
echo "RISC0_DEV_MODE=1 RUST_LOG=info RISC0_INFO=1 cargo run --release"