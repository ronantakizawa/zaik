"""
OpenAI API client for AI agent workflows
"""
import os
import asyncio
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel
import json

load_dotenv()

class AgentMessage(BaseModel):
    role: str
    content: str
    metadata: Optional[Dict[str, Any]] = None

class AgentResponse(BaseModel):
    content: str
    reasoning: Optional[str] = None
    confidence: Optional[float] = None
    next_actions: Optional[List[str]] = None

class OpenAIClient:
    def __init__(self, model: str = "gpt-4-turbo-preview"):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        
    async def chat_completion(
        self, 
        messages: List[AgentMessage], 
        system_prompt: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 2000
    ) -> AgentResponse:
        """Generate a chat completion with structured response"""
        
        # Build messages array
        openai_messages = []
        
        if system_prompt:
            openai_messages.append({"role": "system", "content": system_prompt})
            
        for msg in messages:
            openai_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            content = response.choices[0].message.content
            
            # Try to parse structured response
            try:
                if content.startswith("{") and content.endswith("}"):
                    parsed = json.loads(content)
                    return AgentResponse(
                        content=parsed.get("content", content),
                        reasoning=parsed.get("reasoning"),
                        confidence=parsed.get("confidence"),
                        next_actions=parsed.get("next_actions", [])
                    )
            except json.JSONDecodeError:
                pass
                
            return AgentResponse(content=content)
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def function_call(
        self,
        messages: List[AgentMessage],
        functions: List[Dict[str, Any]],
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Make a function call using OpenAI's function calling"""
        
        openai_messages = []
        
        if system_prompt:
            openai_messages.append({"role": "system", "content": system_prompt})
            
        for msg in messages:
            openai_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                functions=functions,
                function_call="auto"
            )
            
            message = response.choices[0].message
            
            if message.function_call:
                return {
                    "function_name": message.function_call.name,
                    "arguments": json.loads(message.function_call.arguments),
                    "content": message.content
                }
            else:
                return {
                    "function_name": None,
                    "arguments": {},
                    "content": message.content
                }
                
        except Exception as e:
            raise Exception(f"OpenAI function call error: {str(e)}")

class AgentPrompts:
    """Predefined prompts for different agent roles"""
    
    CSV_ANALYZER = """
    You are a CSV Data Analyzer Agent. Your role is to:
    1. Analyze CSV data structure and content
    2. Identify column types and data patterns
    3. Suggest processing strategies
    4. Flag potential data quality issues
    
    Always respond in JSON format:
    {
        "content": "Your analysis",
        "reasoning": "Why you made these decisions",
        "confidence": 0.95,
        "next_actions": ["action1", "action2"]
    }
    """
    
    VERIFICATION_AGENT = """
    You are a Verification Agent. Your role is to:
    1. Review computational results
    2. Validate business logic compliance
    3. Assess proof quality and correctness
    4. Make accept/reject decisions
    
    Always respond in JSON format:
    {
        "content": "Your verification result",
        "reasoning": "Why you accept/reject",
        "confidence": 0.95,
        "next_actions": ["action1", "action2"]
    }
    """
    
    ORCHESTRATOR = """
    You are an Orchestrator Agent. Your role is to:
    1. Coordinate between different agents
    2. Make workflow decisions
    3. Handle error recovery
    4. Optimize processing pipeline
    
    Always respond in JSON format:
    {
        "content": "Your orchestration decision",
        "reasoning": "Why you made this decision",
        "confidence": 0.95,
        "next_actions": ["action1", "action2"]
    }
    """