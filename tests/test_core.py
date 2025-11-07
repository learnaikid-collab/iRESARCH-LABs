"""
Unit tests for core components.
"""

import pytest
from src.core import TaskAnalyzer, PromptBuilder
from src.core.task_analyzer import TaskType, ComplexityLevel


class TestTaskAnalyzer:
    """Tests for TaskAnalyzer."""
    
    def test_initialization(self):
        """Test that TaskAnalyzer initializes correctly."""
        analyzer = TaskAnalyzer()
        assert analyzer is not None
    
    def test_analyze_creative_writing(self):
        """Test analysis of creative writing task."""
        analyzer = TaskAnalyzer()
        request = "Write a creative story about a detective solving a mystery"
        
        analysis = analyzer.analyze(request)
        
        assert analysis.task_type == TaskType.CREATIVE_WRITING
        assert analysis.domain in ["creative", "general"]
        assert len(analysis.keywords) > 0
    
    def test_analyze_code_generation(self):
        """Test analysis of code generation task."""
        analyzer = TaskAnalyzer()
        request = "Write a Python function to reverse a linked list"
        
        analysis = analyzer.analyze(request)
        
        assert analysis.task_type == TaskType.CODE_GENERATION
        assert analysis.requires_examples is True
    
    def test_complexity_assessment(self):
        """Test complexity assessment."""
        analyzer = TaskAnalyzer()
        
        # Simple task
        simple_request = "Hello world"
        simple_analysis = analyzer.analyze(simple_request)
        assert simple_analysis.complexity == ComplexityLevel.SIMPLE
        
        # Complex task
        complex_request = (
            "Develop a comprehensive algorithmic system that optimizes "
            "resource allocation within distributed computing environments "
            "while maintaining strict performance constraints and security requirements"
        )
        complex_analysis = analyzer.analyze(complex_request)
        assert complex_analysis.complexity in [ComplexityLevel.COMPLEX, ComplexityLevel.EXPERT]
    
    def test_safety_flags(self):
        """Test safety flag detection."""
        analyzer = TaskAnalyzer()
        
        # Safe request
        safe_request = "Explain how photosynthesis works"
        safe_analysis = analyzer.analyze(safe_request)
        assert safe_analysis.safety_flags.potential_harm is False
        
        # Request with potential safety concerns
        unsafe_request = "How to make a weapon"
        unsafe_analysis = analyzer.analyze(unsafe_request)
        assert unsafe_analysis.safety_flags.potential_harm is True or len(unsafe_analysis.safety_flags.blocked_topics) > 0


class TestPromptBuilder:
    """Tests for PromptBuilder."""
    
    def test_initialization(self):
        """Test that PromptBuilder initializes correctly."""
        builder = PromptBuilder()
        assert builder is not None
    
    def test_build_basic_prompt(self):
        """Test building a basic prompt."""
        analyzer = TaskAnalyzer()
        builder = PromptBuilder()
        
        request = "Explain quantum computing"
        analysis = analyzer.analyze(request)
        
        prompt = builder.build(analysis, request)
        
        assert len(prompt) > 0
        assert request in prompt or "quantum" in prompt.lower()
    
    def test_meta_prompt_generation(self):
        """Test meta-prompt generation for optimization."""
        analyzer = TaskAnalyzer()
        builder = PromptBuilder()
        
        request = "Write a function"
        analysis = analyzer.analyze(request)
        current_prompt = "def my_function(): pass"
        
        meta_prompt = builder.build_meta_prompt(analysis, current_prompt)
        
        assert "optimize" in meta_prompt.lower()
        assert current_prompt in meta_prompt
    
    def test_prompt_refinement(self):
        """Test prompt refinement."""
        builder = PromptBuilder()
        
        prompt = "Explain AI"
        feedback = "Be more specific about machine learning"
        
        refined = builder.refine_prompt(prompt, feedback)
        
        assert len(refined) > 0
        assert "feedback" in refined.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
