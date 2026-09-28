"""
Error Handler and Graceful Degradation Coordinator for ARA-1.
Implements exponential backoff retries, error categorization, fallback routing,
and graceful degradation reporting.
"""

import time
import logging
from typing import Dict, Any, Callable, Optional, List
from agent.circuit_breaker import CircuitBreaker
from agent.fallback_chains import FallbackChains

logger = logging.getLogger(__name__)


class AgentErrorHandler:
    """
    Coordinates retries, circuit breakers, and fallback invocations for the agent.
    """

    def __init__(self, max_retries: int = 3, base_backoff_sec: float = 0.5):
        self.max_retries = max_retries
        self.base_backoff_sec = base_backoff_sec
        self.circuit_breaker = CircuitBreaker()
        self.fallback_chains = FallbackChains()
        self.degradation_log: List[str] = []

    def execute_with_resilience(
        self,
        tool_name: str,
        tool_dispatcher: Callable[[str], Dict[str, Any]],
        **tool_args
    ) -> Dict[str, Any]:
        """
        Execute tool with circuit-breaker checks, retries, and fallback chains.
        """
        # 1. Check Circuit Breaker
        if not self.circuit_breaker.can_execute(tool_name):
            logger.warning(f"Circuit OPEN for '{tool_name}'. Executing fallback chain immediately.")
            return self._execute_fallback(tool_name, tool_dispatcher, **tool_args)

        # 2. Attempt Execution with Retries & Exponential Backoff
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            result = tool_dispatcher(tool_name, **tool_args)
            if result.get("status") in ["success", "partial_success"]:
                self.circuit_breaker.record_success(tool_name)
                return result

            # Failed attempt
            last_error = result.get("message", "Unknown execution failure")
            logger.warning(f"Tool '{tool_name}' attempt {attempt}/{self.max_retries} failed: {last_error}")
            if attempt < self.max_retries:
                time.sleep(self.base_backoff_sec * (2 ** (attempt - 1)))

        # 3. Trip circuit breaker and route to fallback
        self.circuit_breaker.record_failure(tool_name)
        return self._execute_fallback(tool_name, tool_dispatcher, **tool_args)

    def _execute_fallback(
        self,
        primary_tool: str,
        tool_dispatcher: Callable,
        **tool_args
    ) -> Dict[str, Any]:
        """Iterate through designated fallback tool chains."""
        fallbacks = self.fallback_chains.get_fallbacks_for_tool(primary_tool)
        for fb in fallbacks:
            fb_tool = fb["tool"]
            transformer = fb.get("transform", lambda x: x)
            try:
                transformed_args = transformer(tool_args)
                logger.info(f"Invoking fallback tool '{fb_tool}' for failed primary '{primary_tool}'.")
                fb_result = tool_dispatcher(fb_tool, **transformed_args)
                if fb_result.get("status") in ["success", "partial_success"]:
                    fb_result["fallback_from"] = primary_tool
                    fb_result["degraded"] = True
                    notice = f"Primary tool '{primary_tool}' degraded; recovered using fallback '{fb_tool}'."
                    self.degradation_log.append(notice)
                    return fb_result
            except Exception as e:
                logger.warning(f"Fallback '{fb_tool}' failed: {e}")

        # Graceful degradation failure return
        degradation_notice = f"Data limitation: Primary tool '{primary_tool}' and all fallbacks failed. Analysis proceeding with gaps."
        self.degradation_log.append(degradation_notice)
        return {
            "status": "graceful_degradation",
            "primary_tool": primary_tool,
            "message": degradation_notice,
            "data": {"notice": "Data unavailable from primary sources.", "verified": False}
        }
