"""
Prompt Builder: Constructs and manipulates prompts.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class PromptFormat(Enum):
    """Prompt format types."""
    PLAIN = "plain"
    STRUCTURED = "structured"
    CONVERSATIONAL = "conversational"
    CODE = "code"


@dataclass
class PromptTemplate:
    """Template for prompt construction."""
    name: str
    system_role: Optional[str] = None
    instruction_template: str = ""
    example_template: Optional[str] = None
    format_instructions: Optional[str] = None
    
    def render(self, **kwargs) -> str:
        """Render template with provided values."""
        result = ""
        if self.system_role:
            result += f"System: {self.system_role}\n\n"
        result += self.instruction_template.format(**kwargs)
        if self.format_instructions:
            result += f"\n\n{self.format_instructions}"
        return result


@dataclass
class Prompt:
    """Represents a prompt with all its components."""
    instruction: str
    system_role: Optional[str] = None
    examples: List[Dict] = field(default_factory=list)
    context: Optional[str] = None
    format_spec: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    
    def __str__(self) -> str:
        """Convert prompt to string."""
        parts = []
        
        if self.system_role:
            parts.append(f"[System]: {self.system_role}")
        
        if self.context:
            parts.append(f"[Context]: {self.context}")
        
        if self.examples:
            parts.append("[Examples]:")
            for i, ex in enumerate(self.examples, 1):
                parts.append(f"Example {i}: {ex}")
        
        parts.append(f"[Instruction]: {self.instruction}")
        
        if self.format_spec:
            parts.append(f"[Format]: {self.format_spec}")
        
        return "\n\n".join(parts)
    
    def add_context(self, context: str, position: str = 'before') -> 'Prompt':
        """Add context to prompt."""
        if self.context:
            self.context = f"{self.context}\n\n{context}"
        else:
            self.context = context
        return self
    
    def add_example(self, example: Dict) -> 'Prompt':
        """Add an example to the prompt."""
        self.examples.append(example)
        return self
    
    @classmethod
    def from_text(cls, text: str) -> 'Prompt':
        """Create prompt from plain text."""
        return cls(instruction=text)


class PromptBuilder:
    """Builds prompts from task analysis."""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, PromptTemplate]:
        """Load default prompt templates."""
        return {
            'factual': PromptTemplate(
                name='factual',
                system_role='You are a knowledgeable AI assistant.',
                instruction_template='{query}',
            ),
            'reasoning': PromptTemplate(
                name='reasoning',
                system_role='You are an AI assistant skilled in logical reasoning.',
                instruction_template='{query}\n\nLet\'s think step by step:',
            ),
            'creative': PromptTemplate(
                name='creative',
                system_role='You are a creative AI assistant.',
                instruction_template='{query}',
            ),
            'coding': PromptTemplate(
                name='coding',
                system_role='You are an expert programmer.',
                instruction_template='{query}',
                format_instructions='Provide code with clear comments and explanations.',
            ),
        }
    
    def build_prompt_zero(
        self,
        query: str,
        task_analysis,
        context: Optional[Dict] = None
    ) -> Prompt:
        """
        Build initial prompt (Prompt Zero) from query and analysis.
        
        Args:
            query: User query
            task_analysis: TaskAnalysis object
            context: Optional additional context
            
        Returns:
            Constructed Prompt object
        """
        # Select appropriate template
        template = self.templates.get(
            task_analysis.task_type.value,
            self.templates['factual']
        )
        
        # Build prompt
        prompt = Prompt(
            instruction=query,
            system_role=template.system_role,
            format_spec=template.format_instructions,
            metadata={
                'task_type': task_analysis.task_type.value,
                'complexity': task_analysis.complexity.value,
            }
        )
        
        # Add reasoning trigger if needed
        if task_analysis.requires_reasoning:
            prompt.instruction += "\n\nLet's approach this step-by-step:"
        
        # Add context if provided
        if context and 'retrieved_docs' in context:
            prompt.add_context(context['retrieved_docs'])
        
        return prompt
