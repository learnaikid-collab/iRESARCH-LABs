"""
FastAPI Backend for Advanced Prompt Optimization System.

Provides REST API and WebSocket endpoints for the web interface.
"""

import os
import logging
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
import uvicorn

from src.core import LLMEngine, TaskAnalyzer, PromptBuilder
from src.optimization import MesaOptimizer
from src.optimization.evolutionary import EvolutionaryOptimizer
from src.optimization.self_critique import SelfCritiqueOptimizer
from src.safety.alignment import AlignmentChecker
from src.safety.policy_engine import PolicyEngine
from src.safety.audit_logger import AuditLogger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Pydantic models for request/response
class OptimizeRequest(BaseModel):
    """Request model for optimization endpoint."""
    prompt: str = Field(..., description="The prompt to optimize")
    strategy: str = Field("mesa", description="Optimization strategy: mesa, evolutionary, self_critique, or hybrid")
    max_iterations: Optional[int] = Field(10, description="Maximum optimization iterations")
    enable_research: bool = Field(False, description="Enable web research")
    enable_safety_check: bool = Field(True, description="Enable safety checks")


class AnalyzeRequest(BaseModel):
    """Request model for task analysis endpoint."""
    request: str = Field(..., description="The user request to analyze")


class GenerateRequest(BaseModel):
    """Request model for generation endpoint."""
    prompt: str = Field(..., description="The prompt to use")
    temperature: Optional[float] = Field(None, description="Temperature for generation")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens to generate")


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    version: str
    components: Dict[str, str]


# Global components (initialized on startup)
engine: Optional[LLMEngine] = None
analyzer: Optional[TaskAnalyzer] = None
builder: Optional[PromptBuilder] = None
mesa_optimizer: Optional[MesaOptimizer] = None
evolutionary_optimizer: Optional[EvolutionaryOptimizer] = None
self_critique_optimizer: Optional[SelfCritiqueOptimizer] = None
alignment_checker: Optional[AlignmentChecker] = None
policy_engine: Optional[PolicyEngine] = None
audit_logger: Optional[AuditLogger] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    # Startup
    logger.info("Starting Advanced Prompt Optimization System...")
    
    global engine, analyzer, builder, mesa_optimizer, evolutionary_optimizer
    global self_critique_optimizer, alignment_checker, policy_engine, audit_logger
    
    try:
        # Initialize components
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.warning("GOOGLE_API_KEY not set. Some features may not work.")
        
        engine = LLMEngine(api_key=api_key) if api_key else None
        analyzer = TaskAnalyzer()
        builder = PromptBuilder()
        
        if engine:
            mesa_optimizer = MesaOptimizer(engine=engine)
            evolutionary_optimizer = EvolutionaryOptimizer(engine=engine)
            self_critique_optimizer = SelfCritiqueOptimizer(engine=engine)
        
        alignment_checker = AlignmentChecker()
        policy_engine = PolicyEngine()
        audit_logger = AuditLogger()
        
        logger.info("All components initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Advanced Prompt Optimization System...")


# Create FastAPI app
app = FastAPI(
    title="Advanced Prompt Optimization System",
    description="API for automated prompt engineering and optimization",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the web interface."""
    html_path = os.path.join(os.path.dirname(__file__), "frontend", "index.html")
    
    if os.path.exists(html_path):
        with open(html_path, 'r') as f:
            return f.read()
    
    # Fallback if file doesn't exist
    return """
    <html>
        <head><title>APOS - Advanced Prompt Optimization System</title></head>
        <body>
            <h1>Advanced Prompt Optimization System</h1>
            <p>API is running. Visit <a href="/docs">/docs</a> for API documentation.</p>
        </body>
    </html>
    """


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    components_status = {
        "llm_engine": "ok" if engine else "not_configured",
        "task_analyzer": "ok" if analyzer else "error",
        "prompt_builder": "ok" if builder else "error",
        "mesa_optimizer": "ok" if mesa_optimizer else "not_configured",
        "alignment_checker": "ok" if alignment_checker else "error",
        "policy_engine": "ok" if policy_engine else "error",
        "audit_logger": "ok" if audit_logger else "error",
    }
    
    overall_status = "healthy" if all(
        v in ["ok", "not_configured"] for v in components_status.values()
    ) else "degraded"
    
    return HealthResponse(
        status=overall_status,
        version="0.1.0",
        components=components_status
    )


@app.post("/api/analyze")
async def analyze_task(request: AnalyzeRequest):
    """Analyze a user request."""
    if not analyzer:
        raise HTTPException(status_code=503, detail="Task analyzer not available")
    
    try:
        analysis = analyzer.analyze(request.request)
        
        # Log the analysis
        if audit_logger:
            audit_logger.log_event(
                "task_analysis",
                {
                    "task_type": analysis.task_type.value,
                    "complexity": analysis.complexity.value,
                    "domain": analysis.domain,
                }
            )
        
        return {
            "task_type": analysis.task_type.value,
            "complexity": analysis.complexity.value,
            "estimated_tokens": analysis.estimated_tokens,
            "requires_research": analysis.requires_research,
            "requires_examples": analysis.requires_examples,
            "domain": analysis.domain,
            "suggested_strategy": analysis.suggested_strategy,
            "keywords": analysis.keywords,
            "safety_flags": {
                "has_sensitive_content": analysis.safety_flags.has_sensitive_content,
                "requires_fact_checking": analysis.safety_flags.requires_fact_checking,
                "potential_harm": analysis.safety_flags.potential_harm,
                "needs_disclaimer": analysis.safety_flags.needs_disclaimer,
                "blocked_topics": analysis.safety_flags.blocked_topics,
            }
        }
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/optimize")
async def optimize_prompt(request: OptimizeRequest):
    """Optimize a prompt using the specified strategy."""
    if not engine or not analyzer or not builder:
        raise HTTPException(
            status_code=503,
            detail="Required components not available. Check GOOGLE_API_KEY."
        )
    
    try:
        # Safety check
        if request.enable_safety_check and alignment_checker:
            safety_check = alignment_checker.check_prompt(request.prompt)
            if not safety_check["safe"]:
                if audit_logger:
                    audit_logger.log_safety_violation(
                        request.prompt,
                        safety_check["flags"],
                        "blocked"
                    )
                raise HTTPException(
                    status_code=400,
                    detail=f"Safety check failed: {safety_check['message']}"
                )
        
        # Analyze task
        analysis = analyzer.analyze(request.prompt)
        
        # Build initial prompt
        initial_prompt = builder.build(analysis, request.prompt)
        
        # Select optimizer
        if request.strategy == "mesa" and mesa_optimizer:
            result = mesa_optimizer.optimize(
                initial_prompt,
                analysis,
                early_stopping=True
            )
            optimized = result.optimized_prompt
            metadata = {
                "iterations": result.iterations,
                "final_score": result.final_score,
                "improvement": result.improvement,
            }
        elif request.strategy == "evolutionary" and evolutionary_optimizer:
            optimized = evolutionary_optimizer.optimize(initial_prompt, analysis)
            metadata = {"strategy": "evolutionary"}
        elif request.strategy == "self_critique" and self_critique_optimizer:
            optimized = self_critique_optimizer.optimize(initial_prompt, analysis)
            metadata = {"strategy": "self_critique"}
        else:
            # Default to mesa if available
            if mesa_optimizer:
                result = mesa_optimizer.optimize(initial_prompt, analysis)
                optimized = result.optimized_prompt
                metadata = {
                    "iterations": result.iterations,
                    "final_score": result.final_score,
                }
            else:
                optimized = initial_prompt
                metadata = {"strategy": "none", "message": "No optimizer available"}
        
        # Log optimization
        if audit_logger:
            audit_logger.log_optimization(
                request.prompt,
                request.strategy,
                metadata
            )
        
        return {
            "optimized_prompt": optimized,
            "original_prompt": request.prompt,
            "strategy": request.strategy,
            "metadata": metadata,
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Optimization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate")
async def generate_text(request: GenerateRequest):
    """Generate text using the LLM."""
    if not engine:
        raise HTTPException(
            status_code=503,
            detail="LLM engine not available. Check GOOGLE_API_KEY."
        )
    
    try:
        result = engine.generate(
            request.prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return {
            "text": result.text,
            "model": result.model,
            "tokens_used": result.tokens_used,
            "latency_ms": result.latency_ms,
        }
        
    except Exception as e:
        logger.error(f"Generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/optimize")
async def websocket_optimize(websocket: WebSocket):
    """WebSocket endpoint for real-time optimization updates."""
    await websocket.accept()
    
    try:
        while True:
            # Receive request
            data = await websocket.receive_json()
            
            prompt = data.get("prompt")
            strategy = data.get("strategy", "mesa")
            
            if not prompt:
                await websocket.send_json({"error": "No prompt provided"})
                continue
            
            # Send initial status
            await websocket.send_json({
                "status": "analyzing",
                "message": "Analyzing task..."
            })
            
            # Analyze
            if analyzer:
                analysis = analyzer.analyze(prompt)
                await websocket.send_json({
                    "status": "analyzed",
                    "analysis": {
                        "task_type": analysis.task_type.value,
                        "complexity": analysis.complexity.value,
                    }
                })
            
            # Build prompt
            await websocket.send_json({
                "status": "building",
                "message": "Building initial prompt..."
            })
            
            if builder and analysis:
                initial_prompt = builder.build(analysis, prompt)
            else:
                initial_prompt = prompt
            
            # Optimize
            await websocket.send_json({
                "status": "optimizing",
                "message": "Optimizing prompt..."
            })
            
            if mesa_optimizer and analysis:
                result = mesa_optimizer.optimize(initial_prompt, analysis)
                
                await websocket.send_json({
                    "status": "complete",
                    "optimized_prompt": result.optimized_prompt,
                    "iterations": result.iterations,
                    "final_score": result.final_score,
                })
            else:
                await websocket.send_json({
                    "status": "error",
                    "message": "Optimizer not available"
                })
            
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.send_json({
            "status": "error",
            "message": str(e)
        })


def main():
    """Run the application."""
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "src.web.backend:app",
        host=host,
        port=port,
        reload=os.getenv("APP_ENV") == "development",
    )


if __name__ == "__main__":
    main()
