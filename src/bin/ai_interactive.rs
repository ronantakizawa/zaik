use anyhow::Result;
use dotenv::dotenv;
use std::{env, io::{self, Write}};
use zkvm_verifier::ai_agent::{AIAgent, AgentType};

#[tokio::main]
async fn main() -> Result<()> {
    dotenv().ok();
    
    let api_key = env::var("OPENAI_API_KEY")
        .expect("OPENAI_API_KEY must be set in .env file");

    println!("🤖 Interactive AI Agent for zkVM Testing");
    println!("========================================");
    println!("Available commands:");
    println!("  gen <requirements> - Generate CSV data");
    println!("  analyze <data>     - Analyze verification results");
    println!("  plan <scenario>    - Plan test scenario");
    println!("  quit              - Exit");
    println!();

    let generator = AIAgent::new(api_key.clone(), AgentType::CsvGenerator);
    let verifier = AIAgent::new(api_key.clone(), AgentType::Verifier);
    let orchestrator = AIAgent::new(api_key.clone(), AgentType::Orchestrator);

    loop {
        print!("🤖 > ");
        io::stdout().flush()?;
        
        let mut input = String::new();
        io::stdin().read_line(&mut input)?;
        let input = input.trim();
        
        if input.is_empty() {
            continue;
        }
        
        if input == "quit" {
            println!("👋 Goodbye!");
            break;
        }
        
        let parts: Vec<&str> = input.splitn(2, ' ').collect();
        let command = parts[0];
        let args = parts.get(1).unwrap_or(&"").to_string();
        
        match command {
            "gen" => {
                if args.is_empty() {
                    println!("❌ Please provide CSV requirements");
                    continue;
                }
                
                println!("🏭 Generating CSV data...");
                match generator.generate_csv_data(&args).await {
                    Ok(csv) => {
                        println!("📊 Generated CSV:");
                        println!("{}", csv);
                    }
                    Err(e) => println!("❌ Error: {}", e),
                }
            }
            
            "analyze" => {
                if args.is_empty() {
                    println!("❌ Please provide verification data to analyze");
                    continue;
                }
                
                println!("🔍 Analyzing verification results...");
                match verifier.analyze_verification_result(&args, true).await {
                    Ok(decision) => {
                        println!("🎯 Analysis Result:");
                        println!("   Action: {}", decision.action);
                        println!("   Confidence: {:.2}", decision.confidence);
                        println!("   Reasoning: {}", decision.reasoning);
                    }
                    Err(e) => println!("❌ Error: {}", e),
                }
            }
            
            "plan" => {
                if args.is_empty() {
                    println!("❌ Please provide test scenario");
                    continue;
                }
                
                println!("🧠 Planning test scenario...");
                match orchestrator.orchestrate_test_scenario(&args).await {
                    Ok(plan) => {
                        println!("📋 Test Plan:");
                        println!("{}", plan);
                    }
                    Err(e) => println!("❌ Error: {}", e),
                }
            }
            
            _ => {
                println!("❌ Unknown command: {}", command);
                println!("Available: gen, analyze, plan, quit");
            }
        }
        
        println!();
    }
    
    Ok(())
}