"""
Enhanced AI Agent Workflow with Specialized Agents
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime

from .agent_workflow import AgentWorkflow
from .specialized_agents import (
    DataQualityAgent, 
    SecurityAgent, 
    BusinessLogicAgent, 
    RiskAssessmentAgent
)

class EnhancedAgentWorkflow(AgentWorkflow):
    """Enhanced workflow with specialized agents"""
    
    def __init__(self):
        super().__init__()
        self.data_quality_agent = DataQualityAgent()
        self.security_agent = SecurityAgent()
        self.business_logic_agent = BusinessLogicAgent()
        self.risk_assessment_agent = RiskAssessmentAgent()
    
    async def run_enhanced_csv_workflow(
        self, 
        csv_content: str, 
        business_threshold: int = 1000,
        enable_all_agents: bool = True
    ) -> Dict[str, Any]:
        """
        Enhanced workflow with specialized agents
        
        Workflow Steps:
        1. Data Quality Assessment
        2. CSV Analysis (original)
        3. RISC Zero Verification
        4. Security Assessment  
        5. Business Logic Validation
        6. Verification Agent Review
        7. Risk Assessment
        8. Orchestrator Final Decision
        """
        
        workflow_id = f"enhanced_workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"🚀 Starting Enhanced AI Agent Workflow: {workflow_id}")
        print("=" * 60)
        
        try:
            results = {}
            
            # Step 1: Data Quality Assessment
            if enable_all_agents:
                print("🔍 Step 1: Data Quality Assessment")
                data_quality_result = await self.data_quality_agent.assess_data_quality(csv_content)
                results["data_quality"] = data_quality_result
                self._record_workflow_step("data_quality_assessment", data_quality_result, ["data_quality_agent"])
                print(f"   📊 Quality Score: {data_quality_result['quality_score']}")
            
            # Step 2: CSV Analysis (from base workflow)
            print("🤖 Step 2: CSV Analysis")
            analysis_result = await self._csv_analysis_step(csv_content)
            results["csv_analysis"] = analysis_result
            
            # Step 3: RISC Zero Verification
            print("🔒 Step 3: RISC Zero Verification")
            verification_result = await self._risc0_verification_step(csv_content, business_threshold)
            results["risc0_verification"] = verification_result
            
            # Step 4: Security Assessment
            if enable_all_agents:
                print("🛡️  Step 4: Security Assessment")
                security_result = await self.security_agent.assess_security(
                    verification_result["verification_report"]["verification_guarantees"]
                    if "verification_guarantees" in verification_result.get("verification_report", {})
                    else verification_result["verification_report"]
                )
                results["security"] = security_result
                self._record_workflow_step("security_assessment", security_result, ["security_agent"])
                print(f"   🔐 Security Level: {security_result['security_level']}")
            
            # Step 5: Business Logic Validation
            if enable_all_agents:
                print("💼 Step 5: Business Logic Validation")
                business_logic_result = await self.business_logic_agent.validate_business_logic(
                    verification_result["verification_report"]["csv_details"],
                    {"threshold": business_threshold}
                )
                results["business_logic"] = business_logic_result
                self._record_workflow_step("business_logic_validation", business_logic_result, ["business_logic_agent"])
                print(f"   ✅ Compliance: {business_logic_result['compliance_status']}")
            
            # Step 6: Verification Agent Review (from base workflow)
            print("🔍 Step 6: Verification Agent Review")
            verification_review = await self._verification_agent_step(analysis_result, verification_result)
            results["verification_review"] = verification_review
            
            # Step 7: Risk Assessment
            if enable_all_agents:
                print("⚠️  Step 7: Risk Assessment")
                risk_result = await self.risk_assessment_agent.assess_risks(
                    {"success": verification_result["verification_report"]["verification_successful"]},
                    verification_result["verification_report"].get("verification_guarantees", {})
                )
                results["risk_assessment"] = risk_result
                self._record_workflow_step("risk_assessment", risk_result, ["risk_assessment_agent"])
                print(f"   ⚠️  Risk Level: {risk_result['risk_level']}")
            
            # Step 8: Enhanced Orchestrator Decision
            print("🎯 Step 8: Enhanced Orchestrator Decision")
            final_decision = await self._enhanced_orchestrator_decision(results)
            results["final_decision"] = final_decision
            
            # Compile enhanced final report
            return self._compile_enhanced_report(workflow_id, results)
            
        except Exception as e:
            error_result = {"error": str(e), "step_failed": "enhanced_workflow"}
            self._record_workflow_step("error", error_result, ["system"])
            return {"success": False, "error": str(e), "workflow_id": workflow_id}
    
    async def _enhanced_orchestrator_decision(self, all_results: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced orchestrator decision with all agent inputs"""
        
        # Extract key metrics from all agents
        data_quality_score = all_results.get("data_quality", {}).get("quality_score", 0.8)
        security_level = all_results.get("security", {}).get("security_level", "medium")
        business_compliance = all_results.get("business_logic", {}).get("compliance_status", "unknown")
        risk_level = all_results.get("risk_assessment", {}).get("risk_level", "medium")
        
        verification_success = all_results["risc0_verification"]["verification_report"]["verification_successful"]
        verification_agent_rec = all_results["verification_review"]["recommendation"]
        
        decision_prompt = f"""
        Make an enhanced final decision based on comprehensive agent analysis:
        
        Agent Results Summary:
        - Data Quality Score: {data_quality_score} 
        - RISC Zero Verification: {verification_success}
        - Security Level: {security_level}
        - Business Compliance: {business_compliance}
        - Risk Level: {risk_level}
        - Verification Agent Recommendation: {verification_agent_rec}
        
        Key Factors:
        - All cryptographic proofs valid: {verification_success}
        - Multi-agent consensus achieved: {len([r for r in all_results.values() if isinstance(r, dict) and r.get("confidence", 0) > 0.7])} agents confident
        - Risk mitigation required: {all_results.get("risk_assessment", {}).get("mitigation_required", False)}
        
        Provide final orchestrator decision considering all specialized agent inputs.
        Include overall confidence and key decision factors.
        """
        
        from .openai_client import AgentMessage, AgentPrompts
        messages = [AgentMessage(role="user", content=decision_prompt)]
        response = await self.openai_client.chat_completion(
            messages=messages,
            system_prompt=AgentPrompts.ORCHESTRATOR,
            temperature=0.1
        )
        
        # Enhanced decision logic
        decision_factors = {
            "data_quality_acceptable": data_quality_score >= 0.7,
            "security_adequate": security_level in ["high", "medium"],
            "business_compliant": business_compliance == "pass",
            "risk_manageable": risk_level in ["low", "medium"],
            "verification_passed": verification_success,
            "agent_consensus": verification_agent_rec == "accept"
        }
        
        # All critical factors must pass
        critical_pass = all([
            decision_factors["verification_passed"],
            decision_factors["business_compliant"],
            decision_factors["agent_consensus"]
        ])
        
        # Risk factors should be acceptable
        risk_acceptable = decision_factors["risk_manageable"] and decision_factors["security_adequate"]
        
        final_accept = critical_pass and risk_acceptable
        
        print(f"   🎯 Enhanced Decision: {'ACCEPT' if final_accept else 'REJECT'}")
        print(f"   📊 Decision Confidence: {response.confidence}")
        print(f"   ⚖️  Critical Factors Pass: {critical_pass}")
        print(f"   🛡️  Risk Acceptable: {risk_acceptable}")
        
        return {
            "agent": "enhanced_orchestrator",
            "decision": "accept" if final_accept else "reject",
            "reasoning": response.content,
            "overall_confidence": response.confidence,
            "decision_factors": decision_factors,
            "critical_factors_pass": critical_pass,
            "risk_acceptable": risk_acceptable,
            "enhanced_analysis": True
        }
    
    def _compile_enhanced_report(self, workflow_id: str, all_results: Dict[str, Any]) -> Dict[str, Any]:
        """Compile comprehensive enhanced report"""
        
        base_report = {
            "workflow_id": workflow_id,
            "workflow_type": "enhanced_multi_agent",
            "success": all_results["final_decision"]["decision"] == "accept",
            "final_decision": all_results["final_decision"]["decision"],
            "overall_confidence": all_results["final_decision"]["overall_confidence"],
            "enhanced_analysis": True
        }
        
        # Enhanced agent results
        base_report["agent_results"] = {
            "data_quality_agent": {
                "quality_score": all_results.get("data_quality", {}).get("quality_score", "N/A"),
                "confidence": all_results.get("data_quality", {}).get("confidence", "N/A")
            } if "data_quality" in all_results else {"status": "not_run"},
            
            "csv_analyzer": {
                "analysis": all_results["csv_analysis"]["analysis"],
                "confidence": all_results["csv_analysis"]["confidence"]
            },
            
            "risc0_verifier": {
                "verification_successful": all_results["risc0_verification"]["verification_report"]["verification_successful"],
                "deterministic_proof": all_results["risc0_verification"]["deterministic_proof"],
                "business_compliance": all_results["risc0_verification"]["business_compliance"],
                "column_a_sum": all_results["risc0_verification"]["verification_report"]["csv_details"]["column_a_sum"]
            },
            
            "security_agent": {
                "security_level": all_results.get("security", {}).get("security_level", "N/A"),
                "confidence": all_results.get("security", {}).get("confidence", "N/A")
            } if "security" in all_results else {"status": "not_run"},
            
            "business_logic_agent": {
                "compliance_status": all_results.get("business_logic", {}).get("compliance_status", "N/A"),
                "confidence": all_results.get("business_logic", {}).get("confidence", "N/A")
            } if "business_logic" in all_results else {"status": "not_run"},
            
            "verification_agent": {
                "recommendation": all_results["verification_review"]["recommendation"],
                "confidence": all_results["verification_review"]["confidence"]
            },
            
            "risk_assessment_agent": {
                "risk_level": all_results.get("risk_assessment", {}).get("risk_level", "N/A"),
                "mitigation_required": all_results.get("risk_assessment", {}).get("mitigation_required", "N/A"),
                "confidence": all_results.get("risk_assessment", {}).get("confidence", "N/A")
            } if "risk_assessment" in all_results else {"status": "not_run"},
            
            "enhanced_orchestrator": {
                "decision": all_results["final_decision"]["decision"],
                "critical_factors_pass": all_results["final_decision"]["critical_factors_pass"],
                "risk_acceptable": all_results["final_decision"]["risk_acceptable"]
            }
        }
        
        # Enhanced verification guarantees
        base_report["verification_guarantees"] = all_results["risc0_verification"]["verification_report"].get("verification_guarantees", {})
        
        # Enhanced metadata
        base_report["workflow_metadata"] = {
            "total_steps": len(self.workflow_history),
            "agents_involved": [
                "data_quality_agent", "csv_analyzer", "risc0_verifier", 
                "security_agent", "business_logic_agent", "verification_agent",
                "risk_assessment_agent", "enhanced_orchestrator"
            ],
            "specialized_agents_count": len([r for r in all_results.values() if isinstance(r, dict) and "agent" in r]),
            "execution_time": (datetime.now() - self.workflow_history[0].timestamp).total_seconds() if self.workflow_history else 0
        }
        
        # CSV details
        base_report["csv_details"] = all_results["risc0_verification"]["verification_report"]["csv_details"]
        
        # Decision analysis
        base_report["decision_analysis"] = all_results["final_decision"].get("decision_factors", {})
        
        return base_report