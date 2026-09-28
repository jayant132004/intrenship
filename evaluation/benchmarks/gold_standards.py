"""
Gold-Standard Analyst Benchmark Dataset for ARA-1.
Contains human-analyst ground-truth baselines for Microsoft (MSFT), Apple (AAPL), and Tesla (TSLA).
"""

from typing import Dict, Any

GOLD_STANDARDS: Dict[str, Dict[str, Any]] = {
    "MSFT": {
        "ticker": "MSFT",
        "company_name": "Microsoft Corporation",
        "fiscal_year": 2024,
        "audited_metrics": {
            "total_revenue": 245120000000,
            "operating_income": 109430000000,
            "net_income": 88140000000,
            "free_cash_flow": 74078000000,
            "azure_growth_rate": "29%"
        },
        "required_sections": [
            "Executive Summary & Business Overview",
            "Audited Financial Performance & Multi-Year Trend",
            "Strategic Catalysts, Risk Factors & Valuation Outlook"
        ],
        "mandatory_risk_factors": [
            "Cloud infrastructure competition",
            "Datacenter capital expenditures",
            "Cybersecurity vulnerabilities",
            "AI regulatory scrutiny"
        ]
    },
    "AAPL": {
        "ticker": "AAPL",
        "company_name": "Apple Inc.",
        "fiscal_year": 2024,
        "audited_metrics": {
            "total_revenue": 391035000000,
            "q3_revenue": 85780000000,
            "q3_eps": 1.40,
            "services_revenue": 96170000000,
            "gross_margin": "46.2%"
        },
        "required_sections": [
            "Executive Earnings Summary",
            "Transcript Analysis & Management Guidance",
            "Forward Strategic Outlook"
        ],
        "mandatory_risk_factors": [
            "Supply chain China concentration",
            "App Store antitrust litigation",
            "Consumer hardware upgrade cycles",
            "Foreign exchange volatility"
        ]
    },
    "TSLA": {
        "ticker": "TSLA",
        "company_name": "Tesla, Inc.",
        "fiscal_year": 2024,
        "audited_metrics": {
            "total_revenue": 96773000000,
            "auto_gross_margin_ex_credits": "17.1%",
            "energy_storage_growth": "125%",
            "cash_and_equivalents": 29094000000
        },
        "required_sections": [
            "Executive Risk Matrix & Overview",
            "Categorized Risk Taxonomy (SEC Form 10-K & News Synthesis)",
            "Quantitative Sensitivity & Mitigating Factors"
        ],
        "mandatory_risk_factors": [
            "EV price reduction and margin erosion",
            "FSD autonomous regulatory scrutiny",
            "China EV competition",
            "Cybercab and affordable vehicle timeline execution"
        ]
    }
}
