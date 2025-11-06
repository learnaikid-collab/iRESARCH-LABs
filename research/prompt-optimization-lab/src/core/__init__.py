"""
Core components for the Advanced Prompt Optimization System.

This module provides the foundational classes and interfaces for:
- Task analysis and classification
- Prompt construction and manipulation
- LLM inference and interaction
- Output evaluation and scoring
- Main orchestration logic
"""

from .task_analyzer import TaskAnalyzer, TaskAnalysis, TaskType, ComplexityLevel
from .prompt_builder import PromptBuilder, Prompt, PromptTemplate
from .llm_engine import LLMEngine, LLMResponse, LLMConfig
from .evaluator import OutputEvaluator, EvaluationResult, Critique
from .orchestrator import PromptOptimizer, OptimizationResult, ExecutionConfig

__all__ = [
    # Task Analysis
    'TaskAnalyzer',
    'TaskAnalysis',
    'TaskType',
    'ComplexityLevel',
    
    # Prompt Building
    'PromptBuilder',
    'Prompt',
    'PromptTemplate',
    
    # LLM Interaction
    'LLMEngine',
    'LLMResponse',
    'LLMConfig',
    
    # Evaluation
    'OutputEvaluator',
    'EvaluationResult',
    'Critique',
    
    # Orchestration
    'PromptOptimizer',
    'OptimizationResult',
    'ExecutionConfig',
]

__version__ = '0.1.0'
__author__ = 'iRESARCH-LABs'
