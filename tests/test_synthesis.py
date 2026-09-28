"""
Unit Tests for ARA-1 Synthesis and Conflict Resolution Engine.
"""

import pytest
from synthesis.conflict_resolver import ConflictResolver
from synthesis.engine import SynthesisEngine


def test_conflict_resolver_adjudicates_sec_over_news():
    resolver = ConflictResolver()
    claim_news = {
        "source": "Speculative Blog Post",
        "statement": "Company revenues collapsed 50% in recent quarter.",
        "tier": "Tier 5 (Social Media / Forums)"
    }
    claim_sec = {
        "source": "SEC Form 10-K Audited Filing",
        "statement": "Company revenues grew 16% to $245B.",
        "tier": "Tier 1 (SEC Filings)"
    }

    result = resolver.reconcile_contradiction("Test Corp", "Revenue Growth", claim_news, claim_sec)
    assert result["canonical_tier"] == "Tier 1 (SEC Filings)"
    assert "Resolution via Reliability Hierarchy" in result["resolution_narrative"]
    assert result["confidence_score"] == 1.0


def test_synthesis_engine_palantir_resolution():
    engine = SynthesisEngine()
    res = engine.process("contradictory_data", {"ticker": "PLTR"}, metadata={"ticker": "PLTR"})
    assert res["status"] == "success"
    assert len(res["conflicts_resolved"]) > 0
