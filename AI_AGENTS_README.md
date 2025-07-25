# AI Agent Workflow with RISC Zero Deterministic Verification

A comprehensive Python-based AI agent workflow system that combines OpenAI GPT-4 agents with RISC Zero zkVM for deterministic verification and cryptographic guarantees.

## 🎯 Overview

This project demonstrates a multi-agent AI system where:
- **Multiple specialized AI agents** analyze data and make decisions
- **RISC Zero zkVM** provides deterministic execution proofs  
- **Cryptographic verification** ensures trustless computation
- **Business logic compliance** is enforced through custom SNARKs
- **Risk assessment and security** analysis provide comprehensive validation

## 🏗️ Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                 AI Agent Workflow System                    │
├─────────────────────────────────────────────────────────────┤
│  🤖 AI Agents (OpenAI GPT-4)    │  🔒 RISC Zero Verifier   │
│  ├── Data Quality Agent         │  ├── zkVM Execution      │
│  ├── CSV Analyzer Agent         │  ├── Proof Generation    │
│  ├── Security Agent            │  ├── Business Logic      │
│  ├── Business Logic Agent      │  └── SNARK Verification  │
│  ├── Verification Agent        │                           │
│  ├── Risk Assessment Agent     │                           │
│  └── Orchestrator Agent        │                           │
└─────────────────────────────────────────────────────────────┘
```

### Workflow Steps

1. **Data Quality Assessment** - Evaluates CSV data integrity and quality
2. **CSV Analysis** - AI-powered data structure and content analysis  
3. **RISC Zero Verification** - Deterministic execution with cryptographic proofs
4. **Security Assessment** - Evaluates cryptographic guarantees and attack vectors
5. **Business Logic Validation** - Checks compliance with business rules
6. **Verification Review** - AI agent validates all results
7. **Risk Assessment** - Comprehensive risk analysis and mitigation recommendations
8. **Orchestrated Decision** - Final multi-agent consensus with confidence scoring

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Rust toolchain** with RISC Zero support
3. **OpenAI API key** in `.env` file
4. **Required Python packages** (see requirements.txt)

### Setup

```bash
# 1. Install dependencies and compile RISC Zero
./setup_ai_agents.sh

# 2. Test integration
python3 test_integration.py

# 3. Run basic demo
python3 ai_agent_demo.py

# 4. Run enhanced demo (with all specialized agents)
python3 enhanced_ai_demo.py
```

## 📁 Project Structure

```
ai_agents/
├── __init__.py                 # Package initialization
├── openai_client.py           # OpenAI API integration
├── risc0_verifier.py          # RISC Zero Python wrapper
├── agent_workflow.py          # Basic workflow orchestration
├── enhanced_workflow.py       # Enhanced multi-agent workflow
└── specialized_agents.py      # Specialized agent implementations

# Demo Scripts
├── ai_agent_demo.py           # Basic workflow demo
├── enhanced_ai_demo.py        # Enhanced workflow demo
├── test_integration.py        # Integration tests
└── setup_ai_agents.sh         # Setup script

# Configuration
├── requirements.txt           # Python dependencies
└── .env                      # OpenAI API key
```

## 🤖 Agent Specializations

### Core Agents

- **CSV Analyzer Agent**: Data structure analysis and pattern recognition
- **Verification Agent**: Result validation and acceptance/rejection decisions
- **Orchestrator Agent**: Workflow coordination and final decision making

### Specialized Agents

- **Data Quality Agent**: Data integrity, completeness, and quality scoring
- **Security Agent**: Cryptographic proof validation and security assessment
- **Business Logic Agent**: Business rule compliance and process validation
- **Risk Assessment Agent**: Comprehensive risk analysis and mitigation planning

## 🔒 RISC Zero Integration

The Python wrapper (`risc0_verifier.py`) provides seamless integration with the Rust-based RISC Zero verifier:

```python
from ai_agents.risc0_verifier import RISC0Verifier

verifier = RISC0Verifier()
result = verifier.verify_csv_data(csv_content)

# Returns comprehensive verification report:
# - verification_successful: bool
# - risc0_proof_valid: bool  
# - business_logic_satisfied: bool
# - snark_proof_valid: bool
# - csv_details: {...}
# - proof_details: {...}
```

## 📊 Example Workflow Output

```
🚀 Starting Enhanced AI Agent Workflow
==========================================
🔍 Step 1: Data Quality Assessment
   📊 Quality Score: 0.95
🤖 Step 2: CSV Analysis  
   📊 Analysis: Data structure validated, column A contains numeric values...
   🎯 Confidence: 0.92
🔒 Step 3: RISC Zero Verification
   ✅ Verification: PASSED
   🔐 RISC Zero Proof: VALID
   💼 Business Logic: SATISFIED
   📊 Column A Sum: 800
🛡️ Step 4: Security Assessment
   🔐 Security Level: high
🔍 Step 5: Business Logic Validation
   ✅ Compliance: pass
⚠️ Step 6: Risk Assessment
   ⚠️ Risk Level: low
🔍 Step 7: Verification Agent Review
   🔍 Review: All verification checks passed...
   🎯 Confidence: 0.88
🎯 Step 8: Enhanced Orchestrator Decision
   🎯 Enhanced Decision: ACCEPT
   📊 Decision Confidence: 0.91
   ⚖️ Critical Factors Pass: True
   🛡️ Risk Acceptable: True

🎯 Enhanced Workflow Result
✅ SUCCESS
Final Decision: ACCEPT
Overall Confidence: 0.91
Enhanced Analysis: ✅
```

## 🔧 Configuration Options

### Workflow Configuration

```python
workflow = EnhancedAgentWorkflow()

# Run with all specialized agents
results = await workflow.run_enhanced_csv_workflow(
    csv_content=csv_data,
    business_threshold=1000,
    enable_all_agents=True  # Enable all specialized agents
)

# Run basic workflow
results = await workflow.run_csv_analysis_workflow(
    csv_content=csv_data,
    business_threshold=1000
)
```

### OpenAI Configuration

```python
client = OpenAIClient(model="gpt-4-turbo-preview")

# Adjust temperature for more/less creative responses
response = await client.chat_completion(
    messages=messages,
    temperature=0.1,  # Low for deterministic analysis
    max_tokens=2000
)
```

### RISC Zero Configuration

```python
verifier = RISC0Verifier(project_root="/path/to/risc0/project")

# Run with different modes
result = verifier.run_verification(
    csv_content=data,
    threshold=1000,
    use_dev_mode=True  # Faster for development
)
```

## 🎭 Demo Scenarios

### Demo 1: Successful Verification
- CSV sum: 800 (under threshold of 1000)
- All agents agree: ACCEPT
- High confidence across all agents
- All cryptographic proofs valid

### Demo 2: Business Logic Failure
- CSV sum: 1550 (exceeds threshold of 1000) 
- RISC Zero proof valid but business rule violated
- Agents recommend: REJECT
- Risk assessment flags compliance failure

### Demo 3: Comparison Analysis
- Side-by-side basic vs enhanced workflows
- Shows value of specialized agents
- Demonstrates comprehensive risk analysis

## 🛡️ Security & Trust Guarantees

### Cryptographic Guarantees
- **Deterministic Execution**: RISC Zero zkVM ensures reproducible computation
- **Proof Validity**: Cryptographic verification of execution correctness
- **Data Integrity**: SHA256 hashing prevents data tampering
- **Business Logic Enforcement**: Custom SNARKs ensure rule compliance

### Multi-Agent Consensus
- **Specialized Analysis**: Each agent provides domain expertise
- **Cross-Validation**: Multiple agents validate results independently  
- **Risk Assessment**: Comprehensive evaluation of failure scenarios
- **Confidence Scoring**: Quantitative trust metrics for decisions

## 🚧 Development & Testing

### Running Tests

```bash
# Integration tests
python3 test_integration.py

# Basic workflow test
python3 ai_agent_demo.py

# Full enhanced workflow test  
python3 enhanced_ai_demo.py
```

### Development Mode

For faster iteration during development:

```bash
# Use RISC Zero dev mode (faster, no real proofs)
RISC0_DEV_MODE=1 python3 enhanced_ai_demo.py

# Use real cryptographic proofs
RISC0_DEV_MODE=0 python3 enhanced_ai_demo.py
```

## 🔮 Future Enhancements

### Planned Features
- **Blockchain Integration**: Deploy verification on-chain
- **Merkle Tree Inputs**: Support for large dataset commitments  
- **Optimistic Rollbacks**: Fault tolerance and recovery mechanisms
- **Real-time Monitoring**: Live workflow status and metrics
- **Custom Agent Training**: Fine-tuned models for specific domains

### Extensibility Points
- **New Agent Types**: Easy to add specialized agents
- **Custom Verification Logic**: Pluggable business rule engines
- **Multiple Data Sources**: Support beyond CSV (JSON, databases, APIs)
- **Advanced SNARKs**: More complex cryptographic constraints

## 📈 Performance Considerations

### Execution Times
- **Basic Workflow**: ~30-60 seconds (dev mode)
- **Enhanced Workflow**: ~60-120 seconds (dev mode)
- **Real Proofs**: 5-15 minutes (depending on data size)

### Scalability
- **Parallel Agent Execution**: Agents can run concurrently
- **Batch Processing**: Multiple CSV files in single workflow
- **Remote Proving**: Use Bonsai for faster proof generation

## 📚 API Reference

See individual module documentation:
- [`openai_client.py`](ai_agents/openai_client.py) - OpenAI integration
- [`risc0_verifier.py`](ai_agents/risc0_verifier.py) - RISC Zero wrapper
- [`agent_workflow.py`](ai_agents/agent_workflow.py) - Basic workflow
- [`enhanced_workflow.py`](ai_agents/enhanced_workflow.py) - Enhanced workflow
- [`specialized_agents.py`](ai_agents/specialized_agents.py) - Agent implementations

---

## 🎉 Success Metrics

This implementation successfully demonstrates:

✅ **Multi-agent AI coordination** with OpenAI GPT-4  
✅ **Deterministic verification** with RISC Zero zkVM  
✅ **Cryptographic proof generation** and validation  
✅ **Business logic compliance** enforcement  
✅ **Comprehensive risk assessment** and security analysis  
✅ **End-to-end trustless computation** pipeline  
✅ **Scalable agent architecture** for complex workflows  

The system provides a robust foundation for trustless AI agent workflows with cryptographic guarantees and comprehensive validation.