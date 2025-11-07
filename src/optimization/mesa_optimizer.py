"""
Mesa Optimizer - Inner-loop optimization with user-aligned rewards.

Implements meta-learning optimization where the LLM acts as an inner
optimizer that learns to improve prompts through iterative refinement.
"""

import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
import time

from src.core.llm_engine import LLMEngine
from src.core.task_analyzer import TaskAnalysis

logger = logging.getLogger(__name__)


@dataclass
class OptimizationResult:
    """Result of prompt optimization."""
    optimized_prompt: str
    original_prompt: str
    iterations: int
    final_score: float
    improvement: float
    history: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RewardWeights:
    """Weights for different reward components."""
    quality: float = 0.4
    alignment: float = 0.3
    efficiency: float = 0.2
    safety: float = 0.1


class MesaOptimizer:
    """
    Mesa-style optimizer using the LLM as an inner optimizer.
    
    The optimizer treats prompt improvement as a meta-learning problem,
    where the LLM learns to optimize prompts based on user-aligned
    reward signals.
    
    Features:
    - Iterative prompt refinement
    - User-aligned reward modeling
    - Early stopping based on convergence
    - Performance tracking
    """
    
    def __init__(
        self,
        engine: LLMEngine,
        max_iterations: int = 10,
        learning_rate: float = 0.01,
        convergence_threshold: float = 0.95,
        reward_weights: Optional[RewardWeights] = None,
    ):
        """
        Initialize the Mesa Optimizer.
        
        Args:
            engine: LLM engine for generation
            max_iterations: Maximum optimization iterations
            learning_rate: Learning rate for updates (currently informational)
            convergence_threshold: Score threshold for convergence
            reward_weights: Weights for reward components
        """
        self.engine = engine
        self.max_iterations = max_iterations
        self.learning_rate = learning_rate
        self.convergence_threshold = convergence_threshold
        self.reward_weights = reward_weights or RewardWeights()
        
        logger.info(
            f"Mesa Optimizer initialized: max_iter={max_iterations}, "
            f"threshold={convergence_threshold}"
        )
    
    def optimize(
        self,
        initial_prompt: str,
        task_analysis: TaskAnalysis,
        objective: Optional[str] = None,
        early_stopping: bool = True,
    ) -> OptimizationResult:
        """
        Optimize a prompt using Mesa optimization.
        
        Args:
            initial_prompt: Starting prompt
            task_analysis: Analysis of the task
            objective: Optional specific optimization objective
            early_stopping: Whether to stop early on convergence
            
        Returns:
            OptimizationResult with optimized prompt and metadata
        """
        logger.info("Starting Mesa optimization")
        start_time = time.time()
        
        current_prompt = initial_prompt
        history = []
        best_prompt = initial_prompt
        best_score = 0.0
        
        for iteration in range(self.max_iterations):
            logger.debug(f"Iteration {iteration + 1}/{self.max_iterations}")
            
            # Generate critique and improvement
            critique = self._generate_critique(
                current_prompt,
                task_analysis,
                objective
            )
            
            # Generate improved prompt
            improved_prompt = self._generate_improvement(
                current_prompt,
                critique,
                task_analysis
            )
            
            # Evaluate the improved prompt
            score = self._evaluate_prompt(
                improved_prompt,
                task_analysis,
                objective
            )
            
            # Record iteration
            history.append({
                "iteration": iteration + 1,
                "prompt": improved_prompt,
                "score": score,
                "critique": critique,
                "timestamp": time.time() - start_time,
            })
            
            # Update best if improved
            if score > best_score:
                best_score = score
                best_prompt = improved_prompt
                logger.debug(f"New best score: {best_score:.3f}")
            
            # Check convergence
            if early_stopping and score >= self.convergence_threshold:
                logger.info(
                    f"Converged at iteration {iteration + 1} "
                    f"with score {score:.3f}"
                )
                break
            
            # Update current prompt for next iteration
            current_prompt = improved_prompt
        
        # Calculate improvement
        initial_score = self._evaluate_prompt(
            initial_prompt,
            task_analysis,
            objective
        )
        improvement = best_score - initial_score
        
        elapsed_time = time.time() - start_time
        
        result = OptimizationResult(
            optimized_prompt=best_prompt,
            original_prompt=initial_prompt,
            iterations=len(history),
            final_score=best_score,
            improvement=improvement,
            history=history,
            metadata={
                "optimization_time": elapsed_time,
                "initial_score": initial_score,
                "converged": best_score >= self.convergence_threshold,
            }
        )
        
        logger.info(
            f"Optimization complete: {len(history)} iterations, "
            f"score={best_score:.3f}, improvement={improvement:.3f}, "
            f"time={elapsed_time:.2f}s"
        )
        
        return result
    
    def _generate_critique(
        self,
        prompt: str,
        task_analysis: TaskAnalysis,
        objective: Optional[str] = None
    ) -> str:
        """Generate critique of the current prompt."""
        critique_prompt = f"""Analyze the following prompt and provide constructive critique:

Prompt to analyze:
{prompt}

Task type: {task_analysis.task_type.value}
Complexity: {task_analysis.complexity.value}
{f"Objective: {objective}" if objective else ""}

Critique the prompt on these dimensions:
1. Clarity and specificity
2. Task alignment
3. Completeness of instructions
4. Potential for high-quality responses
5. Safety and appropriateness

Provide specific, actionable feedback for improvement.

Critique:"""
        
        try:
            result = self.engine.generate(
                critique_prompt,
                temperature=0.7,
                max_tokens=500
            )
            return result.text
        except Exception as e:
            logger.error(f"Error generating critique: {str(e)}")
            return "Unable to generate critique."
    
    def _generate_improvement(
        self,
        current_prompt: str,
        critique: str,
        task_analysis: TaskAnalysis
    ) -> str:
        """Generate improved prompt based on critique."""
        improvement_prompt = f"""Given this prompt and critique, create an improved version.

Current prompt:
{current_prompt}

Critique:
{critique}

Task context:
- Type: {task_analysis.task_type.value}
- Complexity: {task_analysis.complexity.value}
- Domain: {task_analysis.domain}

Create an improved version that addresses the critique while maintaining the original intent.
Provide ONLY the improved prompt, without any explanation.

Improved prompt:"""
        
        try:
            result = self.engine.generate(
                improvement_prompt,
                temperature=0.7,
                max_tokens=1000
            )
            return result.text.strip()
        except Exception as e:
            logger.error(f"Error generating improvement: {str(e)}")
            return current_prompt
    
    def _evaluate_prompt(
        self,
        prompt: str,
        task_analysis: TaskAnalysis,
        objective: Optional[str] = None
    ) -> float:
        """
        Evaluate a prompt using user-aligned reward model.
        
        Returns a score between 0 and 1.
        """
        evaluation_prompt = f"""Evaluate the following prompt on a scale of 0 to 1.

Prompt to evaluate:
{prompt}

Task context:
- Type: {task_analysis.task_type.value}
- Complexity: {task_analysis.complexity.value}
{f"- Objective: {objective}" if objective else ""}

Evaluation criteria (weights):
- Quality of instructions ({self.reward_weights.quality}): Clear, specific, comprehensive
- User alignment ({self.reward_weights.alignment}): Matches user intent and needs
- Efficiency ({self.reward_weights.efficiency}): Concise yet complete
- Safety ({self.reward_weights.safety}): Appropriate and risk-aware

Provide a single score between 0.0 and 1.0, considering the weighted criteria.
Respond with ONLY the numeric score (e.g., 0.85).

Score:"""
        
        try:
            result = self.engine.generate(
                evaluation_prompt,
                temperature=0.3,  # Lower temperature for more consistent scoring
                max_tokens=10
            )
            
            # Extract score
            score_text = result.text.strip()
            # Try to parse the score
            score = float(score_text)
            
            # Clamp to [0, 1]
            score = max(0.0, min(1.0, score))
            
            return score
            
        except Exception as e:
            logger.error(f"Error evaluating prompt: {str(e)}")
            # Return a default middle score on error
            return 0.5
    
    def optimize_with_feedback(
        self,
        initial_prompt: str,
        task_analysis: TaskAnalysis,
        feedback_function: Callable[[str], float],
        max_iterations: Optional[int] = None,
    ) -> OptimizationResult:
        """
        Optimize using custom feedback function.
        
        Args:
            initial_prompt: Starting prompt
            task_analysis: Analysis of the task
            feedback_function: Function that scores prompts (returns 0-1)
            max_iterations: Override default max iterations
            
        Returns:
            OptimizationResult
        """
        iterations = max_iterations or self.max_iterations
        current_prompt = initial_prompt
        history = []
        best_prompt = initial_prompt
        best_score = feedback_function(initial_prompt)
        
        for iteration in range(iterations):
            # Generate improvement
            critique = self._generate_critique(
                current_prompt,
                task_analysis,
                None
            )
            improved_prompt = self._generate_improvement(
                current_prompt,
                critique,
                task_analysis
            )
            
            # Use custom feedback
            score = feedback_function(improved_prompt)
            
            history.append({
                "iteration": iteration + 1,
                "prompt": improved_prompt,
                "score": score,
            })
            
            if score > best_score:
                best_score = score
                best_prompt = improved_prompt
            
            if score >= self.convergence_threshold:
                break
            
            current_prompt = improved_prompt
        
        return OptimizationResult(
            optimized_prompt=best_prompt,
            original_prompt=initial_prompt,
            iterations=len(history),
            final_score=best_score,
            improvement=best_score - feedback_function(initial_prompt),
            history=history,
        )
