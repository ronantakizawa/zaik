#!/bin/bash

echo "🚀 ZkVM Verifier Demo"
echo "===================="

echo "📦 Building project..."
cargo build --release

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo ""
echo "🔨 Running host to generate proofs..."
cargo run --bin host

if [ $? -ne 0 ]; then
    echo "❌ Host execution failed"
    exit 1
fi

echo ""
echo "🔍 Running basic verifier (Agent B)..."
cargo run --bin verifier

echo ""
echo "🔐 Running enhanced SNARK verifier (Agent B with custom SNARK)..."
cargo run --bin snark_verifier

echo ""
echo "✅ Demo completed successfully!"
echo ""
echo "📊 Summary:"
echo "- Risc0 zkVM proved correct CSV processing"
echo "- Basic Agent B verified execution proof"
echo "- Enhanced Agent B verified both execution and business logic proofs"
echo "- All cryptographic verifications passed"