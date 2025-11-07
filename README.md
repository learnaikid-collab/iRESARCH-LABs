# Advanced Prompt Optimization System (APOS)

## Overview

The Advanced Prompt Optimization System (APOS) is a comprehensive framework for automated prompt engineering and optimization, leveraging state-of-the-art techniques including meta-learning, evolutionary algorithms, and reinforcement learning. Built on Google's Gemini 2.5 Flash, APOS provides intelligent, user-aligned prompt optimization with real-time web research capabilities.

### Key Features

- **Intelligent Task Analysis**: Automatic classification and complexity assessment of user requests
- **Multi-Strategy Optimization**: Combines PromptBreeder, PromptWizard, and Mesa optimization techniques
- **Knowledge-Augmented Generation**: Integrated web research and Retrieval-Augmented Generation (RAG)
- **Safety-First Design**: Built-in alignment checking, policy enforcement, and audit logging
- **Real-Time Interface**: WebSocket-enabled web interface for live optimization monitoring
- **Production-Ready**: Containerized deployment with comprehensive API documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface (Web)                     │
│              FastAPI + React + WebSocket                     │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                    Core Processing                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │Task Analyzer │─▶│Prompt Builder│─▶│  LLM Engine  │      │
│  │              │  │              │  │ (Gemini 2.5) │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                 Optimization Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │Mesa Optimizer│  │ Evolutionary │  │Self-Critique │      │
│  │(Inner-loop)  │  │(PromptBreed) │  │(PromptWizard)│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│             Knowledge & Safety Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │Web Research/ │  │  Alignment   │  │Audit Logger  │      │
│  │     RAG      │  │Policy Engine │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose (optional, for containerized deployment)
- Google AI Studio API key (for Gemini 2.5 Flash access)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/learnaikid-collab/iRESARCH-LABs.git
   cd iRESARCH-LABs
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

5. **Run the application**
   ```bash
   python -m src.web.backend
   ```

   The web interface will be available at `http://localhost:8000`

### Docker Deployment

```bash
docker-compose up -d
```

## Usage

### Web Interface

Navigate to `http://localhost:8000` and:

1. Enter your prompt or task description
2. Select optimization strategy (Mesa, Evolutionary, or Hybrid)
3. Configure safety and alignment preferences
4. Click "Optimize" to start the process
5. Monitor real-time optimization progress via WebSocket updates
6. Review and deploy the optimized prompt

### API Usage

#### Basic Prompt Optimization

```python
import requests

response = requests.post(
    "http://localhost:8000/api/optimize",
    json={
        "prompt": "Explain quantum computing to a 10-year-old",
        "strategy": "mesa",
        "max_iterations": 10,
        "enable_research": True
    }
)

optimized = response.json()
print(f"Optimized prompt: {optimized['prompt']}")
print(f"Performance score: {optimized['score']}")
```

#### Task Analysis

```python
response = requests.post(
    "http://localhost:8000/api/analyze",
    json={"request": "Write a research paper on climate change"}
)

analysis = response.json()
print(f"Complexity: {analysis['complexity']}")
print(f"Required resources: {analysis['resources']}")
print(f"Safety flags: {analysis['safety_flags']}")
```

### Python SDK

```python
from src.core import LLMEngine, TaskAnalyzer, PromptBuilder
from src.optimization import MesaOptimizer

# Initialize components
engine = LLMEngine(api_key="your-api-key")
analyzer = TaskAnalyzer()
builder = PromptBuilder()
optimizer = MesaOptimizer(engine=engine)

# Analyze task
task_info = analyzer.analyze("Generate creative story ideas")

# Build initial prompt
initial_prompt = builder.build(task_info)

# Optimize
optimized_prompt = optimizer.optimize(
    initial_prompt,
    task_info,
    max_iterations=5
)

# Generate response
result = engine.generate(optimized_prompt)
```

## API Documentation

Full API documentation is available at `http://localhost:8000/docs` (Swagger UI) and `http://localhost:8000/redoc` (ReDoc).

### Key Endpoints

- `POST /api/optimize` - Optimize a prompt using specified strategy
- `POST /api/analyze` - Analyze task complexity and requirements
- `POST /api/generate` - Generate response using LLM
- `GET /api/health` - Health check endpoint
- `WS /ws/optimize` - WebSocket endpoint for real-time optimization updates

## Research Background

APOS integrates cutting-edge research in prompt optimization:

### Mesa Optimization (Inner-Loop Reasoner)
Based on recent work in meta-learning, Mesa optimization treats the LLM as an inner optimizer that learns to improve prompts through iterative refinement with user-aligned reward models.

**References:**
- Hubinger et al. "Risks from Learned Optimization" (2019)
- Fernando et al. "Promptbreeder: Self-Referential Self-Improvement Via Prompt Evolution" (2023)

### PromptBreeder (Evolutionary Approach)
Implements evolutionary algorithms to breed and mutate prompts, discovering novel prompt structures through genetic programming techniques.

**Key Features:**
- Mutation operators for prompt variation
- Cross-over for combining successful prompts
- Fitness evaluation based on task performance
- Population management and diversity maintenance

### PromptWizard (Self-Critique)
Incorporates self-critique mechanisms where the LLM evaluates and refines its own prompts based on output quality and alignment with user intent.

**Methodology:**
1. Generate candidate prompts
2. Evaluate outputs against quality criteria
3. Self-critique and identify improvements
4. Iterative refinement until convergence

### Reinforcement Learning Integration
Uses reward modeling to align prompt optimization with user preferences and safety constraints.

## Configuration

### Model Configuration (`config/models.yaml`)

```yaml
llm:
  provider: google
  model: gemini-2.5-flash
  temperature: 0.7
  max_tokens: 8192
  timeout: 30
```

### Optimization Configuration (`config/optimization.yaml`)

```yaml
mesa:
  max_iterations: 10
  learning_rate: 0.01
  convergence_threshold: 0.95

evolutionary:
  population_size: 20
  mutation_rate: 0.2
  crossover_rate: 0.7
  generations: 50

self_critique:
  critique_rounds: 3
  quality_threshold: 0.85
```

### Safety Configuration (`config/safety.yaml`)

```yaml
alignment:
  check_enabled: true
  strictness: medium
  blocked_topics:
    - harmful_content
    - privacy_violation
    - illegal_activities

audit:
  log_level: info
  retention_days: 90
  anonymize_data: true
```

## Development

### Project Structure

```
iRESARCH-LABs/
├── src/
│   ├── core/                 # Core system components
│   │   ├── __init__.py
│   │   ├── llm_engine.py     # Gemini 2.5 integration
│   │   ├── task_analyzer.py  # Request classification
│   │   └── prompt_builder.py # Prompt construction
│   ├── optimization/         # Optimization algorithms
│   │   ├── __init__.py
│   │   ├── mesa_optimizer.py
│   │   ├── evolutionary.py
│   │   ├── self_critique.py
│   │   └── rl_optimizer.py
│   ├── knowledge/           # Knowledge management
│   │   ├── __init__.py
│   │   ├── retrieval.py
│   │   ├── fact_checker.py
│   │   └── citation_manager.py
│   ├── safety/              # Safety and alignment
│   │   ├── __init__.py
│   │   ├── alignment.py
│   │   ├── policy_engine.py
│   │   └── audit_logger.py
│   ├── web/                 # Web interface
│   │   ├── __init__.py
│   │   ├── backend.py
│   │   └── frontend/
│   └── __init__.py
├── config/                  # Configuration files
├── tests/                   # Test suite
├── docs/                    # Documentation
├── requirements.txt
├── docker-compose.yml
├── .env.example
└── README.md
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test module
pytest tests/test_optimizer.py

# Run with coverage
pytest --cov=src tests/
```

### Code Style

This project follows PEP 8 style guidelines. Use the following tools:

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

## Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with clear, descriptive commits
4. Add tests for new functionality
5. Ensure all tests pass and code is formatted
6. Submit a pull request

### Development Roadmap

- [x] Core system architecture
- [x] Basic optimization algorithms
- [x] Web interface foundation
- [ ] Advanced RL-based optimization
- [ ] Multi-modal prompt optimization
- [ ] Distributed optimization across LLM providers
- [ ] Fine-tuning integration for custom domains
- [ ] Advanced visualization and analytics
- [ ] Mobile application

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google AI for Gemini 2.5 Flash API
- Research papers on prompt optimization and meta-learning
- Open-source community for foundational libraries

## Support

- Documentation: [Full documentation](docs/)
- Issues: [GitHub Issues](https://github.com/learnaikid-collab/iRESARCH-LABs/issues)
- Discussions: [GitHub Discussions](https://github.com/learnaikid-collab/iRESARCH-LABs/discussions)

## Citation

If you use APOS in your research, please cite:

```bibtex
@software{apos2024,
  title={Advanced Prompt Optimization System},
  author={iRESARCH-LABs Team},
  year={2024},
  url={https://github.com/learnaikid-collab/iRESARCH-LABs}
}
```