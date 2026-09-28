"""
End-to-End Unit & Integration Tests for ARA-1 Agent Core.
"""

import pytest
from agent.core import AutonomousFinancialResearchAgent
from agent.query_analyzer import QueryAnalyzer
from agent.disambiguation import QueryDisambiguator


def test_query_analyzer_and_disambiguation():
    analyzer = QueryAnalyzer()
    res = analyzer.analyze("What's happening with the banks?")
    assert res["query_type"] == "ambiguous_query"
    assert res["is_ambiguous"] is True

    disambiguator = QueryDisambiguator()
    dis = disambiguator.disambiguate("What's happening with the banks?", res)
    assert len(dis["documented_assumptions"]) >= 3


def test_agent_end_to_end_single_company():
    agent = AutonomousFinancialResearchAgent()
    out = agent.run_research_task("Create a comprehensive profile of Microsoft Corporation.")
    assert out["status"] == "success"
    assert "Microsoft" in out["report_markdown"]
    assert out["metrics"]["total_tool_calls"] >= 3
    assert out["metrics"]["memory_utilization_ratio"] >= 0.0


def test_agent_circuit_breaker_and_resilience():
    # Test agent running with simulated tool failures (Challenge 8 condition)
    agent = AutonomousFinancialResearchAgent(failure_injection_rate=0.5)
    out = agent.run_research_task("Produce a complete investment research report on NVIDIA Corporation under intermittent API failures.")
    assert out["status"] == "success"
    assert "NVIDIA" in out["report_markdown"]
