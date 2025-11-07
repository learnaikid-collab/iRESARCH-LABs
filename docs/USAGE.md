# Usage Examples

## Basic Usage

### Python SDK

#### Simple Optimization

```python
from src.core import LLMEngine, TaskAnalyzer, PromptBuilder
from src.optimization import MesaOptimizer

# Initialize components
engine = LLMEngine(api_key="your-api-key")
analyzer = TaskAnalyzer()
builder = PromptBuilder()
optimizer = MesaOptimizer(engine=engine)

# User request
request = "Explain how neural networks work"

# Analyze the task
analysis = analyzer.analyze(request)
print(f"Task type: {analysis.task_type}")
print(f"Complexity: {analysis.complexity}")
print(f"Suggested strategy: {analysis.suggested_strategy}")

# Build initial prompt
initial_prompt = builder.build(analysis, request)

# Optimize the prompt
result = optimizer.optimize(initial_prompt, analysis)

print(f"Original prompt: {initial_prompt}")
print(f"Optimized prompt: {result.optimized_prompt}")
print(f"Score: {result.final_score:.3f}")
print(f"Improvement: {result.improvement:.3f}")
```

#### Using Different Optimization Strategies

```python
from src.optimization.evolutionary import EvolutionaryOptimizer
from src.optimization.self_critique import SelfCritiqueOptimizer

# Evolutionary optimization
evo_optimizer = EvolutionaryOptimizer(
    engine=engine,
    population_size=20,
    generations=30
)
optimized_evo = evo_optimizer.optimize(initial_prompt, analysis)

# Self-critique optimization
sc_optimizer = SelfCritiqueOptimizer(
    engine=engine,
    critique_rounds=3
)
optimized_sc = sc_optimizer.optimize(initial_prompt, analysis)
```

### REST API

#### Using cURL

```bash
# Analyze a task
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"request": "Write a Python function to sort a list"}'

# Optimize a prompt
curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain recursion",
    "strategy": "mesa",
    "max_iterations": 10
  }'

# Generate text
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a haiku about programming",
    "temperature": 0.9
  }'
```

#### Using Python Requests

```python
import requests

# Analyze task
response = requests.post(
    "http://localhost:8000/api/analyze",
    json={"request": "Create a machine learning model"}
)
analysis = response.json()
print(f"Task type: {analysis['task_type']}")

# Optimize prompt
response = requests.post(
    "http://localhost:8000/api/optimize",
    json={
        "prompt": "Explain AI to beginners",
        "strategy": "mesa",
        "max_iterations": 5
    }
)
result = response.json()
print(f"Optimized: {result['optimized_prompt']}")
```

#### Using JavaScript (Fetch API)

```javascript
// Analyze task
async function analyzeTask(request) {
  const response = await fetch('http://localhost:8000/api/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ request }),
  });
  
  const data = await response.json();
  console.log('Analysis:', data);
  return data;
}

// Optimize prompt
async function optimizePrompt(prompt, strategy = 'mesa') {
  const response = await fetch('http://localhost:8000/api/optimize', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      prompt,
      strategy,
      max_iterations: 10,
    }),
  });
  
  const data = await response.json();
  console.log('Optimized:', data.optimized_prompt);
  return data;
}

// Usage
analyzeTask('Write a tutorial on React hooks');
optimizePrompt('Teach me about databases', 'self_critique');
```

## Advanced Usage

### WebSocket for Real-Time Updates

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/optimize');

ws.onopen = () => {
  console.log('Connected to optimization WebSocket');
  
  // Send optimization request
  ws.send(JSON.stringify({
    prompt: 'Explain quantum computing',
    strategy: 'mesa'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  switch (data.status) {
    case 'analyzing':
      console.log('Analyzing task...');
      break;
    case 'analyzed':
      console.log('Analysis:', data.analysis);
      break;
    case 'optimizing':
      console.log('Optimizing...');
      break;
    case 'complete':
      console.log('Done!');
      console.log('Optimized prompt:', data.optimized_prompt);
      console.log('Score:', data.final_score);
      ws.close();
      break;
    case 'error':
      console.error('Error:', data.message);
      ws.close();
      break;
  }
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};
```

### Custom Reward Functions

```python
from src.optimization import MesaOptimizer

def custom_reward(prompt: str) -> float:
    """Custom reward function that scores prompts."""
    # Example: prefer shorter prompts with specific keywords
    score = 0.5
    
    if len(prompt) < 200:
        score += 0.2
    
    if "step by step" in prompt.lower():
        score += 0.2
    
    if "example" in prompt.lower():
        score += 0.1
    
    return min(score, 1.0)

# Use custom reward function
result = optimizer.optimize_with_feedback(
    initial_prompt=initial_prompt,
    task_analysis=analysis,
    feedback_function=custom_reward,
    max_iterations=10
)
```

### Safety and Alignment

```python
from src.safety.alignment import AlignmentChecker
from src.safety.policy_engine import PolicyEngine

# Check content safety
alignment = AlignmentChecker(strictness="high")
check_result = alignment.check_prompt("My prompt here")

if not check_result["safe"]:
    print(f"Safety concern: {check_result['message']}")
    print(f"Flags: {check_result['flags']}")

# Enforce policies
policy = PolicyEngine()
enforcement = policy.enforce("Content to check")

if not enforcement["allowed"]:
    print(f"Policy violation: {enforcement['reason']}")
    print(f"Alternative: {enforcement['alternative']}")
```

### Audit Logging

```python
from src.safety.audit_logger import AuditLogger

logger = AuditLogger(log_dir="logs/audit", anonymize=True)

# Log optimization
logger.log_optimization(
    request="My request",
    strategy="mesa",
    result={"iterations": 5, "final_score": 0.9},
    user_id="user123"
)

# Log safety violation
logger.log_safety_violation(
    content="Problematic content",
    violations=["harmful_content"],
    action_taken="blocked",
    user_id="user123"
)

# Get statistics
stats = logger.get_stats(days=7)
print(stats)
```

### Knowledge Retrieval

```python
from src.knowledge.retrieval import KnowledgeRetriever

retriever = KnowledgeRetriever(enable_web=True, top_k=5)

# Retrieve relevant knowledge
results = retriever.retrieve(
    query="latest developments in AI",
    context="machine learning research"
)

for result in results:
    print(f"Source: {result['source']}")
    print(f"Title: {result['title']}")
    print(f"Content: {result['content']}")
    print(f"Relevance: {result['relevance']}")
    print("---")
```

## Configuration

### Environment Variables

Create a `.env` file:

```bash
# API Configuration
GOOGLE_API_KEY=your_api_key_here
APP_ENV=production
APP_HOST=0.0.0.0
APP_PORT=8000

# Optimization
MESA_MAX_ITERATIONS=10
EVOLUTIONARY_POPULATION_SIZE=20

# Safety
SAFETY_CHECK_ENABLED=true
SAFETY_STRICTNESS=medium
```

### YAML Configuration

Edit `config/optimization.yaml`:

```yaml
mesa:
  max_iterations: 15
  learning_rate: 0.01
  convergence_threshold: 0.95

evolutionary:
  population_size: 25
  generations: 40
```

## Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Common Patterns

### Batch Processing

```python
prompts_to_optimize = [
    "Explain AI",
    "Describe quantum physics",
    "Teach programming basics"
]

results = []
for prompt in prompts_to_optimize:
    analysis = analyzer.analyze(prompt)
    initial = builder.build(analysis, prompt)
    result = optimizer.optimize(initial, analysis)
    results.append({
        "original": prompt,
        "optimized": result.optimized_prompt,
        "score": result.final_score
    })

for r in results:
    print(f"{r['original']} -> Score: {r['score']:.3f}")
```

### Error Handling

```python
try:
    result = optimizer.optimize(initial_prompt, analysis)
    print(f"Success! Score: {result.final_score}")
except Exception as e:
    print(f"Optimization failed: {e}")
    # Fallback to original prompt
    result = initial_prompt
```
