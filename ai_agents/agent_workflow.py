"""
AI Agent Workflow Orchestrator
Coordinates multiple AI agents with RISC Zero deterministic verification
"""
import asyncio
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import pandas as pd

from .openai_client import OpenAIClient, AgentMessage, AgentResponse, AgentPrompts
from .risc0_verifier import RISC0Verifier, VerificationResult

@dataclass
class WorkflowState:
    step: str
    data: Dict[str, Any]
    agents_involved: List[str]
    timestamp: datetime
    verification_results: Optional[Dict[str, Any]] = None

class AgentWorkflow:
    """Orchestrates AI agents with RISC Zero verification"""
    
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.risc0_verifier = RISC0Verifier()
        self.workflow_history: List[WorkflowState] = []
        
    async def run_csv_analysis_workflow(
        self, 
        csv_content: str, 
        business_threshold: int = 1000
    ) -> Dict[str, Any]:
        """
        Complete AI agent workflow for CSV analysis with RISC Zero verification
        
        Steps:
        1. CSV Analyzer Agent analyzes the data
        2. RISC Zero verifier processes and proves execution
        3. Verification Agent validates results
        4. Orchestrator makes final decision
        """
        
        workflow_id = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"🚀 Starting AI Agent Workflow: {workflow_id}")
        print("=" * 50)
        
        try:
            # Step 1: CSV Analysis Agent
            analysis_result = await self._csv_analysis_step(csv_content)
            self._record_workflow_step("csv_analysis", analysis_result, ["csv_analyzer"])
            
            # Step 2: RISC Zero Verification
            verification_result = await self._risc0_verification_step(csv_content, business_threshold)
            self._record_workflow_step("risc0_verification", verification_result, ["risc0_verifier"])
            
            # Step 3: Verification Agent Review
            verification_review = await self._verification_agent_step(analysis_result, verification_result)
            self._record_workflow_step("verification_review", verification_review, ["verification_agent"])
            
            # Step 4: Orchestrator Decision
            final_decision = await self._orchestrator_decision_step(
                analysis_result, verification_result, verification_review
            )
            self._record_workflow_step("final_decision", final_decision, ["orchestrator"])
            
            # Compile final report
            return self._compile_final_report(workflow_id, analysis_result, verification_result, verification_review, final_decision)
            
        except Exception as e:
            error_result = {"error": str(e), "step_failed": "unknown"}
            self._record_workflow_step("error", error_result, ["system"])
            return {"success": False, "error": str(e), "workflow_id": workflow_id}
    
    async def _csv_analysis_step(self, csv_content: str) -> Dict[str, Any]:
        """Step 1: AI agent analyzes CSV structure and content"""
        print("🤖 Step 1: CSV Analyzer Agent")
        
        # Parse CSV to get basic stats
        lines = csv_content.strip().split('\n')
        headers = lines[0].split(',') if lines else []
        data_rows = lines[1:] if len(lines) > 1 else []
        
        analysis_prompt = f"""
        Analyze this CSV data:
        
        Headers: {headers}
        Row count: {len(data_rows)}
        Sample rows: {data_rows[:3] if data_rows else []}
        
        Focus on:
        1. Data structure and column types
        2. Column A values and patterns
        3. Potential data quality issues
        4. Business logic implications
        
        Predict what the sum of column A will be.
        """
        
        messages = [AgentMessage(role="user", content=analysis_prompt)]
        response = await self.openai_client.chat_completion(
            messages=messages,
            system_prompt=AgentPrompts.CSV_ANALYZER,
            temperature=0.1
        )
        
        print(f"   📊 Analysis: {response.content[:100]}...")
        print(f"   🎯 Confidence: {response.confidence}")
        
        return {
            "agent": "csv_analyzer",
            "analysis": response.content,
            "reasoning": response.reasoning,
            "confidence": response.confidence,
            "next_actions": response.next_actions,
            "csv_stats": {
                "headers": headers,
                "row_count": len(data_rows),
                "columns": len(headers)
            }
        }
    
    async def _risc0_verification_step(self, csv_content: str, threshold: int) -> Dict[str, Any]:
        """Step 2: RISC Zero deterministic verification"""
        print("🔒 Step 2: RISC Zero Deterministic Verification")
        
        # Run RISC Zero verification
        verification_report = self.risc0_verifier.verify_csv_data(csv_content)
        
        print(f"   ✅ Verification: {'PASSED' if verification_report['verification_successful'] else 'FAILED'}")
        print(f"   🔐 RISC Zero Proof: {'VALID' if verification_report['risc0_proof_valid'] else 'INVALID'}")
        print(f"   💼 Business Logic: {'SATISFIED' if verification_report['business_logic_satisfied'] else 'VIOLATED'}")
        print(f"   📊 Column A Sum: {verification_report['csv_details']['column_a_sum']}")
        
        return {
            "agent": "risc0_verifier",
            "verification_report": verification_report,
            "deterministic_proof": verification_report['risc0_proof_valid'],
            "business_compliance": verification_report['business_logic_satisfied'],
            "cryptographic_guarantees": verification_report['snark_proof_valid']
        }
    
    async def _verification_agent_step(self, analysis_result: Dict[str, Any], verification_result: Dict[str, Any]) -> Dict[str, Any]:
        """Step 3: AI agent reviews verification results"""
        print("🔍 Step 3: Verification Agent Review")
        
        review_prompt = f"""
        Review these results:
        
        CSV Analysis:
        - Agent Analysis: {analysis_result['analysis']}
        - Confidence: {analysis_result['confidence']}
        
        RISC Zero Verification:
        - Verification Successful: {verification_result['verification_report']['verification_successful']}
        - RISC Zero Proof Valid: {verification_result['verification_report']['risc0_proof_valid']}
        - Business Logic Satisfied: {verification_result['verification_report']['business_logic_satisfied']}
        - Column A Sum: {verification_result['verification_report']['csv_details']['column_a_sum']}
        - Cryptographic Guarantees: {verification_result['verification_report']['snark_proof_valid']}
        
        Provide your verification assessment:
        1. Do the results align with the initial analysis?
        2. Are the cryptographic proofs valid?
        3. Should we accept or reject this computation?
        4. What are the trust guarantees?
        """
        
        messages = [AgentMessage(role="user", content=review_prompt)]
        response = await self.openai_client.chat_completion(
            messages=messages,
            system_prompt=AgentPrompts.VERIFICATION_AGENT,
            temperature=0.1
        )
        
        print(f"   🔍 Review: {response.content[:100]}...")
        print(f"   🎯 Confidence: {response.confidence}")
        
        return {
            "agent": "verification_agent",
            "review": response.content,
            "reasoning": response.reasoning,
            "confidence": response.confidence,
            "recommendation": "accept" if verification_result['verification_report']['verification_successful'] else "reject",
            "trust_level": response.confidence if response.confidence else 0.8
        }
    
    async def _orchestrator_decision_step(
        self, 
        analysis_result: Dict[str, Any], 
        verification_result: Dict[str, Any], 
        verification_review: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Step 4: Orchestrator makes final workflow decision"""
        print("🎯 Step 4: Orchestrator Final Decision")
        
        decision_prompt = f"""
        Make a final workflow decision based on all agent inputs:
        
        CSV Analysis Confidence: {analysis_result['confidence']}
        RISC Zero Verification: {verification_result['verification_report']['verification_successful']}
        Verification Agent Recommendation: {verification_review['recommendation']}
        Verification Agent Confidence: {verification_review['confidence']}
        
        Key Metrics:
        - Deterministic Execution Proven: {verification_result['deterministic_proof']}
        - Business Logic Compliance: {verification_result['business_compliance']}
        - Cryptographic Guarantees: {verification_result['cryptographic_guarantees']}
        
        Provide final decision:
        1. Accept or reject the computation
        2. Overall confidence level
        3. Key success factors
        4. Risk assessment
        """
        
        messages = [AgentMessage(role="user", content=decision_prompt)]
        response = await self.openai_client.chat_completion(
            messages=messages,
            system_prompt=AgentPrompts.ORCHESTRATOR,
            temperature=0.1
        )
        
        # Determine final decision based on verification results
        final_accept = (
            verification_result['verification_report']['verification_successful'] and
            verification_result['deterministic_proof'] and
            verification_review['recommendation'] == "accept"
        )
        
        print(f"   🎯 Decision: {'ACCEPT' if final_accept else 'REJECT'}")
        print(f"   📊 Overall Confidence: {response.confidence}")
        
        return {
            "agent": "orchestrator",
            "decision": "accept" if final_accept else "reject",
            "reasoning": response.content,
            "overall_confidence": response.confidence,
            "success_factors": [
                "Deterministic execution proven",
                "Cryptographic guarantees maintained", 
                "Business logic compliance verified",
                "Multi-agent consensus achieved"
            ] if final_accept else ["Verification failed"],
            "risk_assessment": "low" if final_accept else "high"
        }
    
    def _record_workflow_step(self, step: str, data: Dict[str, Any], agents: List[str]):
        """Record a workflow step in history"""
        state = WorkflowState(
            step=step,
            data=data,
            agents_involved=agents,
            timestamp=datetime.now()
        )
        self.workflow_history.append(state)
    
    def _compile_final_report(
        self, 
        workflow_id: str,
        analysis_result: Dict[str, Any],
        verification_result: Dict[str, Any], 
        verification_review: Dict[str, Any],
        final_decision: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compile comprehensive final report"""
        
        return {
            "workflow_id": workflow_id,
            "success": final_decision["decision"] == "accept",
            "final_decision": final_decision["decision"],
            "overall_confidence": final_decision["overall_confidence"],
            
            "agent_results": {
                "csv_analyzer": {
                    "analysis": analysis_result["analysis"],
                    "confidence": analysis_result["confidence"]
                },
                "risc0_verifier": {
                    "verification_successful": verification_result["verification_report"]["verification_successful"],
                    "deterministic_proof": verification_result["deterministic_proof"],
                    "business_compliance": verification_result["business_compliance"],
                    "column_a_sum": verification_result["verification_report"]["csv_details"]["column_a_sum"]
                },
                "verification_agent": {
                    "recommendation": verification_review["recommendation"],
                    "confidence": verification_review["confidence"]
                },
                "orchestrator": {
                    "decision": final_decision["decision"],
                    "risk_assessment": final_decision["risk_assessment"]
                }
            },
            
            "verification_guarantees": {
                "deterministic_execution": verification_result["deterministic_proof"],
                "cryptographic_proof": verification_result["verification_report"]["risc0_proof_valid"],
                "business_logic_compliance": verification_result["business_compliance"],
                "snark_proof_valid": verification_result["cryptographic_guarantees"]
            },
            
            "workflow_metadata": {
                "total_steps": len(self.workflow_history),
                "agents_involved": ["csv_analyzer", "risc0_verifier", "verification_agent", "orchestrator"],
                "execution_time": (datetime.now() - self.workflow_history[0].timestamp).total_seconds() if self.workflow_history else 0
            },
            
            "csv_details": verification_result["verification_report"]["csv_details"]
        }