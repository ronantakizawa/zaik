#!/usr/bin/env python3
"""
Simple integration test for AI agents + RISC Zero
"""

import asyncio
import sys
from pathlib import Path

# Add the ai_agents module to path
sys.path.append(str(Path(__file__).parent))

from ai_agents.risc0_verifier import RISC0Verifier
from ai_agents.openai_client import OpenAIClient, AgentMessage, AgentPrompts

async def test_risc0_integration():
    """Test RISC Zero integration"""
    print("🔧 Testing RISC Zero Integration...")
    
    # Load test CSV
    csv_content = """value_a,value_b,description
100,50,First entry
200,75,Second entry
150,25,Third entry
300,100,Fourth entry
50,200,Fifth entry"""
    
    verifier = RISC0Verifier()
    
    try:
        result = verifier.verify_csv_data(csv_content)
        print(f"✅ RISC Zero verification: {'SUCCESS' if result['verification_successful'] else 'FAILED'}")
        print(f"📊 Column A sum: {result['csv_details']['column_a_sum']}")
        print(f"🔐 Proof valid: {result['risc0_proof_valid']}")
        return True
    except Exception as e:
        print(f"❌ RISC Zero test failed: {e}")
        return False

async def test_openai_integration():
    """Test OpenAI integration"""
    print("🤖 Testing OpenAI Integration...")
    
    try:
        client = OpenAIClient()
        
        messages = [AgentMessage(
            role="user", 
            content="Analyze this CSV data: value_a,value_b\\n100,50\\n200,75. What's the sum of column A?"
        )]
        
        response = await client.chat_completion(
            messages=messages,
            system_prompt=AgentPrompts.CSV_ANALYZER
        )
        
        print(f"✅ OpenAI response received")
        print(f"📝 Content preview: {response.content[:100]}...")
        return True
    except Exception as e:
        print(f"❌ OpenAI test failed: {e}")
        return False

async def main():
    """Run integration tests"""
    print("🧪 Running Integration Tests")
    print("=" * 40)
    
    risc0_ok = await test_risc0_integration()
    print()
    openai_ok = await test_openai_integration()
    
    print("\n" + "=" * 40)
    if risc0_ok and openai_ok:
        print("🎉 All integration tests passed!")
        print("Ready to run the full AI agent workflow demo.")
    else:
        print("❌ Some tests failed. Check your setup:")
        if not risc0_ok:
            print("  • RISC Zero verifier needs compilation")
        if not openai_ok:
            print("  • OpenAI API key may be invalid or missing")

if __name__ == "__main__":
    asyncio.run(main())