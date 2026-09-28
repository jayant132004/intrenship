"""
Company Profile Tool for ARA-1.
Retrieves corporate identity, market capitalization, executive leadership,
business segments, and enterprise valuation.
"""

from typing import Dict, Any

PROFILES: Dict[str, Dict[str, Any]] = {
    "MSFT": {
        "company_name": "Microsoft Corporation",
        "ticker": "MSFT",
        "exchange": "NASDAQ",
        "sector": "Technology",
        "industry": "Software - Infrastructure / Cloud",
        "market_cap": "$3.15 Trillion",
        "enterprise_value": "$3.18 Trillion",
        "headquarters": "Redmond, Washington, USA",
        "ceo": "Satya Nadella",
        "cfo": "Amy Hood",
        "employees": 221000,
        "business_summary": (
            "Microsoft Corporation develops and supports software, services, devices, and solutions. "
            "Operates in three primary segments: Productivity and Business Processes (Office 365, LinkedIn, Dynamics), "
            "Intelligent Cloud (Azure public cloud, Windows Server, GitHub), and More Personal Computing (Windows OEM, Surface, Xbox, Gaming)."
        ),
        "recent_catalysts": [
            "Copilot AI integration across Microsoft 365 enterprise suite.",
            "Accelerating Azure cloud infrastructure revenue driven by generative AI model hosting.",
            "Expansion into custom datacenter silicon (Azure Maia AI Accelerator and Cobalt CPU)."
        ]
    },
    "AAPL": {
        "company_name": "Apple Inc.",
        "ticker": "AAPL",
        "exchange": "NASDAQ",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "market_cap": "$3.45 Trillion",
        "enterprise_value": "$3.52 Trillion",
        "headquarters": "Cupertino, California, USA",
        "ceo": "Tim Cook",
        "cfo": "Luca Maestri (Transitioning to Kevan Parekh)",
        "employees": 161000,
        "business_summary": (
            "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, "
            "and accessories, and sells a variety of related services (App Store, Apple Music, iCloud, Apple Pay, AppleCare)."
        ),
        "recent_catalysts": [
            "Rollout of Apple Intelligence across iOS 18 devices to drive iPhone 16 upgrade cycle.",
            "High-margin Services segment surpassing $96B in annualized run rate.",
            "Expansion of spatial computing ecosystem via Vision Pro."
        ]
    },
    "TSLA": {
        "company_name": "Tesla, Inc.",
        "ticker": "TSLA",
        "exchange": "NASDAQ",
        "sector": "Consumer Cyclical / Technology",
        "industry": "Auto Manufacturers / Clean Energy & Robotics",
        "market_cap": "$780 Billion",
        "enterprise_value": "$765 Billion",
        "headquarters": "Austin, Texas, USA",
        "ceo": "Elon Musk",
        "cfo": "Vaibhav Taneja",
        "employees": 140000,
        "business_summary": (
            "Tesla, Inc. designs, develops, manufactures, sells, and leases electric vehicles (Model 3, Y, S, X, Cybertruck, Semi), "
            "energy generation and storage systems (Megapack, Powerwall), and is developing autonomous driving software (FSD) and humanoid robotics (Optimus)."
        ),
        "recent_catalysts": [
            "Rapid expansion of Energy Storage segment (Megapack margin expansion).",
            "Unveiling of dedicated Cybercab autonomous robotaxi platform and unsupervised FSD roadmaps.",
            "Cost reductions in next-generation unboxed vehicle manufacturing architecture."
        ]
    },
    "AMZN": {
        "company_name": "Amazon.com, Inc.",
        "ticker": "AMZN",
        "exchange": "NASDAQ",
        "sector": "Consumer Cyclical / Technology",
        "industry": "Internet Retail / Cloud Infrastructure",
        "market_cap": "$2.05 Trillion",
        "enterprise_value": "$2.12 Trillion",
        "headquarters": "Seattle, Washington, USA",
        "ceo": "Andy Jassy",
        "cfo": "Brian Olsavsky",
        "employees": 1525000,
        "business_summary": (
            "Amazon focuses on retail, advertising, subscription services, and cloud computing. "
            "Amazon Web Services (AWS) is the world's leading cloud computing provider."
        ),
        "recent_catalysts": ["AWS AI revenue run rate reaching multi-billion dollar scale", "High-margin digital advertising growth"]
    },
    "GOOGL": {
        "company_name": "Alphabet Inc.",
        "ticker": "GOOGL",
        "exchange": "NASDAQ",
        "sector": "Communication Services / Technology",
        "industry": "Internet Content & Information / Cloud",
        "market_cap": "$2.20 Trillion",
        "enterprise_value": "$2.15 Trillion",
        "headquarters": "Mountain View, California, USA",
        "ceo": "Sundar Pichai",
        "cfo": "Anat Ashkenazi",
        "employees": 182000,
        "business_summary": (
            "Alphabet is a global tech holding company. Subsidiaries include Google (Search, Ads, YouTube, Cloud, Android, Hardware) "
            "and Other Bets (Waymo autonomous vehicles, Verily life sciences)."
        ),
        "recent_catalysts": ["Gemini multimodal models powering Google Workspace and Cloud", "Google Cloud operating margin expansion"]
    },
    "PLTR": {
        "company_name": "Palantir Technologies Inc.",
        "ticker": "PLTR",
        "exchange": "NYSE",
        "sector": "Technology",
        "industry": "Software - Infrastructure / Enterprise AI",
        "market_cap": "$85 Billion",
        "enterprise_value": "$81 Billion",
        "headquarters": "Denver, Colorado, USA",
        "ceo": "Alex Karp",
        "cfo": "David Glazer",
        "employees": 3800,
        "business_summary": (
            "Palantir builds software platforms for big data analytics and AI integration. "
            "Flagship platforms include Gotham (defense/intelligence), Foundry (enterprise operating system), "
            "Apollo (continuous deployment), and AIP (Artificial Intelligence Platform)."
        ),
        "recent_catalysts": [
            "AIP Bootcamp velocity expanding US Commercial client base by >80%.",
            "Inclusion in the S&P 500 index cementing institutional ownership.",
            "Consecutive quarters of accelerating GAAP profitability."
        ]
    },
    "NVDA": {
        "company_name": "NVIDIA Corporation",
        "ticker": "NVDA",
        "exchange": "NASDAQ",
        "sector": "Technology",
        "industry": "Semiconductors & AI Compute",
        "market_cap": "$3.10 Trillion",
        "enterprise_value": "$3.08 Trillion",
        "headquarters": "Santa Clara, California, USA",
        "ceo": "Jensen Huang",
        "cfo": "Colette Kress",
        "employees": 29600,
        "business_summary": (
            "NVIDIA Corporation pioneers accelerated computing and graphics processing units (GPUs). "
            "Dominates global AI training and inference infrastructure through Hopper (H100/H200) and Blackwell (B200) "
            "platforms, CUDA software architecture, and Quantum-2 InfiniBand networking."
        ),
        "recent_catalysts": [
            "Transition to Blackwell architecture with unprecedented computing density.",
            "Software & CUDA ecosystem moats creating high switching costs for hyperscalers.",
            "Expansion into sovereign AI and enterprise robotics compute stacks."
        ]
    }
}


def get_company_profile(ticker: str) -> Dict[str, Any]:
    """
    Retrieve comprehensive corporate profile for a company.
    """
    ticker_clean = ticker.strip().upper()
    if ticker_clean in PROFILES:
        return {
            "status": "success",
            "source": "Company Profile Master Registry",
            "ticker": ticker_clean,
            "data": PROFILES[ticker_clean]
        }

    return {
        "status": "partial_success",
        "source": "Fallback Profile Estimator",
        "ticker": ticker_clean,
        "data": {
            "company_name": f"{ticker_clean} Corporation",
            "ticker": ticker_clean,
            "sector": "Diversified Industries",
            "industry": "General Business",
            "market_cap": "Undisclosed / Mid-Cap",
            "business_summary": f"Public enterprise operating under ticker symbol {ticker_clean}."
        }
    }
