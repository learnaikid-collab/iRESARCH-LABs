"""
Task Analyzer for classifying and analyzing user requests.

Provides intelligent classification of tasks, complexity assessment,
and resource requirement determination.
"""

import logging
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class TaskType(Enum):
    """Types of tasks the system can handle."""
    CREATIVE_WRITING = "creative_writing"
    TECHNICAL_EXPLANATION = "technical_explanation"
    CODE_GENERATION = "code_generation"
    DATA_ANALYSIS = "data_analysis"
    QUESTION_ANSWERING = "question_answering"
    SUMMARIZATION = "summarization"
    TRANSLATION = "translation"
    REASONING = "reasoning"
    RESEARCH = "research"
    GENERAL = "general"


class ComplexityLevel(Enum):
    """Complexity levels for tasks."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    EXPERT = "expert"


@dataclass
class SafetyFlags:
    """Safety-related flags for a task."""
    has_sensitive_content: bool = False
    requires_fact_checking: bool = False
    potential_harm: bool = False
    privacy_concerns: bool = False
    needs_disclaimer: bool = False
    blocked_topics: List[str] = field(default_factory=list)


@dataclass
class TaskAnalysis:
    """Complete analysis of a user task."""
    task_type: TaskType
    complexity: ComplexityLevel
    estimated_tokens: int
    requires_research: bool
    requires_examples: bool
    safety_flags: SafetyFlags
    keywords: List[str]
    domain: str
    suggested_strategy: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class TaskAnalyzer:
    """
    Analyzes user requests to determine task characteristics.
    
    Features:
    - Task type classification
    - Complexity assessment
    - Safety flag detection
    - Resource requirement estimation
    - Optimization strategy suggestion
    """
    
    # Keywords for task classification
    TASK_KEYWORDS = {
        TaskType.CREATIVE_WRITING: [
            "write", "story", "creative", "poem", "narrative", "fiction",
            "character", "plot", "script", "novel"
        ],
        TaskType.TECHNICAL_EXPLANATION: [
            "explain", "how does", "what is", "describe", "technical",
            "architecture", "system", "mechanism", "principle"
        ],
        TaskType.CODE_GENERATION: [
            "code", "program", "function", "implement", "script",
            "algorithm", "class", "method", "api", "debug"
        ],
        TaskType.DATA_ANALYSIS: [
            "analyze", "data", "statistics", "trend", "pattern",
            "visualization", "metrics", "report", "insights"
        ],
        TaskType.QUESTION_ANSWERING: [
            "what", "when", "where", "who", "why", "how",
            "question", "answer", "?", "explain"
        ],
        TaskType.SUMMARIZATION: [
            "summarize", "summary", "brief", "overview", "highlights",
            "key points", "tldr", "abstract"
        ],
        TaskType.TRANSLATION: [
            "translate", "translation", "language", "convert to",
            "in spanish", "in french", "in german"
        ],
        TaskType.REASONING: [
            "solve", "reason", "logic", "proof", "derive",
            "calculate", "determine", "figure out"
        ],
        TaskType.RESEARCH: [
            "research", "investigate", "study", "review",
            "literature", "findings", "evidence", "sources"
        ],
    }
    
    # Blocked topics for safety
    BLOCKED_TOPICS = [
        "illegal activities", "violence", "self-harm", "hate speech",
        "adult content", "weapons", "drugs", "terrorism"
    ]
    
    # Topics requiring fact-checking
    FACT_CHECK_TOPICS = [
        "medical", "health", "science", "legal", "financial",
        "news", "history", "statistics", "research"
    ]
    
    def __init__(self):
        """Initialize the Task Analyzer."""
        logger.info("Task Analyzer initialized")
    
    def analyze(self, request: str) -> TaskAnalysis:
        """
        Analyze a user request.
        
        Args:
            request: The user's request/prompt
            
        Returns:
            TaskAnalysis object with complete analysis
        """
        logger.debug(f"Analyzing request: {request[:100]}...")
        
        # Classify task type
        task_type = self._classify_task_type(request)
        
        # Assess complexity
        complexity = self._assess_complexity(request)
        
        # Estimate token requirements
        estimated_tokens = self._estimate_tokens(request, complexity)
        
        # Check if research is needed
        requires_research = self._needs_research(request, task_type)
        
        # Check if examples are needed
        requires_examples = self._needs_examples(task_type)
        
        # Detect safety flags
        safety_flags = self._detect_safety_flags(request)
        
        # Extract keywords
        keywords = self._extract_keywords(request)
        
        # Determine domain
        domain = self._determine_domain(request, keywords)
        
        # Suggest optimization strategy
        suggested_strategy = self._suggest_strategy(
            task_type, complexity, requires_research
        )
        
        analysis = TaskAnalysis(
            task_type=task_type,
            complexity=complexity,
            estimated_tokens=estimated_tokens,
            requires_research=requires_research,
            requires_examples=requires_examples,
            safety_flags=safety_flags,
            keywords=keywords,
            domain=domain,
            suggested_strategy=suggested_strategy,
            metadata={
                "request_length": len(request),
                "word_count": len(request.split()),
            }
        )
        
        logger.info(
            f"Analysis complete: type={task_type.value}, "
            f"complexity={complexity.value}, strategy={suggested_strategy}"
        )
        
        return analysis
    
    def _classify_task_type(self, request: str) -> TaskType:
        """Classify the type of task based on keywords."""
        request_lower = request.lower()
        
        # Count keyword matches for each task type
        scores = {}
        for task_type, keywords in self.TASK_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in request_lower)
            scores[task_type] = score
        
        # Return type with highest score, or GENERAL if no matches
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        return TaskType.GENERAL
    
    def _assess_complexity(self, request: str) -> ComplexityLevel:
        """Assess the complexity of the task."""
        word_count = len(request.split())
        
        # Complexity indicators
        has_technical_terms = any(
            term in request.lower() 
            for term in ["algorithm", "optimization", "architecture", "system"]
        )
        has_multi_step = any(
            word in request.lower() 
            for word in ["step", "process", "workflow", "pipeline"]
        )
        has_constraints = any(
            word in request.lower() 
            for word in ["must", "should", "require", "constraint", "within"]
        )
        
        # Calculate complexity score
        score = 0
        if word_count > 100:
            score += 2
        elif word_count > 50:
            score += 1
        
        if has_technical_terms:
            score += 1
        if has_multi_step:
            score += 1
        if has_constraints:
            score += 1
        
        # Map score to complexity level
        if score >= 4:
            return ComplexityLevel.EXPERT
        elif score >= 3:
            return ComplexityLevel.COMPLEX
        elif score >= 1:
            return ComplexityLevel.MODERATE
        else:
            return ComplexityLevel.SIMPLE
    
    def _estimate_tokens(
        self, 
        request: str, 
        complexity: ComplexityLevel
    ) -> int:
        """Estimate required output tokens based on complexity."""
        base_tokens = len(request.split()) * 2  # Rough estimate
        
        multipliers = {
            ComplexityLevel.SIMPLE: 1.5,
            ComplexityLevel.MODERATE: 2.5,
            ComplexityLevel.COMPLEX: 4.0,
            ComplexityLevel.EXPERT: 6.0,
        }
        
        estimated = int(base_tokens * multipliers[complexity])
        return min(estimated, 8192)  # Cap at model limit
    
    def _needs_research(self, request: str, task_type: TaskType) -> bool:
        """Determine if the task requires web research."""
        research_indicators = [
            "latest", "recent", "current", "news", "today",
            "2024", "2025", "update", "what's new"
        ]
        
        has_research_indicator = any(
            indicator in request.lower() 
            for indicator in research_indicators
        )
        
        is_research_task = task_type in [
            TaskType.RESEARCH,
            TaskType.DATA_ANALYSIS,
            TaskType.QUESTION_ANSWERING
        ]
        
        return has_research_indicator or is_research_task
    
    def _needs_examples(self, task_type: TaskType) -> bool:
        """Determine if the task benefits from examples."""
        example_tasks = [
            TaskType.CODE_GENERATION,
            TaskType.CREATIVE_WRITING,
            TaskType.TECHNICAL_EXPLANATION,
        ]
        return task_type in example_tasks
    
    def _detect_safety_flags(self, request: str) -> SafetyFlags:
        """Detect safety-related concerns in the request."""
        request_lower = request.lower()
        
        flags = SafetyFlags()
        
        # Check for blocked topics
        for topic in self.BLOCKED_TOPICS:
            if topic in request_lower:
                flags.potential_harm = True
                flags.blocked_topics.append(topic)
        
        # Check for fact-checking needs
        for topic in self.FACT_CHECK_TOPICS:
            if topic in request_lower:
                flags.requires_fact_checking = True
                break
        
        # Check for privacy concerns
        privacy_keywords = ["personal", "private", "confidential", "secret"]
        if any(keyword in request_lower for keyword in privacy_keywords):
            flags.privacy_concerns = True
        
        # Check if disclaimer is needed
        disclaimer_topics = ["medical", "legal", "financial", "advice"]
        if any(topic in request_lower for topic in disclaimer_topics):
            flags.needs_disclaimer = True
        
        return flags
    
    def _extract_keywords(self, request: str) -> List[str]:
        """Extract important keywords from the request."""
        # Simple keyword extraction (can be enhanced with NLP)
        words = re.findall(r'\b\w+\b', request.lower())
        
        # Remove common stop words
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at",
            "to", "for", "of", "with", "by", "from", "is", "are", "was"
        }
        
        keywords = [
            word for word in words 
            if word not in stop_words and len(word) > 3
        ]
        
        # Return unique keywords, limited to top 10
        return list(dict.fromkeys(keywords))[:10]
    
    def _determine_domain(
        self, 
        request: str, 
        keywords: List[str]
    ) -> str:
        """Determine the domain/field of the request."""
        domains = {
            "technology": ["code", "software", "computer", "tech", "api"],
            "science": ["science", "research", "study", "experiment"],
            "business": ["business", "market", "company", "strategy"],
            "education": ["learn", "teach", "education", "tutorial"],
            "creative": ["creative", "art", "design", "story"],
            "general": []
        }
        
        for domain, domain_keywords in domains.items():
            if any(kw in keywords for kw in domain_keywords):
                return domain
        
        return "general"
    
    def _suggest_strategy(
        self,
        task_type: TaskType,
        complexity: ComplexityLevel,
        requires_research: bool
    ) -> str:
        """Suggest the best optimization strategy for the task."""
        # Simple tasks: use Mesa for quick optimization
        if complexity == ComplexityLevel.SIMPLE:
            return "mesa"
        
        # Creative tasks: use evolutionary approach
        if task_type == TaskType.CREATIVE_WRITING:
            return "evolutionary"
        
        # Research tasks: use hybrid with knowledge augmentation
        if requires_research:
            return "hybrid"
        
        # Complex technical tasks: use self-critique
        if complexity in [ComplexityLevel.COMPLEX, ComplexityLevel.EXPERT]:
            return "self_critique"
        
        # Default to hybrid for balanced approach
        return "hybrid"
