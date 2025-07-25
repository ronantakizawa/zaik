"""
Specialized AI agents for different aspects of the workflow
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json

from .openai_client import OpenAIClient, AgentMessage, AgentResponse

class DataQualityAgent:
    """Specialized agent for data quality assessment"""
    
    def __init__(self):
        self.client = OpenAIClient()
        self.system_prompt = """
        You are a Data Quality Assessment Agent. Your expertise is in:
        1. Detecting data anomalies and outliers
        2. Validating data formats and consistency
        3. Identifying missing or corrupted data
        4. Assessing data reliability for business decisions
        
        Always provide structured analysis with confidence scores.
        """
    
    async def assess_data_quality(self, csv_content: str) -> Dict[str, Any]:
        """Assess the quality of CSV data"""
        
        lines = csv_content.strip().split('\n')
        headers = lines[0].split(',') if lines else []
        data_rows = lines[1:] if len(lines) > 1 else []
        
        prompt = f"""
        Assess the data quality of this CSV:
        
        Headers: {headers}
        Sample rows: {data_rows[:5]}
        Total rows: {len(data_rows)}
        
        Analyze:
        1. Data completeness (missing values)
        2. Data consistency (format variations)
        3. Data validity (reasonable ranges)
        4. Potential outliers or anomalies
        5. Overall data quality score (0-1)
        
        Respond in JSON format with detailed assessment.
        """
        
        messages = [AgentMessage(role="user", content=prompt)]
        response = await self.client.chat_completion(
            messages=messages,
            system_prompt=self.system_prompt,
            temperature=0.1
        )
        
        return {
            "agent": "data_quality",
            "assessment": response.content,
            "confidence": response.confidence,
            "quality_score": self._extract_quality_score(response.content)
        }
    
    def _extract_quality_score(self, content: str) -> float:
        """Extract quality score from response"""
        try:
            if "quality_score" in content.lower():
                # Try to extract numeric score
                import re
                scores = re.findall(r'0\.\d+|1\.0', content)
                if scores:
                    return float(scores[0])
            return 0.8  # Default reasonable score
        except:
            return 0.8

class SecurityAgent:
    """Specialized agent for security assessment"""
    
    def __init__(self):
        self.client = OpenAIClient()
        self.system_prompt = """
        You are a Security Assessment Agent. Your role is to:
        1. Identify potential security risks in data processing
        2. Assess cryptographic proof validity
        3. Evaluate trust boundaries and attack vectors
        4. Recommend security best practices
        
        Focus on the security implications of the computation and verification process.
        """
    
    async def assess_security(self, verification_results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess security aspects of the verification"""
        
        prompt = f"""
        Assess the security of this verification process:
        
        Verification Results:
        - RISC Zero Proof Valid: {verification_results.get('risc0_proof_valid', False)}
        - SNARK Proof Valid: {verification_results.get('snark_proof_valid', False)}  
        - Deterministic Execution: {verification_results.get('deterministic_execution', False)}
        - Business Logic Satisfied: {verification_results.get('business_logic_satisfied', False)}
        
        Analyze:
        1. Cryptographic security guarantees
        2. Potential attack vectors
        3. Trust assumptions and boundaries
        4. Verification completeness
        5. Overall security confidence (0-1)
        
        Provide security assessment and recommendations.
        """
        
        messages = [AgentMessage(role="user", content=prompt)]
        response = await self.client.chat_completion(
            messages=messages,
            system_prompt=self.system_prompt,
            temperature=0.1
        )
        
        return {
            "agent": "security",
            "assessment": response.content,
            "confidence": response.confidence,
            "security_level": self._extract_security_level(response.content)
        }
    
    def _extract_security_level(self, content: str) -> str:
        """Extract security level from response"""
        content_lower = content.lower()
        if "high" in content_lower and "security" in content_lower:
            return "high"
        elif "medium" in content_lower or "moderate" in content_lower:
            return "medium"
        elif "low" in content_lower:
            return "low"
        return "medium"  # Default

class BusinessLogicAgent:
    """Specialized agent for business logic validation"""
    
    def __init__(self):
        self.client = OpenAIClient()
        self.system_prompt = """
        You are a Business Logic Validation Agent. Your expertise is in:
        1. Validating business rules and constraints
        2. Assessing compliance with business requirements
        3. Identifying edge cases and exceptions
        4. Recommending business process improvements
        
        Focus on the business implications and rule compliance.
        """
    
    async def validate_business_logic(
        self, 
        csv_details: Dict[str, Any], 
        business_rules: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate business logic compliance"""
        
        prompt = f"""
        Validate business logic compliance:
        
        CSV Processing Results:
        - Column A Sum: {csv_details.get('column_a_sum', 0)}
        - Entry Count: {csv_details.get('entry_count', 0)}
        - Data Hash: {csv_details.get('hash', '')[:32]}...
        
        Business Rules:
        - Threshold: {business_rules.get('threshold', 1000)}
        - Required Compliance: Sum must be <= threshold
        
        Analyze:
        1. Rule compliance status
        2. Business risk assessment
        3. Edge case considerations
        4. Process optimization opportunities
        5. Compliance confidence (0-1)
        
        Provide business validation assessment.
        """
        
        messages = [AgentMessage(role="user", content=prompt)]
        response = await self.client.chat_completion(
            messages=messages,
            system_prompt=self.system_prompt,
            temperature=0.1
        )
        
        return {
            "agent": "business_logic",
            "assessment": response.content,
            "confidence": response.confidence,
            "compliance_status": "pass" if csv_details.get('column_a_sum', 0) <= business_rules.get('threshold', 1000) else "fail"
        }

class RiskAssessmentAgent:
    """Specialized agent for comprehensive risk assessment"""
    
    def __init__(self):
        self.client = OpenAIClient()
        self.system_prompt = """
        You are a Risk Assessment Agent. Your role is to:
        1. Analyze overall system and process risks
        2. Evaluate the impact of potential failures
        3. Assess mitigation strategies
        4. Provide risk ratings and recommendations
        
        Consider technical, business, and operational risks holistically.
        """
    
    async def assess_risks(
        self,
        workflow_results: Dict[str, Any],
        verification_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Comprehensive risk assessment"""
        
        prompt = f"""
        Perform comprehensive risk assessment:
        
        Workflow Status:
        - Overall Success: {workflow_results.get('success', False)}
        - Agent Consensus: {workflow_results.get('final_decision', 'unknown')}
        - Overall Confidence: {workflow_results.get('overall_confidence', 0)}
        
        Technical Verification:
        - Cryptographic Proofs: {verification_results.get('cryptographic_proof', False)}
        - Deterministic Execution: {verification_results.get('deterministic_execution', False)}
        - Business Compliance: {verification_results.get('business_logic_compliance', False)}
        
        Assess:
        1. Technical risks (proof validity, execution correctness)
        2. Business risks (compliance failures, financial impact)
        3. Operational risks (system failures, human errors)
        4. Mitigation strategies
        5. Overall risk level (low/medium/high)
        
        Provide comprehensive risk analysis.
        """
        
        messages = [AgentMessage(role="user", content=prompt)]
        response = await self.client.chat_completion(
            messages=messages,
            system_prompt=self.system_prompt,
            temperature=0.1
        )
        
        return {
            "agent": "risk_assessment",
            "assessment": response.content,
            "confidence": response.confidence,
            "risk_level": self._extract_risk_level(response.content),
            "mitigation_required": self._requires_mitigation(response.content)
        }
    
    def _extract_risk_level(self, content: str) -> str:
        """Extract risk level from response"""
        content_lower = content.lower()
        if "high risk" in content_lower or "high" in content_lower:
            return "high"
        elif "medium risk" in content_lower or "medium" in content_lower:
            return "medium"
        elif "low risk" in content_lower or "low" in content_lower:
            return "low"
        return "medium"  # Default
    
    def _requires_mitigation(self, content: str) -> bool:
        """Determine if mitigation is required"""
        content_lower = content.lower()
        mitigation_keywords = ["mitigation", "action required", "immediate attention", "high risk"]
        return any(keyword in content_lower for keyword in mitigation_keywords)