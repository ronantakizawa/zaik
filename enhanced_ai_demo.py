#!/usr/bin/env python3
"""
Enhanced AI Agent Workflow Demo with Specialized Agents + RISC Zero

This demonstrates a comprehensive multi-agent workflow including:
- Data Quality Assessment Agent  
- CSV Analysis Agent
- RISC Zero Deterministic Verifier
- Security Assessment Agent
- Business Logic Validation Agent
- Verification Review Agent
- Risk Assessment Agent
- Enhanced Orchestrator Agent
"""

import asyncio
import json
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.tree import Tree

# Add the ai_agents module to path
sys.path.append(str(Path(__file__).parent))

from ai_agents.enhanced_workflow import EnhancedAgentWorkflow

console = Console()

def load_test_csv(filename: str) -> str:
    """Load test CSV data"""
    csv_path = Path(__file__).parent / filename
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    return csv_path.read_text()

def display_enhanced_results(results: dict):
    """Display enhanced workflow results"""
    
    # Main result panel
    status = "✅ SUCCESS" if results["success"] else "❌ FAILED"
    decision = results["final_decision"].upper()
    confidence = results["overall_confidence"] or "N/A"
    
    console.print(Panel(
        f"[bold green]{status}[/bold green]\n"
        f"Final Decision: [bold]{decision}[/bold]\n"
        f"Overall Confidence: [bold]{confidence}[/bold]\n"
        f"Enhanced Analysis: [bold]{'✅' if results.get('enhanced_analysis', False) else '❌'}[/bold]",
        title="🎯 Enhanced Workflow Result",
        border_style="green" if results["success"] else "red"
    ))
    
    # Enhanced Agent Results Tree
    tree = Tree("🤖 Multi-Agent Analysis Results")
    
    agent_results = results["agent_results"]
    
    # Data Quality Agent
    if agent_results["data_quality_agent"].get("status") != "not_run":
        quality_branch = tree.add("🔍 Data Quality Agent")
        quality_branch.add(f"Quality Score: {agent_results['data_quality_agent']['quality_score']}")
        quality_branch.add(f"Confidence: {agent_results['data_quality_agent']['confidence']}")
    
    # CSV Analyzer
    csv_branch = tree.add("📊 CSV Analyzer Agent")
    csv_branch.add(f"Analysis: {agent_results['csv_analyzer']['analysis'][:50]}...")
    csv_branch.add(f"Confidence: {agent_results['csv_analyzer']['confidence']}")
    
    # RISC Zero Verifier
    risc0_branch = tree.add("🔒 RISC Zero Verifier")
    risc0_branch.add(f"Verification: {'✅ PASSED' if agent_results['risc0_verifier']['verification_successful'] else '❌ FAILED'}")
    risc0_branch.add(f"Deterministic Proof: {'✅' if agent_results['risc0_verifier']['deterministic_proof'] else '❌'}")
    risc0_branch.add(f"Column A Sum: {agent_results['risc0_verifier']['column_a_sum']}")
    
    # Security Agent
    if agent_results["security_agent"].get("status") != "not_run":
        security_branch = tree.add("🛡️ Security Agent")
        security_branch.add(f"Security Level: {agent_results['security_agent']['security_level']}")
        security_branch.add(f"Confidence: {agent_results['security_agent']['confidence']}")
    
    # Business Logic Agent
    if agent_results["business_logic_agent"].get("status") != "not_run":
        business_branch = tree.add("💼 Business Logic Agent")
        business_branch.add(f"Compliance: {agent_results['business_logic_agent']['compliance_status']}")
        business_branch.add(f"Confidence: {agent_results['business_logic_agent']['confidence']}")
    
    # Verification Agent
    verification_branch = tree.add("🔍 Verification Agent")
    verification_branch.add(f"Recommendation: {agent_results['verification_agent']['recommendation'].upper()}")
    verification_branch.add(f"Confidence: {agent_results['verification_agent']['confidence']}")
    
    # Risk Assessment Agent
    if agent_results["risk_assessment_agent"].get("status") != "not_run":
        risk_branch = tree.add("⚠️ Risk Assessment Agent")
        risk_branch.add(f"Risk Level: {agent_results['risk_assessment_agent']['risk_level']}")
        risk_branch.add(f"Mitigation Required: {agent_results['risk_assessment_agent']['mitigation_required']}")
        risk_branch.add(f"Confidence: {agent_results['risk_assessment_agent']['confidence']}")
    
    # Enhanced Orchestrator
    orchestrator_branch = tree.add("🎯 Enhanced Orchestrator")
    orchestrator_branch.add(f"Decision: {agent_results['enhanced_orchestrator']['decision'].upper()}")
    orchestrator_branch.add(f"Critical Factors: {'✅ PASS' if agent_results['enhanced_orchestrator']['critical_factors_pass'] else '❌ FAIL'}")
    orchestrator_branch.add(f"Risk Acceptable: {'✅' if agent_results['enhanced_orchestrator']['risk_acceptable'] else '❌'}")
    
    console.print(tree)
    
    # Decision Analysis
    if "decision_analysis" in results:
        decision_table = Table(title="⚖️ Decision Factor Analysis")
        decision_table.add_column("Factor", style="cyan")
        decision_table.add_column("Status", style="green")
        
        for factor, status in results["decision_analysis"].items():
            decision_table.add_row(
                factor.replace("_", " ").title(),
                "✅ PASS" if status else "❌ FAIL"
            )
        
        console.print(decision_table)
    
    # Verification Guarantees (same as before)
    guarantees = results["verification_guarantees"]
    guarantee_table = Table(title="🔒 Verification Guarantees")
    guarantee_table.add_column("Property", style="cyan")
    guarantee_table.add_column("Status", style="green")
    
    guarantee_table.add_row("Deterministic Execution", "✅" if guarantees.get("deterministic_execution", False) else "❌")
    guarantee_table.add_row("Cryptographic Proof", "✅" if guarantees.get("cryptographic_proof", False) else "❌") 
    guarantee_table.add_row("Business Logic Compliance", "✅" if guarantees.get("business_logic_compliance", False) else "❌")
    guarantee_table.add_row("SNARK Proof Valid", "✅" if guarantees.get("snark_proof_valid", False) else "❌")
    
    console.print(guarantee_table)
    
    # Enhanced Metadata
    metadata = results["workflow_metadata"]
    console.print(Panel(
        f"Workflow ID: {results['workflow_id']}\n"
        f"Workflow Type: {results['workflow_type']}\n"
        f"Total Steps: {metadata['total_steps']}\n"
        f"Specialized Agents: {metadata['specialized_agents_count']}\n"
        f"Execution Time: {metadata['execution_time']:.2f}s\n"
        f"Agents Involved: {len(metadata['agents_involved'])}",
        title="📋 Enhanced Execution Metadata"
    ))

async def run_enhanced_demo(csv_filename: str, threshold: int = 1000, enable_all_agents: bool = True):
    """Run the enhanced AI agent workflow demo"""
    
    console.print(Panel(
        "[bold blue]Enhanced AI Agent Workflow with RISC Zero Verification[/bold blue]\n\n"
        f"📁 CSV File: {csv_filename}\n"
        f"🎯 Business Threshold: {threshold}\n"
        f"🤖 Specialized Agents: {'Enabled' if enable_all_agents else 'Basic Only'}\n"
        f"🔒 Guarantees: Multi-agent consensus, Cryptographic proofs, Risk assessment\n"
        f"📊 Analysis Depth: Comprehensive security, quality, and business validation",
        title="🚀 Enhanced Demo Starting"
    ))
    
    try:
        # Load CSV data
        csv_content = load_test_csv(csv_filename)
        console.print(f"📄 Loaded CSV data ({len(csv_content)} bytes)")
        
        # Initialize enhanced workflow
        workflow = EnhancedAgentWorkflow()
        
        # Run the enhanced workflow
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Running enhanced multi-agent workflow...", total=None)
            results = await workflow.run_enhanced_csv_workflow(
                csv_content, 
                threshold, 
                enable_all_agents=enable_all_agents
            )
            progress.update(task, completed=True)
        
        # Display results
        display_enhanced_results(results)
        
        return results
        
    except Exception as e:
        console.print(Panel(
            f"[bold red]Error: {str(e)}[/bold red]",
            title="❌ Enhanced Demo Failed",
            border_style="red"
        ))
        return None

async def main():
    """Main enhanced demo function"""
    console.print("[bold cyan]🤖 Enhanced AI Agent Workflow Demo with RISC Zero[/bold cyan]\n")
    
    # Demo 1: Enhanced workflow with all agents (good data)
    console.print("[bold yellow]Demo 1: Full Enhanced Workflow (good data, should pass)[/bold yellow]")
    await run_enhanced_demo("test_data.csv", threshold=1000, enable_all_agents=True)
    
    console.print("\n" + "="*80 + "\n")
    
    # Demo 2: Enhanced workflow with all agents (data exceeds threshold)
    console.print("[bold yellow]Demo 2: Full Enhanced Workflow (exceeds threshold, should fail)[/bold yellow]")
    await run_enhanced_demo("test_data_large.csv", threshold=1000, enable_all_agents=True)
    
    console.print("\n" + "="*80 + "\n")
    
    # Demo 3: Basic workflow for comparison
    console.print("[bold yellow]Demo 3: Basic Workflow (for comparison)[/bold yellow]")
    await run_enhanced_demo("test_data.csv", threshold=1000, enable_all_agents=False)
    
    console.print("\n🎉 [bold green]Enhanced Demo completed![/bold green]")
    console.print("\n[italic]This enhanced demo showcased:[/italic]")
    console.print("• [green]Multi-layered AI agent analysis[/green]")
    console.print("• [green]Data quality assessment[/green]")
    console.print("• [green]Security and risk evaluation[/green]")
    console.print("• [green]Business logic validation[/green]")
    console.print("• [green]RISC Zero deterministic verification[/green]") 
    console.print("• [green]Comprehensive decision factor analysis[/green]")
    console.print("• [green]Enhanced orchestration with specialized consensus[/green]")

if __name__ == "__main__":
    asyncio.run(main())