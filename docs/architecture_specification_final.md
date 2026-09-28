# 🏛️ ARA-1 Cognitive Architecture Specification
## Autonomous Financial Research Agent with Multi-Source Synthesis

**System Codename:** `ARA-1` (Autonomous Research Agent 1)  
**Version:** `1.0.0-PROD`  
**Classification:** Institutional Financial AI Architecture  
**Author:** QuantumEdge Research / Zetheta Agentic Engineering Group  

---

## 1. Executive Summary & Problem Formulation

Modern quantitative and fundamental investment research relies heavily on junior financial analysts who spend 70-80% of their time on repeatable, data-intensive tasks: pulling SEC EDGAR filings, transcribing earnings calls, calculating liquidity/profitability ratios, cross-referencing industry news, and assembling structured equity research memos.

`ARA-1` is an autonomous Agentic AI system engineered to replace and augment this workflow. Rather than functioning as a passive conversational chatbot, `ARA-1` operates as an **autonomous, goal-driven cognitive agent** capable of:
1. **Decomposing Ambiguous Queries:** Analyzing intent, financial scope, and temporal boundaries.
2. **Dynamic Plan Formulation:** Generating structured research agendas using a Plan-and-Execute / ReAct hybrid loop.
3. **Multi-Source Data Ingestion:** Orchestrating a registry of 10+ financial tools (SEC EDGAR, market APIs, transcripts, sentiment, calculation engine).
4. **Epistemic Triangulation & Synthesis:** Resolving cross-source contradictions using a 5-tier source reliability hierarchy.
5. **Resilient Self-Correction:** Utilizing exponential backoff, automated fallback chains, circuit breakers, and graceful degradation under API failure.
6. **Institutional-Grade Artifact Generation:** Outputting publication-ready investment research reports grounded in verifiable citations.

---

## 2. Cognitive Engine Architecture

`ARA-1` combines the strategic foresight of **Plan-and-Execute** architectures with the agile responsiveness of **ReAct (Reasoning + Acting)** loops.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ARA-1 COGNITIVE ENGINE                            │
│                                                                             │
│  [User Query] ──> [Query Analyzer & Disambiguation]                        │
│                              │                                              │
│                              ▼                                              │
│                      [Planner Node] ◄──────────────────┐                   │
│                              │                         │ (Replanning)       │
│                              ▼                         │                    │
│                 [ReAct Executor Node] ─────────────────┘                    │
│                   ├── Thought (Reasoning Step)                              │
│                   ├── Action (Tool Invocation)                              │
│                   └── Observation (Result Ingestion)                        │
│                              │                                              │
│                              ▼                                              │
│                    [Synthesis Engine]                                       │
│                   ├── Conflict Resolver (5-Tier Hierarchy)                  │
│                   └── Quantitative Triangulator                             │
│                              │                                              │
│                              ▼                                              │
│                  [Fact Verification Node]                                   │
│                              │                                              │
│                              ▼                                              │
│                  [Report Generator Node] ──> [Final Investment Memo]        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1 StateGraph Definition & Workflow State
The agent maintains a shared execution state (`ResearchState`) throughout its lifecycle:

```python
class ResearchState(TypedDict):
    query: str
    query_type: str                  # 'company_profile' | 'earnings' | 'risk' | 'comparative' | 'thematic'
    clarified_assumptions: List[str] # Documented assumptions for ambiguous queries
    plan: List[str]                  # Numbered research steps
    current_step_index: int
    gathered_data: Dict[str, Any]    # Raw outputs keyed by source and tool
    synthesized_insights: List[Dict] # Structured findings and cross-source connections
    conflicts_detected: List[Dict]   # Discrepancies flagged across sources
    tool_call_history: List[Dict]    # Audit log of all invocations, latencies, status
    memory_hits: int
    external_api_calls: int
    draft_report: str
    verified_report: str
    degradation_notices: List[str]   # Disclosures of missing/failed data sources
```

---

## 3. Tool Registry & Execution Layer

The tool registry provides an extensible, schema-validated execution layer. Every tool defines:
* **OpenAI / Anthropic Function Calling Schema** with strict typing and defaults.
* **Deterministic Parameter Validation** via Pydantic models.
* **Execution Timeout & Rate-Limiter Wrapper**.
* **Designated Secondary & Tertiary Fallback Handlers**.

### 3.1 Registry Matrix

| Tool Identifier | Domain | Primary API / Library | Fallback 1 | Fallback 2 |
| :--- | :--- | :--- | :--- | :--- |
| `sec_filing_search` | Regulatory | SEC EDGAR (`efts.sec.gov`) | FMP SEC Endpoint | Curated Web Search |
| `financial_data_api` | Fundamentals | `yfinance` / FMP / Alpha Vantage | SEC Financial XBRL | Local Cached Store |
| `company_profile` | Metadata | `yfinance` Ticker Info | FMP Profile API | Wikipedia / Web Search |
| `earnings_transcript`| Qualitative | FMP Transcripts / SeekingAlpha | Motley Fool Scraper | 8-K Item 2.02 Filing |
| `news_sentiment` | Market Sentiment | NewsAPI + VADER / TextBlob | GDELT API | Web Search Summary |
| `peer_comparison` | Industry Comp | Sector Aggregator (`yfinance`) | Financial API Multi-call| Hardcoded Peer Index |
| `web_search` | Current Events | Tavily Search API | Brave Search API | DuckDuckGo HTML |
| `calculation_engine`| Math & Valuation | NumPy / Custom Financial Engine | SymPy Math Parser | Deterministic Code |
| `vector_db_search` | Long-Term Memory | ChromaDB Vector Search | BM25 Keyword Search | Local JSON Cache |
| `vector_db_store` | Long-Term Memory | ChromaDB Collection Ingestion | SQLite Document Store| Local JSON Dump |
| `fact_checker` | Grounding | Verification LLM Comparator | Rule-based Triangulation| Secondary LLM Judge |
| `report_generator` | Document Prep | Markdown Synthesis Engine | Jinja2 Template Engine| Fallback Formatter |

---

## 4. Three-Layer Memory System

`ARA-1` implements three isolated yet interacting memory tiers to eliminate redundant API expenditure and support cross-company sector research:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            3-LAYER MEMORY SYSTEM                            │
│                                                                             │
│  1. SHORT-TERM WORKING MEMORY                                               │
│     • Dynamic Token Budget Allocator (128K context window)                 │
│     • Recursive Context Compression when usage > 75%                        │
│     • Tool Output Summarization Buffer                                      │
│                                                                             │
│  2. LONG-TERM VECTOR STORE (ChromaDB)                                       │
│     • Semantic Document Chunks (512 tokens, 64 token overlap)               │
│     • High-Density Embedding (`text-embedding-3-small` / MiniLM)            │
│     • Metadata Filters: {"ticker": "AAPL", "year": 2024, "type": "10-K"}    │
│                                                                             │
│  3. EPISODIC STRATEGY MEMORY                                                │
│     • Success Trajectory Logger (Query Type -> Successful Tool Chains)       │
│     • Error Pattern & Recovery Strategy Cache                               │
│     • Latency & Cost Optimization Indices                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Multi-Source Synthesis & Reliability Protocol

Financial intelligence is fraught with contradictions. `ARA-1` uses a deterministic **Source Reliability Hierarchy** to adjudicate discrepancies:

$$\text{Reliability Rank: } \text{Tier 1 (SEC)} > \text{Tier 2 (APIs)} > \text{Tier 3 (Transcripts)} > \text{Tier 4 (News)} > \text{Tier 5 (Social)}$$

### 5.1 Conflict Resolution Logic
1. **Numerical Discrepancies:** If reported revenue differs between an SEC 10-K and a news article, the 10-K figure is adopted as canonical; the news figure is noted as a preliminary or adjusted figure.
2. **Temporal Alignment:** If Q3 data is compared against TTM (Trailing Twelve Months), `calculation_engine` converts all figures to common annualized or quarterly denominators.
3. **Management Spin vs. Hard Filings:** Management claims in earnings calls regarding "market leadership" are contrasted against segment disclosure revenue shares from 10-K filings.

---

## 6. Resilience, Circuit Breakers & Graceful Degradation

To ensure institutional stability, `ARA-1` is engineered for zero unhandled crashes.

* **Exponential Backoff:** Retries 3 times with backoff intervals ($1\text{s}, 2\text{s}, 4\text{s}$) with jitter.
* **Circuit Breaker:** If an API fails 3 consecutive times within a 60-second window, the circuit trips to `OPEN`, immediately diverting all subsequent calls to secondary fallbacks.
* **Graceful Degradation Notice:** If both primary and fallback tools fail, `ARA-1` inserts a formal **Data Limitation Banner** in the final report, specifying the missing data point, the reason for unavailability, and the analytical impact.

---

## 7. 20+ Quality Evaluation Metrics Framework

| Category | Metric ID | Metric Name | Definition & Formula | Target Benchmark |
| :--- | :--- | :--- | :--- | :--- |
| **Accuracy** | `AC-1` | Numerical Accuracy | % of audited numerical claims verified against primary sources | **100%** |
| | `AC-2` | Citation Validity | % of cited sources resolvable to valid accession # or URL | **100%** |
| | `AC-3` | Hallucination Rate | % of assertions without grounding in retrieved context | **< 2.0%** |
| | `AC-4` | Temporal Alignment | Correct temporal labeling of metrics (e.g. FY24 vs Q3 TTM) | **100%** |
| **Completeness**| `CO-1` | Section Coverage | % of mandatory report template sections completed | **100%** |
| | `CO-2` | Source Diversity | Number of distinct source types utilized ($\ge 4$) | **$\ge 4$ sources** |
| | `CO-3` | Temporal Coverage | Historical horizon covered in years | **$\ge 3$ years** |
| | `CO-4` | Risk Coverage | % of top 10-K risk factors captured | **$\ge 80\%$** |
| **Depth** | `AD-1` | Insight Density | Non-obvious analytical takeaways per page | **$\ge 3$ / page** |
| | `AD-2` | Cross-Source Synthesis | Instances of multi-source correlation | **$\ge 5$ / report** |
| | `AD-3` | Quantitative Reasoning | Original derived calculations (margins, CAGRs, DCF) | **$\ge 10$ calcs** |
| | `AD-4` | Forward Analysis | Reasoned forward projections & scenario models | **$\ge 2$ models** |
| **Coherence** | `CS-1` | Logical Flow | LLM-as-Judge structural coherence score | **$\ge 8.5 / 10$** |
| | `CS-2` | Internal Consistency | Conflicting assertions within the report | **0 conflicts** |
| | `CS-3` | Exec Summary Quality | LLM Judge score on executive synthesis density | **$\ge 9.0 / 10$** |
| | `CS-4` | Professional Formatting| Markdown tables, callouts, and clean typography | **Pass** |
| **Behavior** | `AB-1` | Tool Efficiency | Ratio: useful tool calls cited / total tool calls | **$\ge 70\%$** |
| | `AB-2` | Error Recovery Rate | % of injected tool errors successfully recovered via fallback | **$\ge 90\%$** |
| | `AB-3` | Planning Quality | Completeness of step-by-step decomposition plan | **Pass** |
| | `AB-4` | Memory Utilization | $\text{memory\_hits} / (\text{memory\_hits} + \text{external\_calls})$ | **$\ge 0.30$** |
| | `AB-5` | Execution Latency | Total wall-clock time from query to final report delivery | **< 300 seconds** |

---

## 8. Summary of Benchmark Challenges (C1 – C8)

1. **C1 (Single-Company Profile):** Microsoft Corporation (MSFT) — Financials, executives, business segments.
2. **C2 (Earnings Analysis):** Apple Inc. (AAPL) — Q-on-Q actuals vs. consensus, transcript extraction.
3. **C3 (Risk Assessment):** Tesla Inc. (TSLA) — 10-K item 1A risk taxonomy, news sentiment integration.
4. **C4 (Industry Comparison):** Cloud Giants (AWS vs. Azure vs. GCP) — Segment revenues, operating margins.
5. **C5 (Contradictory Data):** Palantir (PLTR) — Reconciling commercial growth against negative media sentiment.
6. **C6 (Ambiguous Query):** Banking Sector — Entity disambiguation, assumption logging, macro overview.
7. **C7 (Sector Memory):** Tech Sector Thematic Synthesis — Long-term memory query spanning MSFT, AAPL, TSLA, PLTR.
8. **C8 (Full Report under Failure):** NVIDIA (NVDA) — Full institutional report under 50% simulated API failure.

---

*Verified & Approved by QuantumEdge Autonomous Systems Division.*
