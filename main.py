#!/usr/bin/env python3
"""
ARA-1 Autonomous Financial Research Agent — CLI Runner & Demonstration.
Allows interactive research queries, automated challenge benchmark execution,
and real-time 20+ metric evaluation.
"""

import sys
import os
import argparse
import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown

from agent.core import AutonomousFinancialResearchAgent
from evaluation.metrics import EvaluationFramework
from evaluation.dashboard import render_terminal_dashboard


console = Console()


def run_single_query(query: str, failure_rate: float = 0.0):
    """Execute a single autonomous research query and display output."""
    console.print(Panel(f"[bold cyan]Query:[/bold cyan] {query}", title="🤖 ARA-1 Autonomous Agent Execution", expand=False))
    
    with console.status("[bold green]Executing Autonomous Research Loop (Planning -> Tools -> Synthesis -> Fact-Check)...[/bold green]"):
        agent = AutonomousFinancialResearchAgent(failure_injection_rate=failure_rate)
        result = agent.run_research_task(query)

    metrics = result["metrics"]
    
    # Display Execution Metrics Table
    tbl = Table(title="⚡ Execution Telemetry & Efficiency Metrics")
    tbl.add_column("Metric", style="cyan")
    tbl.add_column("Value", style="bold green")
    
    tbl.add_row("Execution Latency", f"{metrics['execution_time_sec']}s")
    tbl.add_row("Query Type Identified", str(metrics['query_type']))
    tbl.add_row("Total Tool Calls Dispatched", str(metrics['total_tool_calls']))
    tbl.add_row("Memory Utilization (AB-4)", f"{metrics['memory_utilization_ratio']} (Target >= 0.30)")
    tbl.add_row("Tool Efficiency Score (AB-1)", f"{round(metrics['tool_efficiency_score']*100, 1)}%")
    tbl.add_row("Estimated Hallucination Rate (AC-3)", f"{metrics['hallucination_rate_estimate']}%")
    tbl.add_row("Circuit Breaker Trips", str(metrics['circuit_breaker_trips']))
    
    console.print(tbl)
    console.print("\n" + "="*80 + "\n")
    console.print(Markdown(result["report_markdown"]))


def run_benchmark_challenges():
    """Run all 8 benchmark challenges and display full 20+ metric scorecard."""
    challenges = [
        ("C1", "MSFT", "Create a comprehensive profile of Microsoft Corporation including business overview, financial summary, key executives, and recent developments."),
        ("C2", "AAPL", "Analyze Apple Inc.'s most recent quarterly earnings. Compare actual results to consensus estimates and identify key takeaways from the earnings call."),
        ("C3", "TSLA", "Produce a comprehensive risk assessment for Tesla Inc. covering financial risks, operational risks, regulatory risks, and competitive risks."),
        ("C4", "Cloud Hyperscalers", "Compare the cloud computing divisions of Amazon (AWS), Microsoft (Azure), and Google (GCP). Analyze revenue growth, market share, margins, and competitive advantages."),
        ("C5", "PLTR", "Research Palantir Technologies. Note: Recent news reports suggest the company is struggling, but their financial statements show strong growth. Investigate and explain the apparent contradiction."),
        ("C6", "US Banks", "What's happening with the banks?"),
        ("C7", "Tech Sector", "Based on the companies you've already researched, what themes emerge across the technology sector? Identify cross-cutting risks and opportunities."),
        ("C8", "NVDA (50% Degradation)", "Produce a complete investment research report on NVIDIA Corporation under 50% simulated tool failure rate.")
    ]

    eval_framework = EvaluationFramework()
    results = []

    console.print(Panel("[bold yellow]Executing 8 Progressive Benchmark Challenges (C1 - C8)...[/bold yellow]", title="🏆 Institutional Quality Benchmark Suite"))

    for cid, entity, query in challenges:
        console.print(f"[cyan]>> Running {cid}: {entity}...[/cyan]")
        rate = 0.5 if cid == "C8" else 0.0
        agent = AutonomousFinancialResearchAgent(failure_injection_rate=rate)
        out = agent.run_research_task(query)
        eval_res = eval_framework.evaluate_output(cid, query, out["report_markdown"], out["metrics"], ticker=entity.split()[0])
        results.append(eval_res)

    render_terminal_dashboard(results)


def main():
    parser = argparse.ArgumentParser(description="ARA-1 Autonomous Financial Research Agent CLI")
    parser.add_argument("--query", "-q", type=str, help="Research query to execute")
    parser.add_argument("--benchmark", "-b", action="store_true", help="Run all 8 benchmark challenges")
    parser.add_argument("--failure-rate", "-f", type=float, default=0.0, help="Simulated tool failure rate (0.0 to 1.0)")

    args = parser.parse_args()

    if args.benchmark:
        run_benchmark_challenges()
    elif args.query:
        run_single_query(args.query, failure_rate=args.failure_rate)
    else:
        # Default interactive run: Cloud Comparison (Challenge 4)
        console.print("[bold cyan]No arguments provided. Running default demo: Challenge 4 (Cloud Infrastructure Comparison: AWS vs Azure vs GCP)...[/bold cyan]\n")
        run_single_query(
            "Compare the cloud computing divisions of Amazon (AWS), Microsoft (Azure), and Google (GCP). Analyze revenue growth, market share, margins, and competitive advantages."
        )


if __name__ == "__main__":
    main()
