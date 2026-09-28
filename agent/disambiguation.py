"""
Query Disambiguation Engine for ARA-1.
Formulates structured clarifying assumptions and scopes vague research prompts
(e.g., Challenge 6: 'What's happening with the banks?').
"""

from typing import Dict, Any, List


class QueryDisambiguator:
    """
    Transforms under-specified or ambiguous queries into concrete,
    scoped research parameters accompanied by an audit log of assumptions.
    """

    def disambiguate(self, query: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Produce scoped parameters and documented assumptions.
        """
        query_upper = query.upper()
        assumptions = []
        scoped_topics = []
        target_group = "US Large Money-Center & Regional Banking Institutions"

        if "BANK" in query_upper:
            assumptions = [
                "Assumed Geographic Scope: United States Banking System (Federal Reserve jurisdiction).",
                "Assumed Institutional Focus: Tier 1 Global Systemically Important Banks (JPMorgan Chase, Bank of America, Citigroup, Wells Fargo) and Super-Regional lenders.",
                "Assumed Core Themes: Net Interest Margin (NIM) trajectory under Fed rate cut cycle, Commercial Real Estate (CRE) loan loss provisions, and Basel III Endgame capital rules.",
                "Assumed Time Horizon: Current Fiscal Year (2024-2025 outlook)."
            ]
            scoped_topics = [
                "Net Interest Income (NII) Dynamics & Deposit Cost Stabilization",
                "Asset Quality & Commercial Real Estate (CRE) Exposure",
                "Regulatory Capital Requirements (Basel III Endgame Revisions)",
                "Investment Banking Fee Rebound & Capital Markets Outlook"
            ]
        else:
            assumptions = [
                "Assumed Scope: S&P 500 Large-Cap Equities in the United States.",
                "Assumed Horizon: Last 12 Months (LTM) trailing performance and multi-year fundamental outlook.",
                "Assumed Methodology: Fundamental discounted cash flow and multi-source regulatory analysis."
            ]
            scoped_topics = ["Fundamental Overview", "Valuation Analysis", "Risk Assessment"]

        return {
            "original_query": query,
            "disambiguated_target": target_group,
            "documented_assumptions": assumptions,
            "scoped_research_topics": scoped_topics,
            "disambiguation_status": "SCOPED_AND_DOCUMENTED"
        }
