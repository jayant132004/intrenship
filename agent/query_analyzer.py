"""
Query Analyzer for ARA-1.
Performs semantic classification, entity identification, financial scope parsing,
and ambiguity detection on incoming user research prompts.
"""

from typing import Dict, Any, List
import re


class QueryAnalyzer:
    """
    Analyzes incoming financial research queries to determine intent, entity scope,
    complexity score, and whether disambiguation is required.
    """

    KNOWN_ENTITIES = {
        "MICROSOFT": "MSFT", "MSFT": "MSFT",
        "APPLE": "AAPL", "AAPL": "AAPL",
        "TESLA": "TSLA", "TSLA": "TSLA",
        "AMAZON": "AMZN", "AWS": "AMZN", "AMZN": "AMZN",
        "GOOGLE": "GOOGL", "ALPHABET": "GOOGL", "GCP": "GOOGL", "GOOGL": "GOOGL",
        "PALANTIR": "PLTR", "PLTR": "PLTR",
        "NVIDIA": "NVDA", "NVDA": "NVDA",
        "BANKS": "US_BANKING_SECTOR", "BANKING": "US_BANKING_SECTOR"
    }

    def analyze(self, query: str) -> Dict[str, Any]:
        """
        Deconstruct query into actionable execution metadata.
        """
        query_upper = query.upper()
        detected_tickers = []

        for name, ticker in self.KNOWN_ENTITIES.items():
            if name in query_upper and ticker not in detected_tickers:
                detected_tickers.append(ticker)

        # Detect Query Type
        if "EARNINGS" in query_upper or "QUARTER" in query_upper or "BEAT" in query_upper:
            q_type = "earnings_analysis"
            complexity = 2
        elif "RISK" in query_upper or "THREAT" in query_upper or "VULNERABILIT" in query_upper:
            q_type = "risk_assessment"
            complexity = 2
        elif "COMPARE" in query_upper or "VS" in query_upper or "CLOUD" in query_upper or len(detected_tickers) > 1:
            q_type = "industry_comparison"
            complexity = 3
        elif "CONTRADICT" in query_upper or "STRUGGLING" in query_upper or "DISCREPANC" in query_upper:
            q_type = "contradictory_data"
            complexity = 3
        elif "SECTOR" in query_upper or "THEME" in query_upper or "ACROSS" in query_upper or "MEMORY" in query_upper:
            q_type = "thematic_sector"
            complexity = 4
        elif "FULL" in query_upper or "DEGRAD" in query_upper or "COMPLETE" in query_upper:
            q_type = "comprehensive_report"
            complexity = 5
        elif "BANKS" in query_upper or "BANKING" in query_upper or len(detected_tickers) == 0 or "HAPPENING" in query_upper:
            q_type = "ambiguous_query"
            complexity = 4
        else:
            q_type = "company_profile"
            complexity = 1

        is_ambiguous = q_type == "ambiguous_query" or len(detected_tickers) == 0

        return {
            "query": query,
            "query_type": q_type,
            "detected_entities": detected_tickers,
            "complexity_level": complexity,
            "is_ambiguous": is_ambiguous,
            "recommended_template": q_type
        }
