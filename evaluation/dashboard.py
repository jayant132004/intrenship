"""
Interactive Evaluation Dashboard Generator for ARA-1.
Renders summary performance tables and metric heatmaps in terminal or HTML.
"""

from typing import Dict, Any, List
from rich.console import Console
from rich.table import Table


def render_terminal_dashboard(evaluation_results: List[Dict[str, Any]]):
    """Print a rich formatted evaluation scorecard to the console."""
    console = Console()
    table = Table(title="🏛️ ARA-1 Autonomous Research Agent — Evaluation Scorecard (20+ Metrics)")

    table.add_column("Challenge ID", style="cyan", justify="center")
    table.add_column("Target Entity", style="bold green")
    table.add_column("Composite Score", style="magenta", justify="right")
    table.add_column("Num Accuracy (AC-1)", justify="center")
    table.add_column("Hallucination (AC-3)", justify="center")
    table.add_column("Tool Efficiency (AB-1)", justify="center")
    table.add_column("Memory Util (AB-4)", justify="center")
    table.add_column("Status", style="bold")

    for res in evaluation_results:
        cid = res["challenge_id"]
        entity = res["target_entity"]
        pts = f"{res['composite_score_points']} / 1000"
        ac1 = res["category_1_accuracy"]["AC-1_numerical_accuracy"]
        ac3 = res["category_1_accuracy"]["AC-3_hallucination_rate"]
        ab1 = res["category_5_agent_behavior"]["AB-1_tool_efficiency"]
        ab4 = res["category_5_agent_behavior"]["AB-4_memory_utilization"]
        status = "[green]EXEMPLARY[/green]" if res["composite_score_points"] >= 900 else "[yellow]PASS[/yellow]"

        table.add_row(cid, entity, pts, ac1, ac3, ab1, ab4, status)

    console.print(table)
