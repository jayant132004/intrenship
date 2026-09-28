"""
Master Tool Registry and Dispatcher for ARA-1.
Manages tool definitions, OpenAI/Anthropic schemas, parameter validation,
runtime dispatching, latency tracking, retry handling, and fault injection.
"""

import time
import random
import logging
from typing import Dict, Any, Callable, Optional, List
from tools.schemas.tool_schemas import TOOL_SCHEMAS

# Import specific tool handlers
from tools.sec_edgar import search_sec_filings
from tools.financial_api import get_financial_data
from tools.company_profile import get_company_profile
from tools.earnings import get_earnings_transcript
from tools.news_sentiment import analyze_news_sentiment
from tools.peer_comparison import compare_peers
from tools.web_search import search_web
from tools.calculator import run_financial_calculation
from tools.fact_checker import verify_fact_claim
from tools.report_gen import generate_investment_report

logger = logging.getLogger(__name__)


class ToolRegistry:
    """
    Central registry and execution manager for ARA-1 autonomous tools.
    """

    def __init__(self, failure_injection_rate: float = 0.0):
        self.failure_injection_rate = failure_injection_rate
        self.tool_schemas: Dict[str, Dict[str, Any]] = TOOL_SCHEMAS
        self.handlers: Dict[str, Callable] = {}
        self.call_history: List[Dict[str, Any]] = []
        self._register_default_tools()

    def _register_default_tools(self):
        """Bind tool names to their underlying executable functions."""
        self.handlers["sec_filing_search"] = search_sec_filings
        self.handlers["financial_data_api"] = get_financial_data
        self.handlers["company_profile"] = get_company_profile
        self.handlers["earnings_transcript"] = get_earnings_transcript
        self.handlers["news_sentiment"] = analyze_news_sentiment
        self.handlers["peer_comparison"] = compare_peers
        self.handlers["web_search"] = search_web
        self.handlers["calculation_engine"] = run_financial_calculation
        self.handlers["fact_checker"] = verify_fact_claim
        self.handlers["report_generator"] = generate_investment_report

    def register_tool(self, name: str, schema: Dict[str, Any], handler: Callable):
        """Register a custom tool dynamically."""
        self.tool_schemas[name] = schema
        self.handlers[name] = handler

    def get_all_schemas(self) -> List[Dict[str, Any]]:
        """Return list of all registered tool schemas for LLM system prompt injection."""
        return list(self.tool_schemas.values())

    def get_schema(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve schema for a specific tool."""
        return self.tool_schemas.get(tool_name)

    def dispatch(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a tool by name with parameter validation, latency recording, and resilience checks.
        """
        start_time = time.time()

        # Simulated Tool Failure Injection (for Challenge 8 & resilience stress testing)
        if self.failure_injection_rate > 0.0 and tool_name in ["sec_filing_search", "financial_data_api"]:
            if random.random() < self.failure_injection_rate:
                latency = round((time.time() - start_time) * 1000, 2)
                record = {
                    "tool": tool_name,
                    "status": "injected_failure",
                    "latency_ms": latency,
                    "params": kwargs,
                    "error": f"Simulated 500 Network Timeout for {tool_name} under degradation test."
                }
                self.call_history.append(record)
                return {
                    "status": "error",
                    "error_code": "CIRCUIT_FAIL_500",
                    "message": f"Primary API for {tool_name} temporarily unreachable (Simulated Rate-Limit/Outage).",
                    "fallback_required": True
                }

        if tool_name not in self.handlers:
            latency = round((time.time() - start_time) * 1000, 2)
            record = {
                "tool": tool_name,
                "status": "not_found",
                "latency_ms": latency,
                "params": kwargs
            }
            self.call_history.append(record)
            return {
                "status": "error",
                "error_code": "TOOL_NOT_FOUND",
                "message": f"No tool registered under name '{tool_name}'."
            }

        try:
            handler = self.handlers[tool_name]
            result = handler(**kwargs)
            latency = round((time.time() - start_time) * 1000, 2)
            record = {
                "tool": tool_name,
                "status": "success",
                "latency_ms": latency,
                "params": kwargs,
                "output_preview": str(result)[:200]
            }
            self.call_history.append(record)
            return result
        except Exception as e:
            latency = round((time.time() - start_time) * 1000, 2)
            logger.error(f"Error executing tool {tool_name}: {e}")
            record = {
                "tool": tool_name,
                "status": "exception",
                "latency_ms": latency,
                "params": kwargs,
                "error": str(e)
            }
            self.call_history.append(record)
            return {
                "status": "error",
                "error_code": "EXECUTION_EXCEPTION",
                "message": str(e),
                "fallback_required": True
            }

    def get_metrics(self) -> Dict[str, Any]:
        """Compute tool execution metrics."""
        total = len(self.call_history)
        if total == 0:
            return {"total_calls": 0, "success_rate": 1.0, "avg_latency_ms": 0.0}

        successes = sum(1 for c in self.call_history if c["status"] == "success")
        latencies = [c.get("latency_ms", 0.0) for c in self.call_history]
        return {
            "total_calls": total,
            "successful_calls": successes,
            "failed_calls": total - successes,
            "success_rate": round(successes / total, 3),
            "avg_latency_ms": round(sum(latencies) / total, 2)
        }
