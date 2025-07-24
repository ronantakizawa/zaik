use anyhow::Result;
use chrono::Utc;
use reqwest::Client;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use uuid::Uuid;

#[derive(Debug, Serialize, Deserialize)]
pub struct OpenAIRequest {
    model: String,
    messages: Vec<Message>,
    temperature: f32,
    max_tokens: Option<u32>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Message {
    role: String,
    content: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct OpenAIResponse {
    choices: Vec<Choice>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Choice {
    message: Message,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct AgentDecision {
    pub action: String,
    pub reasoning: String,
    pub confidence: f32,
    pub data: Option<String>,
}

pub struct AIAgent {
    client: Client,
    api_key: String,
    agent_id: String,
    agent_type: AgentType,
}

#[derive(Debug, Clone)]
pub enum AgentType {
    CsvGenerator,
    Verifier,
    Orchestrator,
}

impl AIAgent {
    pub fn new(api_key: String, agent_type: AgentType) -> Self {
        Self {
            client: Client::new(),
            api_key,
            agent_id: Uuid::new_v4().to_string(),
            agent_type,
        }
    }

    pub async fn call_openai(&self, messages: Vec<Message>) -> Result<String> {
        let request = OpenAIRequest {
            model: "gpt-4".to_string(),
            messages,
            temperature: 0.7,
            max_tokens: Some(1500),
        };

        let response = self
            .client
            .post("https://api.openai.com/v1/chat/completions")
            .header("Authorization", format!("Bearer {}", self.api_key))
            .header("Content-Type", "application/json")
            .json(&request)
            .send()
            .await?;

        let openai_response: OpenAIResponse = response.json().await?;
        
        Ok(openai_response
            .choices
            .first()
            .map(|choice| choice.message.content.clone())
            .unwrap_or_else(|| "No response".to_string()))
    }

    pub async fn generate_csv_data(&self, requirements: &str) -> Result<String> {
        let messages = vec![
            Message {
                role: "system".to_string(),
                content: "You are Agent A, a CSV data generator. Generate CSV data based on requirements. Return only the CSV content with headers 'column_a,column_b,column_c' where column_a contains numeric values.".to_string(),
            },
            Message {
                role: "user".to_string(),
                content: format!("Generate CSV data with the following requirements: {}", requirements),
            },
        ];

        self.call_openai(messages).await
    }

    pub async fn analyze_verification_result(&self, zkvm_output: &str, snark_verified: bool) -> Result<AgentDecision> {
        let messages = vec![
            Message {
                role: "system".to_string(),
                content: "You are Agent B, a verification analyst. Analyze zkVM proofs and SNARK verification results. Return a JSON object with fields: action (accept/reject/investigate), reasoning (your analysis), confidence (0.0-1.0), and optional data field.".to_string(),
            },
            Message {
                role: "user".to_string(),
                content: format!(
                    "Analyze this verification result:\nzkVM Output: {}\nSNARK Verified: {}\n\nProvide your decision as JSON.",
                    zkvm_output, snark_verified
                ),
            },
        ];

        let response = self.call_openai(messages).await?;
        
        // Try to parse as JSON, fallback to structured response
        match serde_json::from_str::<AgentDecision>(&response) {
            Ok(decision) => Ok(decision),
            Err(_) => {
                // Fallback parsing
                let action = if response.to_lowercase().contains("accept") {
                    "accept"
                } else if response.to_lowercase().contains("reject") {
                    "reject"
                } else {
                    "investigate"
                };

                Ok(AgentDecision {
                    action: action.to_string(),
                    reasoning: response,
                    confidence: 0.8,
                    data: None,
                })
            }
        }
    }

    pub async fn orchestrate_test_scenario(&self, scenario: &str) -> Result<String> {
        let messages = vec![
            Message {
                role: "system".to_string(),
                content: "You are an AI orchestrator managing a zkVM verification test. Plan the test steps and coordinate between agents. Be specific about CSV requirements and expected outcomes.".to_string(),
            },
            Message {
                role: "user".to_string(),
                content: format!("Plan and execute this test scenario: {}", scenario),
            },
        ];

        self.call_openai(messages).await
    }

    pub fn get_agent_info(&self) -> HashMap<String, String> {
        let mut info = HashMap::new();
        info.insert("agent_id".to_string(), self.agent_id.clone());
        info.insert("agent_type".to_string(), format!("{:?}", self.agent_type));
        info.insert("timestamp".to_string(), Utc::now().to_rfc3339());
        info
    }
}