# API Documentation

## Overview

This document provides comprehensive API documentation for the Prompt Optimization System.

## Core Components

### TaskAnalyzer

Analyzes user queries to determine optimal processing strategy.

```python
from src.core.task_analyzer import TaskAnalyzer

analyzer = TaskAnalyzer()
analysis = analyzer.analyze_query("Your query here")
```

#### Methods

##### `analyze_query(query: str, context: Optional[Dict] = None) -> TaskAnalysis`

Perform comprehensive query analysis.

**Parameters:**
- `query` (str): User query string
- `context` (Optional[Dict]): Additional context information

**Returns:**
- `TaskAnalysis`: Complete analysis result

**Example:**
```python
analysis = analyzer.analyze_query("Explain quantum computing")
print(f"Task type: {analysis.task_type}")
print(f"Complexity: {analysis.complexity}")
print(f"Recommended strategy: {analysis.recommended_strategy}")
```

##### `classify_task_type(query: str) -> TaskType`

Determine the primary task type.

**Returns:** `TaskType` enum (FACTUAL, REASONING, CREATIVE, CODING, etc.)

##### `estimate_complexity(query: str) -> ComplexityLevel`

Estimate task complexity.

**Returns:** `ComplexityLevel` enum (SIMPLE, MODERATE, COMPLEX, EXPERT)

### PromptBuilder

Constructs prompts from task analysis.

```python
from src.core.prompt_builder import PromptBuilder

builder = PromptBuilder()
prompt = builder.build_prompt_zero(query, analysis)
```

#### Methods

##### `build_prompt_zero(query: str, task_analysis: TaskAnalysis, context: Optional[Dict] = None) -> Prompt`

Build initial prompt (Prompt Zero).

**Parameters:**
- `query`: User query
- `task_analysis`: TaskAnalysis object
- `context`: Optional additional context

**Returns:**
- `Prompt`: Constructed prompt object

**Example:**
```python
prompt = builder.build_prompt_zero(
    query="Explain relativity",
    task_analysis=analysis,
    context={'domain': 'physics'}
)
print(prompt)
```

### Prompt

Represents a prompt with all its components.

```python
from src.core.prompt_builder import Prompt

# Create from text
prompt = Prompt.from_text("Your instruction here")

# Create with components
prompt = Prompt(
    instruction="Main instruction",
    system_role="You are an expert",
    examples=[{"input": "...", "output": "..."}],
    context="Additional context"
)
```

#### Methods

##### `add_context(context: str, position: str = 'before') -> Prompt`

Add context to prompt.

##### `add_example(example: Dict) -> Prompt`

Add an example to the prompt.

##### `from_text(text: str) -> Prompt`

Create prompt from plain text (class method).

### LLMEngine

Unified interface for LLM interactions.

```python
from src.core.llm_engine import LLMEngine, LLMConfig

# Initialize with defaults
llm = LLMEngine(model="gemini-2.5-pro")

# Initialize with config
config = LLMConfig(
    model_name="gpt-4-turbo",
    temperature=0.8,
    max_tokens=2048
)
llm = LLMEngine(config=config)
```

#### Methods

##### `generate(prompt, temperature: Optional[float] = None, max_tokens: Optional[int] = None, tools: Optional[List] = None) -> LLMResponse`

Generate response from prompt.

**Parameters:**
- `prompt`: Prompt object or string
- `temperature`: Override default temperature
- `max_tokens`: Override default max tokens
- `tools`: Optional list of tools for function calling

**Returns:**
- `LLMResponse`: Response object with text and metadata

**Example:**
```python
response = llm.generate(
    prompt="Explain AI",
    temperature=0.7,
    max_tokens=500
)
print(response.text)
print(f"Tokens used: {response.tokens_used}")
```

##### `batch_generate(prompts: List, parallel: bool = True) -> List[LLMResponse]`

Generate responses for multiple prompts.

##### `stream_generate(prompt, **kwargs) -> Generator[str, None, None]`

Generate response with streaming.

**Example:**
```python
for chunk in llm.stream_generate(prompt):
    print(chunk, end='', flush=True)
```

### OutputEvaluator

Evaluates LLM outputs across multiple dimensions.

```python
from src.core.evaluator import OutputEvaluator

evaluator = OutputEvaluator()
result = evaluator.evaluate_output(output, query)
```

#### Methods

##### `evaluate_output(output: str, query: str, prompt = None, context: Optional[Dict] = None) -> EvaluationResult`

Comprehensive output evaluation.

**Parameters:**
- `output`: Generated text
- `query`: Original query
- `prompt`: Prompt used (optional)
- `context`: Additional context (optional)

**Returns:**
- `EvaluationResult`: Complete evaluation with scores

**Example:**
```python
result = evaluator.evaluate_output(
    output="Generated answer...",
    query="Original question",
    context={'sources': [...]}
)
print(f"Overall score: {result.overall_score}")
print(f"Quality: {result.quality_score}")
print(f"Alignment: {result.alignment_score}")
print(f"Feedback: {result.feedback}")
```

### PromptOptimizer

Main orchestrator for prompt optimization.

```python
from src.core.orchestrator import PromptOptimizer
from src.core.llm_engine import LLMEngine

llm = LLMEngine(model="gemini-2.5-pro")
optimizer = PromptOptimizer(
    llm_engine=llm,
    optimization_strategy="auto",
    max_iterations=5
)
```

#### Methods

##### `optimize_and_generate(query: str, user_preferences: Optional[Dict] = None, enable_web_search: bool = False, max_sources: int = 5) -> OptimizationResult`

Main method: optimize prompt and generate response.

**Parameters:**
- `query`: User query
- `user_preferences`: Optional preferences (style, length, etc.)
- `enable_web_search`: Whether to search web
- `max_sources`: Maximum sources to retrieve

**Returns:**
- `OptimizationResult`: Complete result with answer and metadata

**Example:**
```python
result = optimizer.optimize_and_generate(
    query="Explain machine learning",
    user_preferences={
        'style': 'simple',
        'length': 'medium'
    },
    enable_web_search=True
)

print(result.answer)
print(f"Iterations: {result.iterations}")
print(f"Quality score: {result.quality_score}")
print(f"Improvement: {result.improvement:.1%}")
print(f"Time: {result.time_elapsed:.2f}s")
```

## Data Classes

### TaskAnalysis

```python
@dataclass
class TaskAnalysis:
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
```

### EvaluationResult

```python
@dataclass
class EvaluationResult:
    overall_score: float
    quality_score: float
    alignment_score: float
    factuality_score: float
    safety_score: float
    reward: float
    feedback: str
    critique: Optional[Critique]
    metadata: Dict
```

### OptimizationResult

```python
@dataclass
class OptimizationResult:
    answer: str
    final_prompt: str
    iterations: int
    quality_score: float
    improvement: float
    time_elapsed: float
    sources: Optional[list]
    metadata: Dict
```

## Enums

### TaskType

```python
class TaskType(Enum):
    FACTUAL = "factual"
    REASONING = "reasoning"
    CREATIVE = "creative"
    CODING = "coding"
    ANALYSIS = "analysis"
    CONVERSATIONAL = "conversational"
    INSTRUCTION = "instruction"
    SUMMARIZATION = "summarization"
    TRANSLATION = "translation"
    CLASSIFICATION = "classification"
```

### ComplexityLevel

```python
class ComplexityLevel(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    EXPERT = "expert"
```

## Complete Example

```python
from src.core.task_analyzer import TaskAnalyzer
from src.core.prompt_builder import PromptBuilder
from src.core.llm_engine import LLMEngine
from src.core.evaluator import OutputEvaluator
from src.core.orchestrator import PromptOptimizer

# Initialize components
analyzer = TaskAnalyzer()
builder = PromptBuilder()
llm = LLMEngine(model="gemini-2.5-pro")
evaluator = OutputEvaluator()

# Option 1: Use components individually
query = "Explain quantum entanglement simply"
analysis = analyzer.analyze_query(query)
prompt = builder.build_prompt_zero(query, analysis)
response = llm.generate(prompt)
evaluation = evaluator.evaluate_output(response.text, query)

print(f"Output: {response.text}")
print(f"Score: {evaluation.overall_score}")

# Option 2: Use orchestrator (recommended)
optimizer = PromptOptimizer(
    llm_engine=llm,
    optimization_strategy="auto",
    max_iterations=5
)

result = optimizer.optimize_and_generate(
    query=query,
    user_preferences={'style': 'simple', 'length': 'medium'}
)

print(f"Answer: {result.answer}")
print(f"Quality: {result.quality_score}")
print(f"Iterations: {result.iterations}")
```

## Configuration

Load configuration from YAML:

```python
import yaml

with open('config/default_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

llm = LLMEngine(
    model=config['llm']['model'],
    config=LLMConfig(
        temperature=config['llm']['temperature'],
        max_tokens=config['llm']['max_tokens']
    )
)
```

## Error Handling

```python
from src.core.orchestrator import PromptOptimizer

try:
    optimizer = PromptOptimizer(llm_engine=llm)
    result = optimizer.optimize_and_generate(query)
except Exception as e:
    print(f"Error: {e}")
    # Handle error appropriately
```

## Best Practices

1. **Reuse components**: Create instances once and reuse
2. **Configure appropriately**: Use config files for settings
3. **Handle errors**: Wrap API calls in try-except blocks
4. **Monitor usage**: Track tokens and costs
5. **Cache results**: Store successful prompts for reuse

## Advanced Usage

### Custom Optimization Strategy

```python
# Implement custom optimizer
from src.optimizers.base import BaseOptimizer

class CustomOptimizer(BaseOptimizer):
    def optimize(self, prompt, query, evaluation_fn):
        # Custom optimization logic
        pass

# Use with orchestrator
optimizer.register_strategy('custom', CustomOptimizer())
```

### Tool Usage

```python
# Define tools
tools = [
    {
        'name': 'web_search',
        'description': 'Search the web',
        'parameters': {'query': 'string'}
    },
    {
        'name': 'calculator',
        'description': 'Perform calculations',
        'parameters': {'expression': 'string'}
    }
]

response = llm.generate(prompt, tools=tools)
```

---

**API Version**: 0.1.0  
**Last Updated**: 2025-11-06
