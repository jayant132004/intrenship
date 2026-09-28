"""
Unit Tests for ARA-1 Tool Registry and Integrations.
"""

import pytest
from tools.tool_registry import ToolRegistry
from tools.sec_edgar import search_sec_filings
from tools.financial_api import get_financial_data
from tools.calculator import run_financial_calculation
from tools.fact_checker import verify_fact_claim


def test_tool_registry_registration_and_dispatch():
    registry = ToolRegistry()
    schemas = registry.get_all_schemas()
    assert len(schemas) >= 10, "Registry must contain at least 10 tools"

    # Test company_profile dispatch
    res = registry.dispatch("company_profile", ticker="MSFT")
    assert res["status"] == "success"
    assert res["data"]["company_name"] == "Microsoft Corporation"


def test_sec_edgar_retrieval():
    res = search_sec_filings("MSFT", filing_type="10-K")
    assert res["status"] in ["success", "partial_success"]
    assert "accession_number" in res
    assert res["ticker"] == "MSFT"


def test_financial_data_api():
    res = get_financial_data("AAPL", statement_type="all")
    assert res["status"] in ["success", "partial_success"]
    data = res["data"]
    assert "income_statement" in data or "key_ratios" in data


def test_calculation_engine_dcf_and_cagr():
    dcf = run_financial_calculation("dcf", {
        "free_cash_flows": [100.0, 115.0, 130.0, 145.0, 160.0],
        "wacc": 0.09,
        "terminal_growth_rate": 0.03
    })
    assert dcf["status"] == "success"
    assert "implied_enterprise_value" in dcf["result"]

    cagr = run_financial_calculation("cagr", {"start_val": 100.0, "end_val": 200.0, "periods": 3})
    assert cagr["status"] == "success"
    assert "cagr" in cagr["result"]


def test_fact_checker_verification():
    res = verify_fact_claim("Microsoft 2024 revenue was 245 billion")
    assert res["status"] == "success"
    assert res["verification_status"] == "VERIFIED_ACCURATE"
    assert len(res["supporting_evidence"]) > 0
