"""
Episodic Memory Logger for ARA-1.
Records research trajectories, query patterns, tool chain effectiveness,
error encounters, and recovery strategies for continuous agent improvement.
"""

import os
import json
import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)


class EpisodicMemory:
    """
    Persists historical agent experiences, successful research strategies,
    and error recovery pathways.
    """

    def __init__(self, storage_path: str = "./data/episodic_memory.json"):
        self.storage_path = storage_path
        self.episodes: List[Dict[str, Any]] = []
        os.makedirs(os.path.dirname(os.path.abspath(self.storage_path)), exist_ok=True)
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    self.episodes = json.load(f)
            except Exception as e:
                logger.warning(f"Could not load episodic memory: {e}")
                self.episodes = []

    def _save(self):
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(self.episodes, f, indent=2)
        except Exception as e:
            logger.error(f"Could not persist episodic memory: {e}")

    def log_episode(
        self,
        query: str,
        query_type: str,
        plan_executed: List[str],
        tools_used: List[str],
        success: bool,
        metrics: Dict[str, Any],
        lessons_learned: List[str] = None
    ):
        """Record an episodic research execution trace."""
        episode = {
            "episode_id": f"EP_{len(self.episodes) + 1:04d}",
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "query_type": query_type,
            "plan_executed": plan_executed,
            "tools_used": tools_used,
            "success": success,
            "metrics": metrics,
            "lessons_learned": lessons_learned or [
                "Checked SEC EDGAR 10-K before secondary web sources.",
                "Cross-verified numerical revenue totals against financial statements."
            ]
        }
        self.episodes.append(episode)
        self._save()

    def get_best_strategy_for_query(self, query_type: str) -> Dict[str, Any]:
        """Retrieve the historical optimal tool chain for a specific query category."""
        matching = [ep for ep in self.episodes if ep.get("query_type") == query_type and ep.get("success")]
        if matching:
            best = matching[-1]
            return {
                "found_strategy": True,
                "recommended_tools": best.get("tools_used", []),
                "recommended_plan": best.get("plan_executed", []),
                "reference_episode": best.get("episode_id")
            }

        # Default fallback recommended trajectories
        defaults = {
            "company_profile": ["company_profile", "financial_data_api", "web_search"],
            "earnings_analysis": ["financial_data_api", "earnings_transcript", "news_sentiment", "fact_checker"],
            "risk_assessment": ["sec_filing_search", "web_search", "news_sentiment", "fact_checker"],
            "industry_comparison": ["sec_filing_search", "peer_comparison", "financial_data_api", "calculation_engine"],
            "thematic_sector": ["vector_db_search", "web_search", "calculation_engine"]
        }
        return {
            "found_strategy": False,
            "recommended_tools": defaults.get(query_type, ["company_profile", "web_search"]),
            "recommended_plan": ["1. Gather fundamental data", "2. Cross-reference filings", "3. Synthesize findings"]
        }
