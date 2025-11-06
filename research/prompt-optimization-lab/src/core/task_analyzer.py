"""
Task Analyzer: Analyzes user queries to determine optimal processing strategy.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional
import re


class TaskType(Enum):
    """Categories of tasks."""
    FACTUAL = "factual"  # Fact-based questions
    REASONING = "reasoning"  # Logic, math, complex reasoning
    CREATIVE = "creative"  # Writing, brainstorming
    CODING = "coding"  # Programming tasks
    ANALYSIS = "analysis"  # Data analysis, interpretation
    CONVERSATIONAL = "conversational"  # Chat, dialogue
    INSTRUCTION = "instruction"  # How-to, step-by-step
    SUMMARIZATION = "summarization"  # Condensing information
    TRANSLATION = "translation"  # Language translation
    CLASSIFICATION = "classification"  # Categorization tasks


class ComplexityLevel(Enum):
    """Task complexity levels."""
    SIMPLE = "simple"  # Single-step, straightforward
    MODERATE = "moderate"  # Multi-step, some reasoning
    COMPLEX = "complex"  # Deep reasoning, multiple components
    EXPERT = "expert"  # Highly specialized, extensive analysis


@dataclass
class SafetyReport:
    """Safety analysis of a query."""
    is_safe: bool
    flags: List[str]
    sensitivity_level: str  # 'low', 'medium', 'high'
    recommendations: List[str]


@dataclass
class TaskAnalysis:
    """Complete analysis of a user query."""
    query: str
    task_type: TaskType
    complexity: ComplexityLevel
    requires_web_search: bool
    requires_reasoning: bool
    requires_examples: bool
    estimated_tokens: int
    safety_report: SafetyReport
    recommended_strategy: str
    metadata: Dict


class TaskAnalyzer:
    """Analyzes queries to determine optimal processing approach."""
    
    def __init__(self):
        # Keywords for task classification
        self.factual_keywords = [
            'what is', 'who is', 'when did', 'where is',
            'define', 'explain', 'describe'
        ]
        self.reasoning_keywords = [
            'why', 'how does', 'analyze', 'compare',
            'evaluate', 'calculate', 'solve', 'prove'
        ]
        self.creative_keywords = [
            'write', 'create', 'generate', 'imagine',
            'design', 'compose', 'brainstorm'
        ]
        self.coding_keywords = [
            'code', 'program', 'function', 'algorithm',
            'debug', 'implement', 'script'
        ]
        
        # Complexity indicators
        self.complexity_indicators = {
            'simple': ['simple', 'basic', 'quick', 'briefly'],
            'moderate': ['explain', 'describe', 'how', 'why'],
            'complex': ['comprehensive', 'detailed', 'analyze', 'compare'],
            'expert': ['research', 'advanced', 'technical', 'in-depth']
        }
        
    def analyze_query(self, query: str, context: Optional[Dict] = None) -> TaskAnalysis:
        """
        Perform comprehensive query analysis.
        
        Args:
            query: User query string
            context: Optional context information
            
        Returns:
            TaskAnalysis object with all analysis results
        """
        # Classify task type
        task_type = self.classify_task_type(query)
        
        # Assess complexity
        complexity = self.estimate_complexity(query)
        
        # Check if web search is needed
        requires_web_search = self._needs_web_search(query)
        
        # Check if reasoning is required
        requires_reasoning = self._needs_reasoning(query, task_type)
        
        # Check if examples would help
        requires_examples = self._benefits_from_examples(query, task_type)
        
        # Estimate token requirements
        estimated_tokens = self._estimate_tokens(query, complexity)
        
        # Safety analysis
        safety_report = self.check_safety_flags(query)
        
        # Recommend optimization strategy
        recommended_strategy = self._recommend_strategy(
            task_type, complexity, requires_reasoning
        )
        
        return TaskAnalysis(
            query=query,
            task_type=task_type,
            complexity=complexity,
            requires_web_search=requires_web_search,
            requires_reasoning=requires_reasoning,
            requires_examples=requires_examples,
            estimated_tokens=estimated_tokens,
            safety_report=safety_report,
            recommended_strategy=recommended_strategy,
            metadata=context or {}
        )
    
    def classify_task_type(self, query: str) -> TaskType:
        """
        Determine the primary task type.
        
        Args:
            query: User query
            
        Returns:
            TaskType enum value
        """
        query_lower = query.lower()
        
        # Check for coding tasks
        if any(kw in query_lower for kw in self.coding_keywords):
            return TaskType.CODING
        
        # Check for creative tasks
        if any(kw in query_lower for kw in self.creative_keywords):
            return TaskType.CREATIVE
        
        # Check for reasoning tasks
        if any(kw in query_lower for kw in self.reasoning_keywords):
            return TaskType.REASONING
        
        # Check for factual queries
        if any(kw in query_lower for kw in self.factual_keywords):
            return TaskType.FACTUAL
        
        # Check for summarization
        if 'summarize' in query_lower or 'summary' in query_lower:
            return TaskType.SUMMARIZATION
        
        # Check for translation
        if 'translate' in query_lower:
            return TaskType.TRANSLATION
        
        # Default to conversational
        return TaskType.CONVERSATIONAL
    
    def estimate_complexity(self, query: str) -> ComplexityLevel:
        """
        Estimate task complexity.
        
        Args:
            query: User query
            
        Returns:
            ComplexityLevel enum value
        """
        query_lower = query.lower()
        
        # Score based on indicators
        scores = {level: 0 for level in ComplexityLevel}
        
        for level, keywords in self.complexity_indicators.items():
            for keyword in keywords:
                if keyword in query_lower:
                    if level == 'simple':
                        scores[ComplexityLevel.SIMPLE] += 1
                    elif level == 'moderate':
                        scores[ComplexityLevel.MODERATE] += 1
                    elif level == 'complex':
                        scores[ComplexityLevel.COMPLEX] += 1
                    elif level == 'expert':
                        scores[ComplexityLevel.EXPERT] += 1
        
        # Consider query length
        word_count = len(query.split())
        if word_count > 50:
            scores[ComplexityLevel.COMPLEX] += 2
        elif word_count > 20:
            scores[ComplexityLevel.MODERATE] += 1
        
        # Consider questions
        question_marks = query.count('?')
        if question_marks > 2:
            scores[ComplexityLevel.COMPLEX] += 1
        
        # Return highest scoring complexity
        if scores[ComplexityLevel.EXPERT] > 0:
            return ComplexityLevel.EXPERT
        elif scores[ComplexityLevel.COMPLEX] > scores[ComplexityLevel.MODERATE]:
            return ComplexityLevel.COMPLEX
        elif scores[ComplexityLevel.MODERATE] > 0 or word_count > 10:
            return ComplexityLevel.MODERATE
        else:
            return ComplexityLevel.SIMPLE
    
    def check_safety_flags(self, query: str) -> SafetyReport:
        """
        Analyze query for safety concerns.
        
        Args:
            query: User query
            
        Returns:
            SafetyReport with analysis
        """
        flags = []
        sensitivity_level = 'low'
        recommendations = []
        
        query_lower = query.lower()
        
        # Check for potentially sensitive topics
        sensitive_keywords = [
            'violence', 'harm', 'illegal', 'weapon',
            'drug', 'hack', 'exploit', 'malware'
        ]
        
        for keyword in sensitive_keywords:
            if keyword in query_lower:
                flags.append(f"Contains keyword: {keyword}")
                sensitivity_level = 'medium'
        
        # Medical/legal advice
        if any(kw in query_lower for kw in ['medical', 'legal', 'financial advice']):
            flags.append("May require professional disclaimer")
            sensitivity_level = 'medium'
            recommendations.append("Add appropriate disclaimer")
        
        # Determine if safe
        is_safe = sensitivity_level != 'high'
        
        # Add recommendations based on sensitivity
        if sensitivity_level == 'medium':
            recommendations.append("Consider adding context or clarification")
            recommendations.append("Ensure response includes appropriate caveats")
        
        return SafetyReport(
            is_safe=is_safe,
            flags=flags,
            sensitivity_level=sensitivity_level,
            recommendations=recommendations
        )
    
    def _needs_web_search(self, query: str) -> bool:
        """Check if query requires current information."""
        current_keywords = [
            'latest', 'recent', 'current', 'today',
            'now', 'this year', '2024', '2025'
        ]
        return any(kw in query.lower() for kw in current_keywords)
    
    def _needs_reasoning(self, query: str, task_type: TaskType) -> bool:
        """Determine if chain-of-thought reasoning would help."""
        reasoning_tasks = [
            TaskType.REASONING,
            TaskType.ANALYSIS,
            TaskType.CODING
        ]
        return task_type in reasoning_tasks or 'why' in query.lower()
    
    def _benefits_from_examples(self, query: str, task_type: TaskType) -> bool:
        """Check if few-shot examples would improve results."""
        example_beneficial_tasks = [
            TaskType.CODING,
            TaskType.CREATIVE,
            TaskType.CLASSIFICATION,
            TaskType.TRANSLATION
        ]
        return task_type in example_beneficial_tasks
    
    def _estimate_tokens(self, query: str, complexity: ComplexityLevel) -> int:
        """Estimate token requirements for response."""
        base_tokens = {
            ComplexityLevel.SIMPLE: 200,
            ComplexityLevel.MODERATE: 500,
            ComplexityLevel.COMPLEX: 1000,
            ComplexityLevel.EXPERT: 2000
        }
        
        # Add query tokens (rough estimate: 1.3 tokens per word)
        query_tokens = int(len(query.split()) * 1.3)
        
        return base_tokens[complexity] + query_tokens
    
    def _recommend_strategy(
        self,
        task_type: TaskType,
        complexity: ComplexityLevel,
        requires_reasoning: bool
    ) -> str:
        """Recommend optimization strategy based on analysis."""
        
        # Simple tasks -> fast optimization
        if complexity == ComplexityLevel.SIMPLE:
            return 'self_critique'
        
        # Complex reasoning -> mesa-optimization
        if requires_reasoning and complexity in [ComplexityLevel.COMPLEX, ComplexityLevel.EXPERT]:
            return 'mesa_optimization'
        
        # Creative tasks -> evolutionary
        if task_type == TaskType.CREATIVE:
            return 'evolutionary'
        
        # Coding tasks -> RL optimization
        if task_type == TaskType.CODING:
            return 'rl'
        
        # Default to self-critique for moderate tasks
        return 'self_critique'
