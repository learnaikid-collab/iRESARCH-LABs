"""
Prompt Builder for constructing optimized prompts.

Handles Prompt Zero construction, chain-of-thought integration,
few-shot examples, and template management.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from src.core.task_analyzer import TaskAnalysis, TaskType

logger = logging.getLogger(__name__)


@dataclass
class PromptTemplate:
    """Template for prompt construction."""
    name: str
    template: str
    task_types: List[TaskType]
    requires_examples: bool = False
    requires_context: bool = False


class PromptBuilder:
    """
    Builds optimized prompts using templates and best practices.
    
    Features:
    - Prompt Zero construction
    - Chain-of-thought integration
    - Few-shot example management
    - Template-based generation
    - Context injection
    """
    
    # Predefined templates for different task types
    TEMPLATES = {
        "creative_writing": PromptTemplate(
            name="creative_writing",
            template=(
                "You are a creative writing assistant. Your task is to {task}.\n\n"
                "Guidelines:\n"
                "- Be creative and original\n"
                "- Use vivid descriptions and engaging language\n"
                "- Maintain consistency in tone and style\n"
                "{examples}\n"
                "{context}\n"
                "Now, {task}"
            ),
            task_types=[TaskType.CREATIVE_WRITING],
            requires_examples=True,
        ),
        "technical_explanation": PromptTemplate(
            name="technical_explanation",
            template=(
                "You are a technical expert. Please {task}.\n\n"
                "Requirements:\n"
                "- Be accurate and precise\n"
                "- Use clear, accessible language\n"
                "- Provide relevant examples\n"
                "- Structure your explanation logically\n"
                "{context}\n"
                "Let's think step by step:\n"
                "{task}"
            ),
            task_types=[TaskType.TECHNICAL_EXPLANATION],
            requires_context=True,
        ),
        "code_generation": PromptTemplate(
            name="code_generation",
            template=(
                "You are an expert programmer. Your task is to {task}.\n\n"
                "Requirements:\n"
                "- Write clean, efficient, and well-documented code\n"
                "- Follow best practices and conventions\n"
                "- Include error handling where appropriate\n"
                "- Add comments explaining key logic\n"
                "{examples}\n"
                "{context}\n"
                "Implementation:\n"
                "{task}"
            ),
            task_types=[TaskType.CODE_GENERATION],
            requires_examples=True,
            requires_context=True,
        ),
        "reasoning": PromptTemplate(
            name="reasoning",
            template=(
                "Let's solve this step by step.\n\n"
                "Problem: {task}\n\n"
                "{context}\n"
                "Step-by-step reasoning:\n"
                "1. First, let's understand what we're being asked\n"
                "2. Next, let's identify the key information\n"
                "3. Then, let's work through the logic\n"
                "4. Finally, let's arrive at a conclusion\n\n"
                "Now let's proceed:"
            ),
            task_types=[TaskType.REASONING],
            requires_context=True,
        ),
        "general": PromptTemplate(
            name="general",
            template=(
                "{task}\n\n"
                "{context}\n"
                "Please provide a comprehensive response."
            ),
            task_types=[TaskType.GENERAL],
        ),
    }
    
    # Few-shot examples for different task types
    EXAMPLES = {
        TaskType.CREATIVE_WRITING: [
            {
                "input": "Write a short story about a detective",
                "output": (
                    "Detective Sarah Chen stood in the rain-soaked alley, "
                    "her keen eyes scanning the crime scene..."
                )
            }
        ],
        TaskType.CODE_GENERATION: [
            {
                "input": "Write a function to reverse a string in Python",
                "output": (
                    "def reverse_string(s: str) -> str:\n"
                    "    \"\"\"Reverse a string using slicing.\"\"\"\n"
                    "    return s[::-1]"
                )
            }
        ],
    }
    
    def __init__(self):
        """Initialize the Prompt Builder."""
        logger.info("Prompt Builder initialized")
    
    def build(
        self,
        task_analysis: TaskAnalysis,
        user_request: str,
        context: Optional[str] = None,
        include_examples: bool = True,
        use_chain_of_thought: bool = True,
    ) -> str:
        """
        Build an optimized prompt.
        
        Args:
            task_analysis: Analysis of the task
            user_request: The original user request
            context: Optional additional context
            include_examples: Whether to include few-shot examples
            use_chain_of_thought: Whether to use chain-of-thought prompting
            
        Returns:
            Optimized prompt string
        """
        logger.debug(f"Building prompt for task type: {task_analysis.task_type.value}")
        
        # Select appropriate template
        template = self._select_template(task_analysis.task_type)
        
        # Prepare examples if needed
        examples_text = ""
        if include_examples and task_analysis.requires_examples:
            examples_text = self._format_examples(task_analysis.task_type)
        
        # Prepare context if provided
        context_text = ""
        if context:
            context_text = f"Context:\n{context}\n"
        elif task_analysis.domain != "general":
            context_text = f"Domain: {task_analysis.domain}\n"
        
        # Add safety disclaimers if needed
        safety_text = ""
        if task_analysis.safety_flags.needs_disclaimer:
            safety_text = self._add_safety_disclaimer(task_analysis)
        
        # Build the prompt using the template
        prompt = template.template.format(
            task=user_request,
            examples=examples_text,
            context=context_text,
        )
        
        # Add chain-of-thought if applicable
        if use_chain_of_thought and self._should_use_cot(task_analysis):
            prompt = self._add_chain_of_thought(prompt, task_analysis)
        
        # Add safety disclaimers
        if safety_text:
            prompt = f"{safety_text}\n\n{prompt}"
        
        logger.info(f"Built prompt of length {len(prompt)} characters")
        
        return prompt
    
    def build_meta_prompt(
        self,
        task_analysis: TaskAnalysis,
        current_prompt: str,
    ) -> str:
        """
        Build a meta-prompt for prompt optimization.
        
        Args:
            task_analysis: Analysis of the task
            current_prompt: The current prompt to optimize
            
        Returns:
            Meta-prompt for optimization
        """
        meta_prompt = f"""You are an expert prompt engineer. Your task is to optimize the following prompt.

Current Prompt:
{current_prompt}

Task Analysis:
- Type: {task_analysis.task_type.value}
- Complexity: {task_analysis.complexity.value}
- Domain: {task_analysis.domain}

Optimization Goals:
1. Improve clarity and specificity
2. Enhance task alignment
3. Add relevant constraints or guidelines
4. Ensure safety and appropriateness
5. Optimize for better LLM performance

Please provide an improved version of the prompt that achieves these goals while maintaining the original intent.

Improved Prompt:"""
        
        return meta_prompt
    
    def _select_template(self, task_type: TaskType) -> PromptTemplate:
        """Select the appropriate template for a task type."""
        # Find matching template
        for template in self.TEMPLATES.values():
            if task_type in template.task_types:
                return template
        
        # Default to general template
        return self.TEMPLATES["general"]
    
    def _format_examples(self, task_type: TaskType) -> str:
        """Format few-shot examples for inclusion in the prompt."""
        if task_type not in self.EXAMPLES:
            return ""
        
        examples = self.EXAMPLES[task_type]
        formatted = "Examples:\n\n"
        
        for i, example in enumerate(examples, 1):
            formatted += f"Example {i}:\n"
            formatted += f"Input: {example['input']}\n"
            formatted += f"Output: {example['output']}\n\n"
        
        return formatted
    
    def _should_use_cot(self, task_analysis: TaskAnalysis) -> bool:
        """Determine if chain-of-thought should be used."""
        # Use CoT for reasoning, complex tasks, and technical explanations
        cot_task_types = [
            TaskType.REASONING,
            TaskType.TECHNICAL_EXPLANATION,
            TaskType.CODE_GENERATION,
        ]
        
        return (
            task_analysis.task_type in cot_task_types or
            task_analysis.complexity.value in ["complex", "expert"]
        )
    
    def _add_chain_of_thought(
        self,
        prompt: str,
        task_analysis: TaskAnalysis
    ) -> str:
        """Add chain-of-thought reasoning to the prompt."""
        cot_instruction = (
            "\n\nPlease think through this step by step before providing "
            "your final answer. Show your reasoning process."
        )
        
        return prompt + cot_instruction
    
    def _add_safety_disclaimer(self, task_analysis: TaskAnalysis) -> str:
        """Add safety disclaimers based on task analysis."""
        disclaimers = []
        
        if "medical" in task_analysis.keywords:
            disclaimers.append(
                "DISCLAIMER: This is for informational purposes only and not "
                "medical advice. Consult a healthcare professional."
            )
        
        if "legal" in task_analysis.keywords:
            disclaimers.append(
                "DISCLAIMER: This is for informational purposes only and not "
                "legal advice. Consult a qualified attorney."
            )
        
        if "financial" in task_analysis.keywords:
            disclaimers.append(
                "DISCLAIMER: This is for informational purposes only and not "
                "financial advice. Consult a financial advisor."
            )
        
        return "\n".join(disclaimers) if disclaimers else ""
    
    def refine_prompt(
        self,
        prompt: str,
        feedback: str,
    ) -> str:
        """
        Refine a prompt based on feedback.
        
        Args:
            prompt: Current prompt
            feedback: Feedback on the prompt
            
        Returns:
            Refined prompt
        """
        refinement_prompt = f"""Given this prompt:
{prompt}

And this feedback:
{feedback}

Please provide an improved version of the prompt that addresses the feedback.

Improved prompt:"""
        
        return refinement_prompt
    
    def combine_prompts(
        self,
        prompts: List[str],
        strategy: str = "best_elements"
    ) -> str:
        """
        Combine multiple prompts into a single optimized prompt.
        
        Args:
            prompts: List of prompts to combine
            strategy: Combination strategy ('best_elements', 'sequential', 'parallel')
            
        Returns:
            Combined prompt
        """
        if not prompts:
            return ""
        
        if len(prompts) == 1:
            return prompts[0]
        
        if strategy == "sequential":
            # Combine prompts in sequence
            return "\n\n".join(prompts)
        
        elif strategy == "parallel":
            # Present prompts as alternatives
            combined = "Please address the following:\n\n"
            for i, prompt in enumerate(prompts, 1):
                combined += f"{i}. {prompt}\n\n"
            return combined
        
        else:  # best_elements
            # This would require LLM assistance to extract best parts
            # For now, return the longest prompt as a heuristic
            return max(prompts, key=len)
