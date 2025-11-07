# System Architecture

## Overview

The Advanced Prompt Optimization System (APOS) is built with a modular, layered architecture that separates concerns and enables easy extension and maintenance.

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                  Presentation Layer                          │
│                  (Web Interface)                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   FastAPI    │  │    React     │  │  WebSocket   │      │
│  │   Backend    │  │   Frontend   │  │   Handler    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  Core Logic Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │Task Analyzer │  │Prompt Builder│  │  LLM Engine  │      │
│  │              │  │              │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              Optimization Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    Mesa      │  │ Evolutionary │  │Self-Critique │      │
│  │  Optimizer   │  │  Optimizer   │  │  Optimizer   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│         Cross-Cutting Concerns Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Safety &   │  │  Knowledge   │  │    Audit     │      │
│  │  Alignment   │  │  Management  │  │   Logging    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Core Components (`src/core/`)

#### LLM Engine (`llm_engine.py`)
- **Purpose**: Interface with Google Gemini 2.5 Flash
- **Responsibilities**:
  - API communication
  - Response processing
  - Error handling and retries
  - Performance monitoring
- **Key Features**:
  - Automatic retry with exponential backoff
  - Token usage tracking
  - Latency monitoring
  - Configurable generation parameters

#### Task Analyzer (`task_analyzer.py`)
- **Purpose**: Analyze and classify user requests
- **Responsibilities**:
  - Task type classification
  - Complexity assessment
  - Resource requirement estimation
  - Safety flag detection
- **Output**: TaskAnalysis object with:
  - Task type (creative_writing, code_generation, etc.)
  - Complexity level (simple, moderate, complex, expert)
  - Resource requirements
  - Safety flags
  - Suggested optimization strategy

#### Prompt Builder (`prompt_builder.py`)
- **Purpose**: Construct optimized prompts
- **Responsibilities**:
  - Template selection
  - Chain-of-thought integration
  - Few-shot example management
  - Safety disclaimer injection
- **Features**:
  - Multiple prompt templates
  - Meta-prompt generation
  - Prompt refinement
  - Context injection

### 2. Optimization Components (`src/optimization/`)

#### Mesa Optimizer (`mesa_optimizer.py`)
- **Algorithm**: Inner-loop meta-learning optimization
- **Process**:
  1. Generate critique of current prompt
  2. Create improved version based on critique
  3. Evaluate improvement using reward model
  4. Iterate until convergence or max iterations
- **Reward Model**: User-aligned with weights for:
  - Quality (40%)
  - Alignment (30%)
  - Efficiency (20%)
  - Safety (10%)

#### Evolutionary Optimizer (`evolutionary.py`)
- **Algorithm**: Genetic algorithm (PromptBreeder)
- **Process**:
  1. Initialize population of prompt variations
  2. Evaluate fitness of each individual
  3. Select parents via tournament selection
  4. Apply crossover and mutation
  5. Repeat for specified generations
- **Operators**:
  - Mutation: Create variations of prompts
  - Crossover: Combine elements from two prompts
  - Selection: Tournament-based

#### Self-Critique Optimizer (`self_critique.py`)
- **Algorithm**: Iterative self-critique (PromptWizard)
- **Process**:
  1. Generate self-critique of current prompt
  2. Refine prompt based on critique
  3. Evaluate quality
  4. Repeat for specified rounds
- **Dimensions**:
  - Clarity
  - Completeness
  - Relevance
  - Creativity
  - Safety

### 3. Knowledge Components (`src/knowledge/`)

#### Knowledge Retriever (`retrieval.py`)
- **Purpose**: Retrieve relevant information
- **Features**:
  - Web search integration (placeholder)
  - RAG support
  - Result ranking
  - Caching

#### Fact Checker (`fact_checker.py`)
- **Purpose**: Validate factual claims
- **Features**:
  - Claim extraction
  - Verification
  - Confidence scoring

#### Citation Manager (`citation_manager.py`)
- **Purpose**: Manage source citations
- **Features**:
  - Citation formatting (APA, MLA, etc.)
  - Source tracking
  - Bibliography generation

### 4. Safety Components (`src/safety/`)

#### Alignment Checker (`alignment.py`)
- **Purpose**: Ensure content safety
- **Features**:
  - Keyword-based filtering
  - Content categorization
  - Confidence scoring
- **Levels**:
  - Safe: No concerns
  - Caution: Potential issues
  - Blocked: Clear violations

#### Policy Engine (`policy_engine.py`)
- **Purpose**: Enforce safety policies
- **Features**:
  - Policy loading from YAML
  - Violation detection
  - Alternative suggestions
  - Creative compliance
- **Modes**:
  - Strict: Block violations
  - Moderate: Allow with warnings

#### Audit Logger (`audit_logger.py`)
- **Purpose**: Track system decisions
- **Features**:
  - Structured logging (JSONL)
  - Event categorization
  - Data anonymization
  - Retention management
- **Events Logged**:
  - Optimization requests
  - Safety violations
  - Policy enforcement
  - Performance metrics

### 5. Web Interface (`src/web/`)

#### Backend (`backend.py`)
- **Framework**: FastAPI
- **Endpoints**:
  - GET `/`: Web interface
  - GET `/api/health`: Health check
  - POST `/api/analyze`: Task analysis
  - POST `/api/optimize`: Prompt optimization
  - POST `/api/generate`: Text generation
  - WebSocket `/ws/optimize`: Real-time optimization
- **Features**:
  - CORS support
  - Automatic OpenAPI documentation
  - WebSocket for real-time updates
  - Error handling

#### Frontend (`frontend/index.html`)
- **Technology**: Vanilla JavaScript + HTML5 + CSS3
- **Features**:
  - Tabbed interface
  - Real-time status updates
  - Responsive design
  - Interactive API calls

## Data Flow

### Typical Optimization Flow

```
1. User Request
   ↓
2. Task Analysis
   - Classify task type
   - Assess complexity
   - Detect safety flags
   ↓
3. Safety Check
   - Alignment verification
   - Policy compliance
   ↓
4. Prompt Building
   - Select template
   - Add context
   - Inject examples
   ↓
5. Optimization
   - Apply selected strategy
   - Iterate improvements
   - Track performance
   ↓
6. Safety Validation
   - Check optimized prompt
   - Verify alignment
   ↓
7. Audit Logging
   - Record decisions
   - Log metrics
   ↓
8. Response
   - Return optimized prompt
   - Include metadata
```

## Configuration Management

### YAML Configuration Files

1. **models.yaml**: LLM and embedding model settings
2. **optimization.yaml**: Algorithm parameters
3. **safety.yaml**: Safety and alignment policies

### Environment Variables

- Loaded from `.env` file
- Override defaults
- Sensitive data (API keys)

## Extension Points

### Adding New Optimizers

```python
from src.optimization.base import BaseOptimizer

class MyOptimizer(BaseOptimizer):
    def optimize(self, prompt, task_analysis):
        # Implementation
        return optimized_prompt
```

### Adding New Safety Checks

```python
from src.safety.base import SafetyCheck

class MyCheck(SafetyCheck):
    def check(self, content):
        # Implementation
        return {"safe": True, "flags": []}
```

### Adding New API Endpoints

```python
from src.web.backend import app

@app.post("/api/my-endpoint")
async def my_endpoint(request: MyRequest):
    # Implementation
    return response
```

## Performance Considerations

### Caching
- LLM responses can be cached
- Configuration loaded once at startup
- Compiled regex patterns

### Async Operations
- FastAPI runs async by default
- LLM calls can be parallelized
- WebSocket for non-blocking updates

### Monitoring
- Performance metrics tracked
- Latency monitoring
- Token usage tracking
- Audit logs for analysis

## Security Considerations

### API Key Protection
- Never commit API keys
- Use environment variables
- Validate on startup

### Input Validation
- Pydantic models for request validation
- Length limits
- Type checking

### Safety Layers
- Pre-generation safety checks
- Post-generation validation
- Policy enforcement
- Audit logging

## Deployment Architecture

### Docker Deployment
```
┌─────────────────────┐
│   Docker Container  │
│  ┌───────────────┐  │
│  │  APOS Backend │  │
│  └───────────────┘  │
│         ↓           │
│  ┌───────────────┐  │
│  │  Config Files │  │
│  └───────────────┘  │
└─────────────────────┘
         ↓
┌─────────────────────┐
│  External Services  │
│  - Google Gemini    │
│  - (Future: DB)     │
└─────────────────────┘
```

### Scalability Options
- Horizontal scaling behind load balancer
- Redis for distributed caching (future)
- Database for persistence (future)
- Message queue for async tasks (future)

## Future Enhancements

1. **Multi-Model Support**: OpenAI, Anthropic, etc.
2. **Advanced RAG**: Vector database integration
3. **Fine-Tuning**: Custom model adaptation
4. **Distributed Optimization**: Parallel strategy execution
5. **Analytics Dashboard**: Visualization of metrics
6. **User Authentication**: API key management
7. **Rate Limiting**: Request throttling
8. **Model Caching**: Response caching layer
