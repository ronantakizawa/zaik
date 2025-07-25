#!/bin/bash

echo "🚀 RISC Zero CSV Processing Demo"
echo "================================="
echo

echo "📋 Test 1: Processing test_data.csv (sum should pass threshold)"
echo "Expected sum: 800 (100+200+150+300+50), threshold: 1000"
cargo run --release

echo
echo "📋 Test 2: Processing test_data_large.csv (sum should exceed threshold)"
echo "Expected sum: 1550 (400+500+300+200+150), threshold: 1000"

# Temporarily modify main.rs to use test_data_large.csv
sed -i.bak 's/test_data.csv/test_data_large.csv/' host/src/main.rs

cargo run --release

# Restore original file
mv host/src/main.rs.bak host/src/main.rs

echo
echo "✅ Demo completed!"