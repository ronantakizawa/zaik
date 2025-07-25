#!/usr/bin/env python3
"""
Quick start script for AI Agent Workflow
"""

import asyncio
import sys
from pathlib import Path

# Add the ai_agents module to path
sys.path.append(str(Path(__file__).parent))

async def main():
    print("🤖 AI Agent Workflow with RISC Zero - Quick Start")
    print("=" * 55)
    
    # Simple demo
    try:
        from ai_agents.agent_workflow import AgentWorkflow
        
        csv_content = """value_a,value_b,description
100,50,First entry
200,75,Second entry  
150,25,Third entry
300,100,Fourth entry
50,200,Fifth entry"""
        
        print("📄 Running AI agent workflow on sample CSV data...")
        print("🔒 Using RISC Zero for deterministic verification...")
        
        workflow = AgentWorkflow()
        results = await workflow.run_csv_analysis_workflow(csv_content, 1000)
        
        print(f"\n🎯 Result: {'✅ SUCCESS' if results['success'] else '❌ FAILED'}")
        print(f"📊 Final Decision: {results['final_decision'].upper()}")
        print(f"🎯 Overall Confidence: {results['overall_confidence']}")
        print(f"📈 Column A Sum: {results['csv_details']['column_a_sum']}")
        print(f"🔐 Cryptographic Proof: {'✅ Valid' if results['verification_guarantees']['cryptographic_proof'] else '❌ Invalid'}")
        
        print("\n🎉 Quick start completed successfully!")
        print("\nTo run the full enhanced demo with all agents:")
        print("   python3 enhanced_ai_demo.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Try running setup first:")
        print("   ./setup_ai_agents.sh")

if __name__ == "__main__":
    asyncio.run(main())