"""
Circuit Breaker Pattern Implementation for ARA-1.
Prevents cascading API failures by automatically tripping when an endpoint
experiences repeated faults and diverting to fallback handlers.
"""

import time
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class CircuitBreaker:
    """
    Tracks failure rates per tool and enforces state transitions (CLOSED, OPEN, HALF_OPEN).
    """

    def __init__(self, failure_threshold: int = 3, recovery_timeout_sec: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout_sec
        # State per tool: {tool_name: {"state": "CLOSED", "failures": 0, "last_failure_time": 0.0}}
        self.tool_states: Dict[str, Dict[str, Any]] = {}

    def _get_state(self, tool_name: str) -> Dict[str, Any]:
        if tool_name not in self.tool_states:
            self.tool_states[tool_name] = {
                "state": "CLOSED",
                "failures": 0,
                "last_failure_time": 0.0,
                "tripped_count": 0
            }
        return self.tool_states[tool_name]

    def can_execute(self, tool_name: str) -> bool:
        """Check if the tool's circuit is currently allowed to execute."""
        st = self._get_state(tool_name)
        if st["state"] == "CLOSED":
            return True

        if st["state"] == "OPEN":
            # Check if recovery timeout has elapsed
            if time.time() - st["last_failure_time"] > self.recovery_timeout:
                logger.info(f"Circuit Breaker for '{tool_name}' transitioned to HALF_OPEN (probing recovery).")
                st["state"] = "HALF_OPEN"
                return True
            return False

        if st["state"] == "HALF_OPEN":
            return True

        return True

    def record_success(self, tool_name: str):
        """Record a successful tool execution and reset failure counters."""
        st = self._get_state(tool_name)
        if st["state"] in ["HALF_OPEN", "OPEN"]:
            logger.info(f"Circuit Breaker for '{tool_name}' recovered and closed successfully.")
        st["state"] = "CLOSED"
        st["failures"] = 0

    def record_failure(self, tool_name: str) -> bool:
        """
        Record a failure. If failures >= threshold, trip circuit to OPEN.
        Returns True if circuit was tripped.
        """
        st = self._get_state(tool_name)
        st["failures"] += 1
        st["last_failure_time"] = time.time()

        if st["failures"] >= self.failure_threshold:
            st["state"] = "OPEN"
            st["tripped_count"] += 1
            logger.warning(
                f"🚨 Circuit Breaker TRIPPED for tool '{tool_name}' after {st['failures']} consecutive failures! "
                f"Routing all calls to Fallback Chains."
            )
            return True
        return False
