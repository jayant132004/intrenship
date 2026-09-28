"""
Reasoning Trace and Tool Call Parser for ARA-1.
Extracts Thought, Action, Action Input, and Final Report blocks from LLM outputs.
"""

import re
import json
import logging
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)


class AgentOutputParser:
    """
    Parses LLM reasoning text into structured action steps or final conclusions.
    """

    def parse_step(self, text: str) -> Dict[str, Any]:
        """
        Parse raw agent generation into a structured thought/action object.
        """
        # Look for Final Answer / Report
        if "Final Report:" in text or "Final Answer:" in text:
            parts = re.split(r"Final (?:Report|Answer):", text, flags=re.IGNORECASE)
            thought = parts[0].replace("Thought:", "").strip() if len(parts) > 1 else ""
            report = parts[-1].strip()
            return {
                "type": "finish",
                "thought": thought,
                "final_output": report
            }

        # Look for Action & Action Input
        thought_match = re.search(r"Thought:\s*(.*?)(?=Action:|$)", text, re.DOTALL | re.IGNORECASE)
        action_match = re.search(r"Action:\s*([a-zA-Z0-9_]+)", text, re.IGNORECASE)
        input_match = re.search(r"Action Input:\s*(\{.*?\})", text, re.DOTALL | re.IGNORECASE)

        thought = thought_match.group(1).strip() if thought_match else ""
        action = action_match.group(1).strip() if action_match else None
        action_input = {}

        if input_match:
            try:
                action_input = json.loads(input_match.group(1))
            except json.JSONDecodeError:
                action_input = {"raw_input": input_match.group(1)}

        if action:
            return {
                "type": "action",
                "thought": thought,
                "tool": action,
                "tool_input": action_input
            }

        return {
            "type": "continue",
            "thought": text.strip(),
            "final_output": text.strip()
        }
