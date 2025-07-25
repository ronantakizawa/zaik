#!/usr/bin/env python3
"""
AI Agent Workflow Demo with RISC Zero Deterministic Verification

This script demonstrates a complete AI agent workflow that:
1. Uses OpenAI GPT-4 agents to analyze CSV data
2. Leverages RISC Zero zkVM for deterministic verification
3. Orchestrates multiple agents with cryptographic guarantees
"""

import asyncio
import json
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.json import JSON

# Add the ai_agents module to path
sys.path.append(str(Path(__file__).parent))

from ai_agents.agent_workflow import AgentWorkflow

console = Console()

def load_test_csv(filename: str) -> str:
    """Load test CSV data"""
    csv_path = Path(__file__).parent / filename
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    return csv_path.read_text()

def display_workflow_results(results: dict):
    """Display workflow results in a nice format"""
    
    # Main result panel
    status = "✅ SUCCESS" if results["success"] else "❌ FAILED"
    decision = results["final_decision"].upper()
    confidence = results["overall_confidence"] or "N/A"
    
    console.print(Panel(
        f"[bold green]{status}[/bold green]\n"
        f"Final Decision: [bold]{decision}[/bold]\n"
        f"Overall Confidence: [bold]{confidence}[/bold]",
        title="🎯 Workflow Result",
        border_style="green" if results["success"] else "red"
    ))
    
    # Agent Results Table
    table = Table(title="🤖 Agent Results")
    table.add_column("Agent", style="cyan", no_wrap=True)
    table.add_column("Result", style="magenta")
    table.add_column("Confidence", style="green")
    
    agent_results = results["agent_results"]
    
    table.add_row(
        "CSV Analyzer",
        agent_results["csv_analyzer"]["analysis"][:50] + "...",
        str(agent_results["csv_analyzer"]["confidence"])
    )
    
    table.add_row(
        "RISC Zero Verifier", 
        "VERIFIED" if agent_results["risc0_verifier"]["verification_successful"] else "FAILED",
        "1.0" if agent_results["risc0_verifier"]["deterministic_proof"] else "0.0"
    )
    
    table.add_row(
        "Verification Agent",
        agent_results["verification_agent"]["recommendation"].upper(),
        str(agent_results["verification_agent"]["confidence"])
    )
    
    table.add_row(
        "Orchestrator",
        agent_results["orchestrator"]["decision"].upper(),
        str(results["overall_confidence"])
    )
    
    console.print(table)
    
    # Verification Guarantees
    guarantees = results["verification_guarantees"]
    guarantee_table = Table(title="🔒 Verification Guarantees")
    guarantee_table.add_column("Property", style="cyan")
    guarantee_table.add_column("Status", style="green")
    
    guarantee_table.add_row("Deterministic Execution", "✅" if guarantees["deterministic_execution"] else "❌")
    guarantee_table.add_row("Cryptographic Proof", "✅" if guarantees["cryptographic_proof"] else "❌") 
    guarantee_table.add_row("Business Logic Compliance", "✅" if guarantees["business_logic_compliance"] else "❌")
    guarantee_table.add_row("SNARK Proof Valid", "✅" if guarantees["snark_proof_valid"] else "❌")
    
    console.print(guarantee_table)
    
    # CSV Details
    csv_details = results["csv_details"]
    console.print(Panel(
        f"Hash: {csv_details['hash'][:32]}...\n"
        f"Column A Sum: {csv_details['column_a_sum']}\n"
        f"Entry Count: {csv_details['entry_count']}\n"
        f"Column A Hash: {csv_details['column_a_hash'][:32]}...",
        title="📊 CSV Processing Details"
    ))

async def run_demo_workflow(csv_filename: str, threshold: int = 1000):
    """Run the complete AI agent workflow demo"""
    
    console.print(Panel(
        "[bold blue]AI Agent Workflow with RISC Zero Verification[/bold blue]\n\n"
        f"📁 CSV File: {csv_filename}\n"
        f"🎯 Business Threshold: {threshold}\n"
        f"🤖 Agents: CSV Analyzer, RISC Zero Verifier, Verification Agent, Orchestrator\n"
        f"🔒 Guarantees: Deterministic execution, Cryptographic proofs, Business logic compliance",
        title="🚀 Demo Starting"
    ))
    
    try:
        # Load CSV data
        csv_content = load_test_csv(csv_filename)
        console.print(f"📄 Loaded CSV data ({len(csv_content)} bytes)")
        
        # Initialize workflow
        workflow = AgentWorkflow()
        
        # Run the workflow with progress indication
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Running AI agent workflow...", total=None)
            results = await workflow.run_csv_analysis_workflow(csv_content, threshold)
            progress.update(task, completed=True)
        
        # Display results
        display_workflow_results(results)
        
        # Show execution metadata
        metadata = results["workflow_metadata"]
        console.print(Panel(
            f"Workflow ID: {results['workflow_id']}\n"
            f"Total Steps: {metadata['total_steps']}\n"
            f"Execution Time: {metadata['execution_time']:.2f}s\n"
            f"Agents Involved: {', '.join(metadata['agents_involved'])}",
            title="📋 Execution Metadata"
        ))
        
        return results
        
    except Exception as e:
        console.print(Panel(
            f"[bold red]Error: {str(e)}[/bold red]",
            title="❌ Demo Failed",
            border_style="red"
        ))
        return None

async def main():
    """Main demo function"""
    console.print("[bold cyan]🤖 AI Agent Workflow Demo with RISC Zero[/bold cyan]\n")
    
    # Demo 1: Test with good CSV data (should pass)
    console.print("[bold yellow]Demo 1: Testing with good CSV data (sum should pass threshold)[/bold yellow]")
    await run_demo_workflow("test_data.csv", threshold=1000)
    
    console.print("\n" + "="*80 + "\n")
    
    # Demo 2: Test with CSV data that exceeds threshold (should fail business logic)
    console.print("[bold yellow]Demo 2: Testing with CSV data that exceeds threshold[/bold yellow]")
    await run_demo_workflow("test_data_large.csv", threshold=1000)
    
    console.print("\n🎉 [bold green]Demo completed![/bold green]")
    console.print("\n[italic]This demo showcased:[/italic]")
    console.print("• [green]Multi-agent AI workflow coordination[/green]")
    console.print("• [green]RISC Zero deterministic verification[/green]") 
    console.print("• [green]Cryptographic proof generation and validation[/green]")
    console.print("• [green]Business logic compliance checking[/green]")
    console.print("• [green]End-to-end trustless computation[/green]")

if __name__ == "__main__":
    asyncio.run(main())