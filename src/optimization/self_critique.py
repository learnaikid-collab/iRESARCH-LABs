"""
Self-Critique Optimizer - PromptWizard methodology.

Implements iterative self-critique and refinement.
"""

import logging
from typing import List, Dict, Any

from src.core.llm_engine import LLMEngine
from src.core.task_analyzer import TaskAnalysis

logger = logging.getLogger(__name__)


class SelfCritiqueOptimizer:
    """
    Self-critique based optimization using PromptWizard methodology.
    
    The LLM evaluates and refines its own prompts based on
    quality criteria and self-assessment.
    """
    
    def __init__(
        self,
        engine: LLMEngine,
        critique_rounds: int = 3,
        quality_threshold: float = 0.85,
    ):
        """Initialize the Self-Critique Optimizer."""
        self.engine = engine
        self.critique_rounds = critique_rounds
        self.quality_threshold = quality_threshold
        
        logger.info(
            f"Self-Critique Optimizer initialized: "
            f"rounds={critique_rounds}, threshold={quality_threshold}"
        )
    
    def optimize(
        self,
        initial_prompt: str,
        task_analysis: TaskAnalysis,
    ) -> str:
        """
        Optimize prompt using self-critique.
        
        Args:
            initial_prompt: Starting prompt
            task_analysis: Task analysis
            
        Returns:
            Optimized prompt
        """
        logger.info("Starting self-critique optimization")
        
        current_prompt = initial_prompt
        
        for round_num in range(self.critique_rounds):
            logger.debug(f"Critique round {round_num + 1}/{self.critique_rounds}")
            
            # Self-critique
            critique = self._self_critique(current_prompt, task_analysis)
            
            # Self-refine
            refined_prompt = self._self_refine(
                current_prompt,
                critique,
                task_analysis
            )
            
            # Evaluate quality
            quality = self._evaluate_quality(refined_prompt, task_analysis)
            
            logger.debug(f"Quality score: {quality:.3f}")
            
            if quality >= self.quality_threshold:
                logger.info(f"Quality threshold reached at round {round_num + 1}")
                return refined_prompt
            
            current_prompt = refined_prompt
        
        logger.info("Self-critique optimization complete")
        return current_prompt
    
    def _self_critique(
        self,
        prompt: str,
        task_analysis: TaskAnalysis
    ) -> str:
        """Generate self-critique of the prompt."""
        critique_prompt = f"""Critically evaluate this prompt:

{prompt}

Task: {task_analysis.task_type.value}
Complexity: {task_analysis.complexity.value}

Evaluate on:
1. Clarity
2. Completeness
3. Relevance
4. Creativity (if applicable)
5. Safety

Provide specific critiques:"""
        
        try:
            result = self.engine.generate(critique_prompt, temperature=0.7)
            return result.text
        except:
            return "Unable to generate critique"
    
    def _self_refine(
        self,
        prompt: str,
        critique: str,
        task_analysis: TaskAnalysis
    ) -> str:
        """Refine prompt based on self-critique."""
        refine_prompt = f"""Improve this prompt based on the critique:

Original prompt:
{prompt}

Critique:
{critique}

Provide ONLY the improved prompt:"""
        
        try:
            result = self.engine.generate(refine_prompt, temperature=0.7)
            return result.text.strip()
        except:
            return prompt
    
    def _evaluate_quality(
        self,
        prompt: str,
        task_analysis: TaskAnalysis
    ) -> float:
        """Evaluate prompt quality."""
        eval_prompt = f"""Rate this prompt's quality (0.0-1.0): {prompt}

Provide only the numeric score:"""
        
        try:
            result = self.engine.generate(eval_prompt, temperature=0.3, max_tokens=10)
            return max(0.0, min(1.0, float(result.text.strip())))
        except:
            return 0.5
