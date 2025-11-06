# Quick Start Guide

Get up and running with the Advanced Prompt Optimization System in minutes!

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/learnaikid-collab/iRESARCH-LABs.git
cd iRESARCH-LABs/research/prompt-optimization-lab
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install the package:

```bash
pip install -e .
```

## 📝 Basic Usage

### Example 1: Simple Query Optimization

```python
from src.core.task_analyzer import TaskAnalyzer
from src.core.prompt_builder import PromptBuilder
from src.core.llm_engine import LLMEngine
from src.core.orchestrator import PromptOptimizer

# Initialize the system
llm = LLMEngine(model="gemini-2.5-pro")
optimizer = PromptOptimizer(
    llm_engine=llm,
    optimization_strategy="auto",
    max_iterations=5
)

# Optimize and generate
query = "Explain quantum entanglement in simple terms"
result = optimizer.optimize_and_generate(query)

print(result.answer)
print(f"Quality Score: {result.quality_score}")
print(f"Iterations: {result.iterations}")
```

### Example 2: With User Preferences

```python
result = optimizer.optimize_and_generate(
    query="Explain machine learning",
    user_preferences={
        'style': 'simple',      # simple, technical, formal, casual
        'length': 'medium',     # short, medium, long
        'examples': True        # include examples
    }
)
```

### Example 3: With Web Search

```python
from src.knowledge.rag_system import RAGSystem

# Initialize with knowledge system
rag = RAGSystem(web_search_enabled=True)
optimizer = PromptOptimizer(
    llm_engine=llm,
    knowledge_system=rag
)

# Query requiring current information
result = optimizer.optimize_and_generate(
    query="What are the latest AI breakthroughs?",
    enable_web_search=True,
    max_sources=5
)

print(result.answer)
print(f"Sources: {result.sources}")
```

## 🔧 Configuration

### Using Config Files

```python
import yaml

# Load configuration
with open('config/default_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Initialize with config
llm = LLMEngine(
    model=config['llm']['model'],
    config=LLMConfig(
        temperature=config['llm']['temperature'],
        max_tokens=config['llm']['max_tokens']
    )
)
```

### Environment Variables

Create a `.env` file:

```bash
# LLM API Keys
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Search API
GOOGLE_SEARCH_API_KEY=your_key_here
```

## 📊 Running Examples

### Basic Example

```bash
cd examples
python basic_optimization.py
```

### Dry Run (No API Calls)

```bash
python basic_optimization.py --dry-run
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_core/test_task_analyzer.py
```

## 📚 Next Steps

1. **Explore Documentation**
   - [Architecture](docs/ARCHITECTURE.md)
   - [Algorithms](docs/ALGORITHMS.md)
   - [API Reference](docs/API.md)

2. **Try Different Strategies**
   ```python
   strategies = ['auto', 'fast', 'thorough', 'aggressive']
   for strategy in strategies:
       optimizer = PromptOptimizer(llm, optimization_strategy=strategy)
       result = optimizer.optimize_and_generate(query)
   ```

3. **Customize Components**
   - Implement custom optimizers
   - Add new evaluation metrics
   - Create domain-specific templates

4. **Deploy as Service**
   ```bash
   uvicorn src.api.server:app --host 0.0.0.0 --port 8000
   ```

## 🎯 Common Use Cases

### Research Questions

```python
query = "What are the implications of quantum computing for cryptography?"
result = optimizer.optimize_and_generate(
    query,
    enable_web_search=True
)
```

### Code Generation

```python
query = "Write a Python function to implement binary search"
llm = LLMEngine(model="gpt-4-turbo")  # Good for coding
optimizer = PromptOptimizer(llm, optimization_strategy="fast")
result = optimizer.optimize_and_generate(query)
```

### Creative Writing

```python
query = "Write a short story about time travel"
optimizer = PromptOptimizer(llm, optimization_strategy="evolutionary")
result = optimizer.optimize_and_generate(
    query,
    user_preferences={'style': 'creative', 'length': 'long'}
)
```

### Data Analysis

```python
query = "Analyze the trends in this dataset and provide insights"
result = optimizer.optimize_and_generate(
    query,
    user_preferences={'style': 'technical', 'examples': True}
)
```

## ⚙️ Optimization Strategies

| Strategy | Speed | Quality | Best For |
|----------|-------|---------|----------|
| `fast` | ⚡⚡⚡ | ⭐⭐ | Quick answers |
| `auto` | ⚡⚡ | ⭐⭐⭐ | General use |
| `thorough` | ⚡ | ⭐⭐⭐⭐ | Complex tasks |
| `aggressive` | 🐌 | ⭐⭐⭐⭐⭐ | Research/critical |

## 🔍 Debugging

### Enable Verbose Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Task Analysis

```python
analyzer = TaskAnalyzer()
analysis = analyzer.analyze_query(query)
print(f"Task Type: {analysis.task_type}")
print(f"Complexity: {analysis.complexity}")
print(f"Strategy: {analysis.recommended_strategy}")
```

### Inspect Prompts

```python
builder = PromptBuilder()
prompt = builder.build_prompt_zero(query, analysis)
print(prompt)  # See what's being sent to LLM
```

## 💡 Tips & Best Practices

1. **Start Simple**: Use `fast` strategy first, then upgrade if needed
2. **Reuse Components**: Create instances once and reuse
3. **Monitor Costs**: Track token usage and API calls
4. **Cache Results**: Store successful prompts for similar queries
5. **Experiment**: Try different strategies for your use case

## 🆘 Troubleshooting

### API Key Not Found

```bash
export GEMINI_API_KEY=your_key_here
# or add to .env file
```

### Module Not Found

```bash
pip install -e .
# or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Rate Limit Errors

Adjust in config:
```yaml
llm:
  max_requests_per_minute: 30
  retry_attempts: 5
```

## 📖 Resources

- [Full Documentation](README.md)
- [Architecture Guide](docs/ARCHITECTURE.md)
- [Algorithm Details](docs/ALGORITHMS.md)
- [API Reference](docs/API.md)
- [Contributing](../../docs/CONTRIBUTING.md)

## 🤝 Getting Help

- Open an issue on GitHub
- Check existing documentation
- Join community discussions

---

**Happy Optimizing! 🚀**
