"""
Output Evaluator: Assesses quality and alignment of generated outputs.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Critique:
    """Critique of model output."""
    is_satisfactory: bool
    issues: List[str]
    suggestions: List[str]
    priority_fixes: List[str]
    score: float


@dataclass
class EvaluationResult:
    """Complete evaluation of an output."""
    overall_score: float
    quality_score: float
    alignment_score: float
    factuality_score: float
    safety_score: float
    reward: float
    feedback: str
    critique: Optional[Critique] = None
    metadata: Dict = None


class OutputEvaluator:
    """Evaluates LLM outputs across multiple dimensions."""
    
    def __init__(self):
        self.weights = {
            'quality': 0.3,
            'alignment': 0.3,
            'factuality': 0.2,
            'safety': 0.2
        }
    
    def evaluate_output(
        self,
        output: str,
        query: str,
        prompt = None,
        context: Optional[Dict] = None
    ) -> EvaluationResult:
        """
        Comprehensive output evaluation.
        
        Args:
            output: Generated text
            query: Original query
            prompt: Prompt used (optional)
            context: Additional context (optional)
            
        Returns:
            EvaluationResult with scores and feedback
        """
        # Evaluate different dimensions
        quality_score = self._assess_quality(output, query)
        alignment_score = self._check_alignment(output, query)
        factuality_score = self._verify_facts(output, context)
        safety_score = self._safety_score(output)
        
        # Compute overall score
        overall = (
            quality_score * self.weights['quality'] +
            alignment_score * self.weights['alignment'] +
            factuality_score * self.weights['factuality'] +
            safety_score * self.weights['safety']
        )
        
        # Compute reward (for optimization)
        reward = self._compute_reward(overall, quality_score, alignment_score)
        
        # Generate feedback
        feedback = self._generate_feedback(
            quality_score,
            alignment_score,
            factuality_score,
            safety_score
        )
        
        return EvaluationResult(
            overall_score=overall,
            quality_score=quality_score,
            alignment_score=alignment_score,
            factuality_score=factuality_score,
            safety_score=safety_score,
            reward=reward,
            feedback=feedback,
            metadata={
                'output_length': len(output),
                'query_length': len(query)
            }
        )
    
    def _assess_quality(self, output: str, query: str) -> float:
        """Assess output quality (completeness, coherence, etc.)."""
        score = 0.5  # Base score
        
        # Check if output is not empty
        if len(output.strip()) > 0:
            score += 0.2
        
        # Check reasonable length
        if 50 < len(output) < 5000:
            score += 0.2
        
        # Check if it addresses the query (simple keyword overlap)
        query_words = set(query.lower().split())
        output_words = set(output.lower().split())
        overlap = len(query_words & output_words) / max(len(query_words), 1)
        score += min(overlap * 0.1, 0.1)
        
        return min(score, 1.0)
    
    def _check_alignment(self, output: str, query: str) -> float:
        """Check alignment with user's intent."""
        # Simplified alignment check
        score = 0.7  # Baseline
        
        # Check if output is responsive
        if len(output) > 20:
            score += 0.2
        
        # Check for question marks if query asks a question
        if '?' in query and ('.' in output or '!' in output):
            score += 0.1
        
        return min(score, 1.0)
    
    def _verify_facts(self, output: str, context: Optional[Dict]) -> float:
        """Verify factual consistency."""
        # Placeholder - would check against sources
        score = 0.8  # Assume mostly accurate
        
        if context and 'sources' in context:
            # Would compare output claims with sources
            pass
        
        return score
    
    def _safety_score(self, output: str) -> float:
        """Check safety of output."""
        # Simplified safety check
        unsafe_keywords = [
            'harm', 'violence', 'illegal', 'dangerous'
        ]
        
        score = 1.0
        output_lower = output.lower()
        
        for keyword in unsafe_keywords:
            if keyword in output_lower:
                score -= 0.1
        
        return max(score, 0.0)
    
    def _compute_reward(
        self,
        overall: float,
        quality: float,
        alignment: float
    ) -> float:
        """Compute reward signal for optimization."""
        # Emphasize alignment and quality
        return (alignment * 0.5 + quality * 0.3 + overall * 0.2)
    
    def _generate_feedback(
        self,
        quality: float,
        alignment: float,
        factuality: float,
        safety: float
    ) -> str:
        """Generate human-readable feedback."""
        feedback_parts = []
        
        if quality < 0.6:
            feedback_parts.append("Output quality could be improved")
        if alignment < 0.6:
            feedback_parts.append("Better alignment with user intent needed")
        if factuality < 0.7:
            feedback_parts.append("Factual accuracy should be verified")
        if safety < 0.9:
            feedback_parts.append("Safety concerns detected")
        
        if not feedback_parts:
            return "Output meets quality standards"
        
        return "; ".join(feedback_parts)


class RewardModel:
    """Predicts user satisfaction (for RL optimization)."""
    
    def __init__(self):
        # Would load trained model
        pass
    
    def predict(self, output: str, query: str) -> float:
        """
        Predict user satisfaction score.
        
        Args:
            output: Generated text
            query: User query
            
        Returns:
            Predicted satisfaction score [0, 1]
        """
        # Placeholder - would use trained model
        evaluator = OutputEvaluator()
        result = evaluator.evaluate_output(output, query)
        return result.reward
