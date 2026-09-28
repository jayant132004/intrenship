"""
Earnings Call Transcript Tool for ARA-1.
Retrieves executive prepared remarks and analyst Q&A sessions.
"""

from typing import Dict, Any, Optional

TRANSCRIPTS: Dict[str, Dict[str, Any]] = {
    "AAPL": {
        "Q3_2024": {
            "quarter": "Q3",
            "year": 2024,
            "call_date": "August 1, 2024",
            "prepared_remarks_ceo": (
                "Tim Cook (CEO): 'Today Apple is reporting a new June quarter revenue record of $85.8 billion, "
                "up 5% from a year ago. We set all-time revenue records in over two dozen countries and regions. "
                "During the quarter, we were excited to announce incredible updates to our software platforms, including "
                "Apple Intelligence, an intuitive, private personal intelligence system that puts powerful, generative AI models "
                "at the center of iPhone, iPad, and Mac.'"
            ),
            "prepared_remarks_cfo": (
                "Luca Maestri (CFO): 'Our record business performance drove EPS growth of 11% to $1.40 and nearly $29 billion in "
                "operating cash flow. Services set an all-time revenue record of $24.2 billion, up 14% year-over-year with gross margin of 74.0%. "
                "We returned over $32 billion to shareholders including $26 billion in open-market share repurchases.'"
            ),
            "analyst_qa_highlights": [
                {
                    "analyst": "Wamsi Mohan (Bank of America)",
                    "question": "Can you give us more detail on the rollout timeline for Apple Intelligence and its impact on the hardware upgrade cycle?",
                    "response": "Tim Cook: 'We are very excited about Apple Intelligence. We began rolling out features to developers and will deploy in US English this fall followed by additional languages in 2025. We believe this represents a compelling reason to upgrade.'"
                },
                {
                    "analyst": "Erik Woodring (Morgan Stanley)",
                    "question": "How are you viewing the competitive environment and regulatory landscape in Greater China and Europe?",
                    "response": "Luca Maestri: 'In Greater China, revenue was $14.7B, which represents a 6.5% decline YoY, though this reflects significant sequential improvement from Q2 on a constant-currency basis.'"
                }
            ],
            "key_takeaways": [
                "EPS beat consensus ($1.40 vs $1.35 expected).",
                "Services gross margin expanded to record 74.0%.",
                "Apple Intelligence positioned as primary catalyst for multi-year iPhone replacement cycle.",
                "China revenue decline moderated to -6.5% with currency headwinds."
            ]
        }
    },
    "MSFT": {
        "Q4_2024": {
            "quarter": "Q4",
            "year": 2024,
            "call_date": "July 30, 2024",
            "prepared_remarks_ceo": (
                "Satya Nadella (CEO): 'Our Cloud surpassed $36.8 billion in quarterly revenue, up 21%. "
                "Azure continues to take share as customers apply our platforms and AI tools. Azure AI customers grew to over 60,000, "
                "and average spend continues to increase. Copilot for M365 is driving enterprise productivity transformation.'"
            ),
            "prepared_remarks_cfo": (
                "Amy Hood (CFO): 'Azure revenue grew 29% in constant currency, with 8 points of growth from AI services. "
                "Capital expenditures were $19.0 billion in Q4, driven by cloud demand and AI infrastructure investments. "
                "We expect CapEx to increase in FY25 to support capacity needs.'"
            ),
            "analyst_qa_highlights": [
                {
                    "analyst": "Keith Weiss (Morgan Stanley)",
                    "question": "Could you clarify Azure capacity constraints and the expected reacceleration in the second half of FY25?",
                    "response": "Amy Hood: 'Demand continues to outpace available capacity. As datacenter builds come online throughout the first half, we anticipate Azure growth will reaccelerate in H2.'"
                }
            ],
            "key_takeaways": [
                "Azure grew 29% YoY with 8 percentage points contributed directly by generative AI workloads.",
                "CapEx stepped up significantly to $19B/quarter to build out AI GPU datacenter footprint.",
                "Short-term capacity constraints limiting immediate Azure upside until new datacenters energize."
            ]
        }
    },
    "TSLA": {
        "Q3_2024": {
            "quarter": "Q3",
            "year": 2024,
            "call_date": "October 23, 2024",
            "prepared_remarks_ceo": (
                "Elon Musk (CEO): 'We delivered strong results in Q3 with growth in vehicle deliveries and record energy storage deployments. "
                "Our cost of goods sold per vehicle came down to its lowest level ever at ~$35,100. We anticipate vehicle growth of 20% to 30% next year "
                "driven by lower cost models and autonomy breakthroughs.'"
            ),
            "prepared_remarks_cfo": (
                "Vaibhav Taneja (CFO): 'Automotive gross margin ex-regulatory credits improved sequentially to 17.1%. "
                "Operating cash flow was $6.3B and free cash flow was $2.7B. Energy business gross margins reached a record 30.5%.'"
            ),
            "analyst_qa_highlights": [
                {
                    "analyst": "Dan Levy (Barclays)",
                    "question": "What is the timeline for the sub-$30k mass-market vehicle and Cybercab production?",
                    "response": "Elon Musk: 'We remain on track to start production of more affordable models in the first half of 2025 utilizing aspects of the next-generation platform along with existing lines.'"
                }
            ],
            "key_takeaways": [
                "Automotive gross margin ex-credits rebounded to 17.1%, beating analyst consensus.",
                "Energy Storage division emerged as high-margin engine with 30.5% gross margin.",
                "Targeted 20-30% volume growth in 2025 underpinned by affordable vehicle platform launches."
            ]
        }
    }
}


def get_earnings_transcript(ticker: str, quarter: str = "Q3", year: int = 2024) -> Dict[str, Any]:
    """
    Retrieve full earnings call transcript for a company.
    """
    ticker_clean = ticker.strip().upper()
    key = f"{quarter}_{year}"

    if ticker_clean in TRANSCRIPTS:
        quarters = TRANSCRIPTS[ticker_clean]
        if key in quarters:
            return {
                "status": "success",
                "source": "Tier-3 Corporate Earnings Call Transcripts",
                "ticker": ticker_clean,
                "quarter": quarter,
                "year": year,
                "data": quarters[key]
            }
        # Return most recent available quarter
        latest_key = list(quarters.keys())[0]
        return {
            "status": "success",
            "source": "Tier-3 Corporate Earnings Call Transcripts",
            "ticker": ticker_clean,
            "quarter": quarter,
            "year": year,
            "data": quarters[latest_key],
            "notice": f"Retrieved transcript for closest available period ({latest_key})."
        }

    return {
        "status": "partial_success",
        "source": "Earnings Transcript Archive",
        "ticker": ticker_clean,
        "quarter": quarter,
        "year": year,
        "data": {
            "prepared_remarks_ceo": f"Executive remarks for {ticker_clean} {quarter} {year} highlighted solid execution.",
            "prepared_remarks_cfo": f"Financial update for {ticker_clean} indicated stable margins and disciplined capital allocation.",
            "key_takeaways": ["Revenue and EPS in line with expectations.", "Management maintained forward guidance."]
        }
    }
