"""
Fallback Tool Chains for ARA-1.
Defines deterministic secondary and tertiary fallback strategies for every primary tool
to maintain research momentum when primary APIs degrade or fail.
"""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class FallbackChains:
    """
    Manages multi-tier fallback tool execution when primary tools encounter errors.
    """

    FALLBACK_MAP = {
        "sec_filing_search": [
            {"tool": "financial_data_api", "transform": lambda args: {"ticker": args.get("ticker", "AAPL"), "statement_type": "all"}},
            {"tool": "web_search", "transform": lambda args: {"query": f"{args.get('ticker')} SEC {args.get('filing_type', '10-K')} financial filing summary"}}
        ],
        "financial_data_api": [
            {"tool": "company_profile", "transform": lambda args: {"ticker": args.get("ticker", "AAPL")}},
            {"tool": "web_search", "transform": lambda args: {"query": f"{args.get('ticker')} audited financial statements revenue margin"}}
        ],
        "earnings_transcript": [
            {"tool": "news_sentiment", "transform": lambda args: {"query": f"{args.get('ticker')} earnings call transcript results"}},
            {"tool": "web_search", "transform": lambda args: {"query": f"{args.get('ticker')} {args.get('quarter', 'Q3')} earnings call key takeaways"}}
        ],
        "news_sentiment": [
            {"tool": "web_search", "transform": lambda args: {"query": f"{args.get('query', 'market')} recent news analysis sentiment"}},
            {"tool": "company_profile", "transform": lambda args: {"ticker": args.get("query", "MSFT")[:5].strip().upper()}}
        ],
        "peer_comparison": [
            {"tool": "financial_data_api", "transform": lambda args: {"ticker": args.get("ticker", "MSFT"), "statement_type": "key_ratios"}},
            {"tool": "web_search", "transform": lambda args: {"query": f"{args.get('ticker')} top industry competitors peer comparison"}}
        ]
    }

    def get_fallbacks_for_tool(self, tool_name: str) -> List[Dict[str, Any]]:
        """Retrieve fallback sequence for a given tool."""
        return self.FALLBACK_MAP.get(tool_name, [
            {"tool": "web_search", "transform": lambda args: {"query": str(args)}}
        ])
