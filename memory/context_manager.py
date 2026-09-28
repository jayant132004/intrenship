"""
Short-Term Working Context Manager for ARA-1.
Manages working memory buffer, token allocation budgets, and recursive
context summarization when approaching token capacity limits.
"""

from typing import Dict, Any, List


class ContextManager:
    """
    Manages prompt token budgeting and working context window for the agent.
    """

    def __init__(self, max_context_tokens: int = 128000, compression_threshold_ratio: float = 0.75):
        self.max_context_tokens = max_context_tokens
        self.compression_threshold = int(max_context_tokens * compression_threshold_ratio)
        self.working_buffer: List[Dict[str, Any]] = []
        self.accumulated_findings: Dict[str, Any] = {}

    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation (approx 4 chars per token)."""
        return max(1, len(text) // 4)

    def add_observation(self, tool_name: str, query_args: Dict[str, Any], observation_data: Any):
        """Append an observation to short-term working context."""
        entry = {
            "step": len(self.working_buffer) + 1,
            "tool": tool_name,
            "args": query_args,
            "observation": observation_data
        }
        self.working_buffer.append(entry)
        self.accumulated_findings[tool_name] = observation_data

    def get_total_working_tokens(self) -> int:
        """Calculate total token consumption in current working context."""
        raw_text = str(self.working_buffer)
        return self.estimate_tokens(raw_text)

    def should_compress(self) -> bool:
        """Check if working context exceeds compression threshold."""
        return self.get_total_working_tokens() > self.compression_threshold

    def compress_context(self) -> str:
        """
        Compress older observations into high-density analytical bullet points.
        """
        summary_lines = ["### Compressed Working Context Summary:"]
        for item in self.working_buffer:
            tool = item["tool"]
            obs = str(item["observation"])
            preview = obs[:180].replace("\n", " ")
            summary_lines.append(f"- **Step {item['step']} ({tool})**: {preview}...")
        return "\n".join(summary_lines)

    def get_context_snapshot(self) -> Dict[str, Any]:
        """Return snapshot of current working memory."""
        return {
            "steps_recorded": len(self.working_buffer),
            "estimated_tokens": self.get_total_working_tokens(),
            "findings_keys": list(self.accumulated_findings.keys()),
            "buffer": self.working_buffer
        }
