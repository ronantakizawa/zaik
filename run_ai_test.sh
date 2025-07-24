#!/bin/bash

echo "🤖 AI Agent zkVM Testing System"
echo "==============================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create it with your OPENAI_API_KEY"
    exit 1
fi

# Source environment variables
source .env

# Check if API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY not set in .env file"
    exit 1
fi

echo "📦 Building project with AI agent support..."
cargo build --release

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo ""
echo "🚀 Starting AI Agent Testing..."
echo "This will:"
echo "  1. Use AI to generate different CSV datasets"
echo "  2. Process each through the zkVM system"
echo "  3. Generate SNARK proofs for business logic"
echo "  4. Have AI agents analyze and make decisions"
echo ""

# Run the AI agent test
cargo run --bin ai_agent_test

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ AI Agent Testing completed successfully!"
    echo ""
    echo "📊 Summary:"
    echo "- AI agents successfully generated test data"
    echo "- zkVM proofs were generated and verified"
    echo "- SNARK business logic proofs were validated"
    echo "- AI verifiers made autonomous decisions"
    echo "- Complete end-to-end AI-driven testing achieved"
else
    echo "❌ AI Agent Testing failed"
    exit 1
fi