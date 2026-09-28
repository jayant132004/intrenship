"""
Evaluation package for ARA-1.
"""

from .metrics import EvaluationFramework
from .dashboard import render_terminal_dashboard

__all__ = ["EvaluationFramework", "render_terminal_dashboard"]
