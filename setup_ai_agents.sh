#!/bin/bash

echo "🤖 Setting up AI Agent Workflow with RISC Zero"
echo "=============================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed"
    exit 1
fi

echo "🐍 Python 3 found: $(python3 --version)"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Ensure RISC Zero binary is compiled
echo "🔨 Ensuring RISC Zero verifier is compiled..."
RISC0_DEV_MODE=1 cargo build --release

if [ $? -ne 0 ]; then
    echo "❌ Failed to compile RISC Zero verifier"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "   Please create .env with OPENAI_API_KEY=your_key_here"
    exit 1
fi

echo "✅ Setup complete!"
echo ""
echo "🧪 To run integration tests:"
echo "   python3 test_integration.py"
echo ""
echo "🚀 To run the full AI agent demo:"
echo "   python3 ai_agent_demo.py"