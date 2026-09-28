"""
Unit Tests for ARA-1 Memory Architecture (Short-term, Vector Store, Episodic).
"""

import pytest
import os
import shutil
from memory.vector_store import VectorMemoryStore
from memory.context_manager import ContextManager
from memory.episodic import EpisodicMemory


@pytest.fixture
def temp_memory_env(tmp_path):
    persist_dir = str(tmp_path / "chromadb")
    episodic_file = str(tmp_path / "episodic.json")
    return persist_dir, episodic_file


def test_vector_store_ingestion_and_search(temp_memory_env):
    p_dir, _ = temp_memory_env
    store = VectorMemoryStore(persist_dir=p_dir)

    # Store sample financial chunks
    res = store.store_document(
        "Microsoft Azure cloud revenue expanded by 29% in FY2024 driven by enterprise AI adoption.",
        metadata={"ticker": "MSFT", "source_type": "10-K"}
    )
    assert res["status"] == "success"
    assert res["stored_chunks_count"] > 0

    # Search
    search_res = store.search("Azure cloud revenue growth", top_k=2)
    assert search_res["status"] == "success"
    assert search_res["hits_count"] > 0
    assert search_res["results"][0]["metadata"]["ticker"] == "MSFT"


def test_context_manager_budgeting():
    cm = ContextManager(max_context_tokens=1000, compression_threshold_ratio=0.5)
    cm.add_observation("sec_filing_search", {"ticker": "AAPL"}, {"filing": "10-K", "revenue": "391B"})
    tokens = cm.get_total_working_tokens()
    assert tokens > 0
    assert not cm.should_compress()


def test_episodic_memory_strategy_logging(temp_memory_env):
    _, ep_file = temp_memory_env
    em = EpisodicMemory(storage_path=ep_file)
    em.log_episode(
        query="Microsoft profile",
        query_type="company_profile",
        plan_executed=["company_profile", "financial_data_api"],
        tools_used=["company_profile", "financial_data_api"],
        success=True,
        metrics={"execution_time_sec": 1.2}
    )

    strat = em.get_best_strategy_for_query("company_profile")
    assert strat["found_strategy"] is True
    assert "company_profile" in strat["recommended_tools"]
