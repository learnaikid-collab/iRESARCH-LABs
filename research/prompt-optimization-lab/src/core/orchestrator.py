"""
Orchestrator: Main coordinator for the prompt optimization system.
"""

from dataclasses import dataclass
from typing import Dict, Optional
from enum import Enum


class OptimizationStrategy(Enum):
    """Available optimization strategies."""
    AUTO = "auto"
    FAST = "fast"
    THOROUGH = "thorough"
    AGGRESSIVE = "aggressive"


@dataclass
class ExecutionConfig:
    """Configuration for execution."""
    max_iterations: int = 10
    max_time: float = 300.0  # seconds
    convergence_threshold: float = 0.01
    strategy: str = "auto"


@dataclass
class OptimizationResult:
    """Result of optimization process."""
    answer: str
    final_prompt: str
    iterations: int
    quality_score: float
    improvement: float
    time_elapsed: float
    sources: Optional[list] = None
    metadata: Dict = None


class PromptOptimizer:
    """
    Main orchestrator for prompt optimization.
    
    Coordinates all components to optimize prompts and generate
    high-quality responses.
    """
    
    def __init__(
        self,
        llm_engine,
        knowledge_system = None,
        optimization_strategy: str = "auto",
        max_iterations: int = 10
    ):
        """
        Initialize the prompt optimizer.
        
        Args:
            llm_engine: LLM engine instance
            knowledge_system: Optional RAG/search system
            optimization_strategy: Optimization approach
            max_iterations: Maximum optimization iterations
        """
        self.llm = llm_engine
        self.knowledge = knowledge_system
        self.config = ExecutionConfig(
            strategy=optimization_strategy,
            max_iterations=max_iterations
        )
        
        # Import components
        from .task_analyzer import TaskAnalyzer
        from .prompt_builder import PromptBuilder
        from .evaluator import OutputEvaluator
        
        self.task_analyzer = TaskAnalyzer()
        self.prompt_builder = PromptBuilder()
        self.evaluator = OutputEvaluator()
    
    def optimize_and_generate(
        self,
        query: str,
        user_preferences: Optional[Dict] = None,
        enable_web_search: bool = False,
        max_sources: int = 5
    ) -> OptimizationResult:
        """
        Main method: optimize prompt and generate response.
        
        Args:
            query: User query
            user_preferences: Optional preferences (style, length, etc.)
            enable_web_search: Whether to search web
            max_sources: Maximum sources to retrieve
            
        Returns:
            OptimizationResult with answer and metadata
        """
        import time
        start_time = time.time()
        
        # Step 1: Analyze task
        analysis = self.task_analyzer.analyze_query(query)
        
        # Step 2: Retrieve knowledge if needed
        context = {}
        sources = []
        if enable_web_search or analysis.requires_web_search:
            if self.knowledge:
                # Would retrieve documents
                sources = []  # Placeholder
                context['sources'] = sources
        
        # Step 3: Build initial prompt
        initial_prompt = self.prompt_builder.build_prompt_zero(
            query, analysis, context
        )
        
        # Step 4: Generate initial output
        initial_output = self.llm.generate(initial_prompt)
        initial_eval = self.evaluator.evaluate_output(
            initial_output.text, query, initial_prompt, context
        )
        
        # Step 5: Optimization loop
        best_prompt = initial_prompt
        best_output = initial_output.text
        best_score = initial_eval.overall_score
        
        iterations = 1
        improvement = 0.0
        
        # Simple optimization: try refinement if not good enough
        if best_score < 0.9 and iterations < self.config.max_iterations:
            # Would call optimizer here
            # For now, just use initial result
            pass
        
        # Calculate metrics
        time_elapsed = time.time() - start_time
        improvement = (best_score - initial_eval.overall_score) / max(initial_eval.overall_score, 0.01)
        
        return OptimizationResult(
            answer=best_output,
            final_prompt=str(best_prompt),
            iterations=iterations,
            quality_score=best_score,
            improvement=improvement,
            time_elapsed=time_elapsed,
            sources=sources if sources else None,
            metadata={
                'task_type': analysis.task_type.value,
                'complexity': analysis.complexity.value,
                'strategy': self.config.strategy
            }
        )
    
    def __repr__(self) -> str:
        return f"PromptOptimizer(llm={self.llm}, strategy={self.config.strategy})"
