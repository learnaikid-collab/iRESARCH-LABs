# Quick Start Guide

## 5-Minute Setup

### 1. Get the Code
```bash
git clone https://github.com/learnaikid-collab/iRESARCH-LABs.git
cd iRESARCH-LABs
```

### 2. Install
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### 4. Verify
```bash
python verify_installation.py
```

### 5. Run
```bash
python run.py
```

Visit: http://localhost:8000

## Without API Key

You can test core components without an API key:

```python
from src.core import TaskAnalyzer, PromptBuilder

analyzer = TaskAnalyzer()
builder = PromptBuilder()

# Analyze a task
analysis = analyzer.analyze("Write a Python function")
print(f"Task type: {analysis.task_type.value}")

# Build a prompt
prompt = builder.build(analysis, "Write a Python function")
print(f"Prompt: {prompt}")
```

## Quick Examples

### Analyze a Task
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"request": "Explain neural networks"}'
```

### Optimize a Prompt (requires API key)
```bash
curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Teach me about AI",
    "strategy": "mesa",
    "max_iterations": 5
  }'
```

## Common Commands

```bash
# Run server
python run.py

# Run tests
pytest tests/ -v

# Verify installation
python verify_installation.py

# Format code
black src/ tests/

# With Docker
docker-compose up -d
```

## Getting Help

- 📖 [Full Documentation](docs/)
- 🐛 [Report Issues](https://github.com/learnaikid-collab/iRESARCH-LABs/issues)
- 💬 [Discussions](https://github.com/learnaikid-collab/iRESARCH-LABs/discussions)

## Next Steps

1. Read [Installation Guide](docs/INSTALLATION.md)
2. Try [Usage Examples](docs/USAGE.md)
3. Explore [API Documentation](docs/API.md)
4. Understand [Architecture](docs/ARCHITECTURE.md)
5. Contribute! See [Contributing Guide](CONTRIBUTING.md)
