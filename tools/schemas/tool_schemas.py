"""
Tool Schemas Module for ARA-1.
Contains JSON function calling schemas adhering to OpenAI / Anthropic specification.
"""

from typing import Dict, Any, List

TOOL_SCHEMAS: Dict[str, Dict[str, Any]] = {
    "sec_filing_search": {
        "name": "sec_filing_search",
        "description": (
            "Search and retrieve official SEC EDGAR filings for a publicly traded US company. "
            "Use this tool when you need authoritative disclosures including annual reports (10-K), "
            "quarterly reports (10-Q), material event reports (8-K), or proxy statements (DEF 14A)."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Stock ticker symbol (e.g., AAPL, MSFT, TSLA, NVDA)"
                },
                "filing_type": {
                    "type": "string",
                    "enum": ["10-K", "10-Q", "8-K", "DEF 14A"],
                    "description": "Type of SEC filing to retrieve"
                },
                "year": {
                    "type": "integer",
                    "description": "Filing calendar year (defaults to the most recent available filing)",
                    "default": None
                }
            },
            "required": ["ticker", "filing_type"]
        }
    },

    "financial_data_api": {
        "name": "financial_data_api",
        "description": (
            "Retrieve structured financial statement data including income statements, balance sheets, "
            "cash flow statements, and key financial ratios for a given ticker."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Stock ticker symbol (e.g., AAPL, MSFT)"
                },
                "statement_type": {
                    "type": "string",
                    "enum": ["income_statement", "balance_sheet", "cash_flow", "key_ratios", "all"],
                    "description": "The specific financial statement or metric category required"
                },
                "period": {
                    "type": "string",
                    "enum": ["annual", "quarterly"],
                    "description": "Reporting period horizon",
                    "default": "annual"
                },
                "years": {
                    "type": "integer",
                    "description": "Number of past historical years to retrieve",
                    "default": 3
                }
            },
            "required": ["ticker", "statement_type"]
        }
    },

    "company_profile": {
        "name": "company_profile",
        "description": (
            "Retrieve fundamental corporate profile including sector, industry, market capitalization, "
            "executive leadership, headquarters, business model overview, and enterprise valuation."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Stock ticker symbol (e.g., MSFT, GOOGL)"
                }
            },
            "required": ["ticker"]
        }
    },

    "earnings_transcript": {
        "name": "earnings_transcript",
        "description": (
            "Retrieve full earnings call transcript including executive prepared remarks and analyst Q&A "
            "for a specific company, quarter, and year."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Stock ticker symbol"
                },
                "quarter": {
                    "type": "string",
                    "enum": ["Q1", "Q2", "Q3", "Q4"],
                    "description": "Fiscal quarter"
                },
                "year": {
                    "type": "integer",
                    "description": "Fiscal year"
                }
            },
            "required": ["ticker", "quarter", "year"]
        }
    },

    "news_sentiment": {
        "name": "news_sentiment",
        "description": (
            "Analyze sentiment, tone, and prevailing narrative themes across recent financial news articles "
            "for a company, industry topic, or ticker."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Topic or company name to evaluate (e.g., 'Tesla operational risks')"
                },
                "num_articles": {
                    "type": "integer",
                    "description": "Number of articles to analyze",
                    "default": 5
                },
                "lookback_days": {
                    "type": "integer",
                    "description": "Number of historical days to inspect",
                    "default": 30
                }
            },
            "required": ["query"]
        }
    },

    "peer_comparison": {
        "name": "peer_comparison",
        "description": (
            "Identify industry competitors and generate a comparative financial benchmarking matrix "
            "across revenue growth, EBITDA margin, P/E ratio, and market share."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Target company ticker"
                },
                "num_peers": {
                    "type": "integer",
                    "description": "Number of peers to compare",
                    "default": 3
                },
                "metrics": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of comparison metrics (e.g., ['revenue', 'margin', 'pe_ratio'])",
                    "default": ["revenue", "revenue_growth", "operating_margin", "pe_ratio"]
                }
            },
            "required": ["ticker"]
        }
    },

    "web_search": {
        "name": "web_search",
        "description": (
            "Perform real-time web search for current news, industry reports, analyst commentary, "
            "and market intelligence not yet reflected in static databases."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string"
                },
                "num_results": {
                    "type": "integer",
                    "description": "Number of search results to return",
                    "default": 5
                },
                "date_range": {
                    "type": "string",
                    "description": "Optional timeframe constraint (e.g., 'past_month')",
                    "default": "all"
                }
            },
            "required": ["query"]
        }
    },

    "calculation_engine": {
        "name": "calculation_engine",
        "description": (
            "Perform deterministic financial calculations including Discounted Cash Flow (DCF) valuation, "
            "Compound Annual Growth Rate (CAGR), WACC, financial ratios, and statistical variances."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "calculation_type": {
                    "type": "string",
                    "enum": ["dcf", "cagr", "ratios", "wacc", "margin_analysis", "variance"],
                    "description": "The type of mathematical financial model to run"
                },
                "inputs": {
                    "type": "object",
                    "description": "Key-value dictionary of numeric inputs for the calculation model"
                }
            },
            "required": ["calculation_type", "inputs"]
        }
    },

    "vector_db_search": {
        "name": "vector_db_search",
        "description": (
            "Search the agent's long-term memory (ChromaDB vector store) for previously ingested and analyzed "
            "company research, SEC chunks, and thematic insights."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Semantic search query string"
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of top matching chunks to retrieve",
                    "default": 5
                },
                "filters": {
                    "type": "object",
                    "description": "Optional metadata filters (e.g., {'ticker': 'MSFT'})",
                    "default": None
                }
            },
            "required": ["query"]
        }
    },

    "vector_db_store": {
        "name": "vector_db_store",
        "description": (
            "Store newly researched findings, extracted SEC filing sections, or synthesized analytical insights "
            "into long-term vector memory for cross-query persistence."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Text document or research chunk to store"
                },
                "metadata": {
                    "type": "object",
                    "description": "Metadata dictionary (ticker, source_type, date, verified)",
                    "default": {}
                }
            },
            "required": ["content"]
        }
    },

    "fact_checker": {
        "name": "fact_checker",
        "description": (
            "Cross-reference specific numerical or narrative claims against retrieved primary sources "
            "(SEC filings, API data) to verify accuracy, detect discrepancies, and compute confidence."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "claim": {
                    "type": "string",
                    "description": "The specific factual or numerical claim to verify"
                },
                "sources": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of source texts or identifiers to cross-check against",
                    "default": []
                }
            },
            "required": ["claim"]
        }
    },

    "report_generator": {
        "name": "report_generator",
        "description": (
            "Format research findings into an institutional-grade investment research report with "
            "structured sections, data tables, callouts, and citation footnotes."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "template": {
                    "type": "string",
                    "enum": ["company_profile", "earnings_analysis", "risk_assessment", "industry_comparison", "thematic_sector", "comprehensive_memo"],
                    "description": "Report template structure to apply"
                },
                "sections": {
                    "type": "object",
                    "description": "Dictionary of section headers and synthesized markdown content"
                },
                "sources": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of formal citations and evidence references",
                    "default": []
                }
            },
            "required": ["template", "sections"]
        }
    }
}
