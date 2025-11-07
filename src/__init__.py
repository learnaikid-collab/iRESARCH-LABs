"""
Advanced Prompt Optimization System (APOS)

A comprehensive framework for automated prompt engineering and optimization.
"""

__version__ = "0.1.0"
__author__ = "iRESARCH-LABs Team"

from src.core import LLMEngine, TaskAnalyzer, PromptBuilder
from src.optimization import MesaOptimizer

__all__ = [
    "LLMEngine",
    "TaskAnalyzer", 
    "PromptBuilder",
    "MesaOptimizer",
]
