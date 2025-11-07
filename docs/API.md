# API Reference

## Overview

The Advanced Prompt Optimization System (APOS) provides a RESTful API and WebSocket interface for prompt optimization, task analysis, and text generation.

Base URL: `http://localhost:8000`

## Authentication

Currently, the API does not require authentication. In production, implement API key authentication.

## Endpoints

### Health Check

**GET** `/api/health`

Check the health status of the system and its components.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "components": {
    "llm_engine": "ok",
    "task_analyzer": "ok",
    "prompt_builder": "ok",
    "mesa_optimizer": "ok",
    "alignment_checker": "ok",
    "policy_engine": "ok",
    "audit_logger": "ok"
  }
}
```

### Task Analysis

**POST** `/api/analyze`

Analyze a user request to determine task characteristics.

**Request Body:**
```json
{
  "request": "Write a research paper on climate change"
}
```

**Response:**
```json
{
  "task_type": "research",
  "complexity": "complex",
  "estimated_tokens": 2048,
  "requires_research": true,
  "requires_examples": false,
  "domain": "science",
  "suggested_strategy": "hybrid",
  "keywords": ["research", "paper", "climate", "change"],
  "safety_flags": {
    "has_sensitive_content": false,
    "requires_fact_checking": true,
    "potential_harm": false,
    "needs_disclaimer": false,
    "blocked_topics": []
  }
}
```

### Prompt Optimization

**POST** `/api/optimize`

Optimize a prompt using the specified strategy.

**Request Body:**
```json
{
  "prompt": "Explain quantum computing to a 10-year-old",
  "strategy": "mesa",
  "max_iterations": 10,
  "enable_research": false,
  "enable_safety_check": true
}
```

**Parameters:**
- `prompt` (string, required): The prompt to optimize
- `strategy` (string, optional): Optimization strategy - "mesa", "evolutionary", "self_critique", or "hybrid" (default: "mesa")
- `max_iterations` (integer, optional): Maximum optimization iterations (default: 10)
- `enable_research` (boolean, optional): Enable web research (default: false)
- `enable_safety_check` (boolean, optional): Enable safety checks (default: true)

**Response:**
```json
{
  "optimized_prompt": "You are an expert educator...",
  "original_prompt": "Explain quantum computing to a 10-year-old",
  "strategy": "mesa",
  "metadata": {
    "iterations": 7,
    "final_score": 0.92,
    "improvement": 0.35
  }
}
```

### Text Generation

**POST** `/api/generate`

Generate text using the LLM with a given prompt.

**Request Body:**
```json
{
  "prompt": "Write a short story about a robot",
  "temperature": 0.7,
  "max_tokens": 500
}
```

**Parameters:**
- `prompt` (string, required): The prompt to use for generation
- `temperature` (float, optional): Temperature for generation (0.0-1.0)
- `max_tokens` (integer, optional): Maximum tokens to generate

**Response:**
```json
{
  "text": "Once upon a time, there was a robot named...",
  "model": "gemini-2.0-flash-exp",
  "tokens_used": 423,
  "latency_ms": 1250.5
}
```

### WebSocket: Real-Time Optimization

**WebSocket** `/ws/optimize`

Real-time optimization with progress updates via WebSocket.

**Send:**
```json
{
  "prompt": "Explain machine learning",
  "strategy": "mesa"
}
```

**Receive (multiple messages):**
```json
{
  "status": "analyzing",
  "message": "Analyzing task..."
}
```

```json
{
  "status": "analyzed",
  "analysis": {
    "task_type": "technical_explanation",
    "complexity": "moderate"
  }
}
```

```json
{
  "status": "optimizing",
  "message": "Optimizing prompt..."
}
```

```json
{
  "status": "complete",
  "optimized_prompt": "You are an expert in machine learning...",
  "iterations": 5,
  "final_score": 0.88
}
```

## Error Responses

All endpoints may return standard HTTP error responses:

**400 Bad Request**
```json
{
  "detail": "Safety check failed: Found concerning keywords: violence"
}
```

**422 Validation Error**
```json
{
  "detail": [
    {
      "loc": ["body", "prompt"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**500 Internal Server Error**
```json
{
  "detail": "Optimization error: Connection timeout"
}
```

**503 Service Unavailable**
```json
{
  "detail": "LLM engine not available. Check GOOGLE_API_KEY."
}
```

## Rate Limiting

Currently, no rate limiting is implemented. For production use, implement appropriate rate limiting based on your requirements.

## Interactive Documentation

The API provides interactive documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
