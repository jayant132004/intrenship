"""
Tools package for ARA-1.
"""

from .tool_registry import ToolRegistry
from .sec_edgar import search_sec_filings
from .financial_api import get_financial_data
from .company_profile import get_company_profile
from .earnings import get_earnings_transcript
from .news_sentiment import analyze_news_sentiment
from .peer_comparison import compare_peers
from .web_search import search_web
from .calculator import run_financial_calculation
from .fact_checker import verify_fact_claim
from .report_gen import generate_investment_report

__all__ = [
    "ToolRegistry",
    "search_sec_filings",
    "get_financial_data",
    "get_company_profile",
    "get_earnings_transcript",
    "analyze_news_sentiment",
    "compare_peers",
    "search_web",
    "run_financial_calculation",
    "verify_fact_claim",
    "generate_investment_report"
]
