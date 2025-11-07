"""
LLM Engine for interfacing with Google Gemini 2.5 Flash.

Provides a unified interface for LLM operations including generation,
error handling, retries, and performance monitoring.
"""

import os
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


@dataclass
class GenerationConfig:
    """Configuration for text generation."""
    temperature: float = 0.7
    max_tokens: int = 8192
    top_p: float = 0.95
    top_k: int = 40
    timeout: int = 30


@dataclass
class GenerationResult:
    """Result of a generation request."""
    text: str
    model: str
    tokens_used: int = 0
    latency_ms: float = 0.0
    finish_reason: str = "complete"
    metadata: Dict[str, Any] = field(default_factory=dict)


class LLMEngine:
    """
    LLM Engine for interacting with Google Gemini 2.5 Flash.
    
    Features:
    - Automatic retry with exponential backoff
    - Performance monitoring
    - Error handling and logging
    - Token usage tracking
    - Response caching (future)
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-2.0-flash-exp",
        config: Optional[GenerationConfig] = None,
    ):
        """
        Initialize the LLM Engine.
        
        Args:
            api_key: Google API key (defaults to GOOGLE_API_KEY env var)
            model: Model name to use
            config: Generation configuration
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable.")
        
        self.model_name = model
        self.config = config or GenerationConfig()
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                "temperature": self.config.temperature,
                "top_p": self.config.top_p,
                "top_k": self.config.top_k,
                "max_output_tokens": self.config.max_tokens,
            }
        )
        
        # Performance tracking
        self.total_requests = 0
        self.total_tokens = 0
        self.total_latency_ms = 0.0
        
        logger.info(f"LLM Engine initialized with model: {self.model_name}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system_instruction: Optional[str] = None,
    ) -> GenerationResult:
        """
        Generate text from a prompt.
        
        Args:
            prompt: The input prompt
            temperature: Override default temperature
            max_tokens: Override default max tokens
            system_instruction: Optional system instruction
            
        Returns:
            GenerationResult with generated text and metadata
        """
        start_time = time.time()
        
        try:
            # Update config if overrides provided
            gen_config = {
                "temperature": temperature or self.config.temperature,
                "max_output_tokens": max_tokens or self.config.max_tokens,
                "top_p": self.config.top_p,
                "top_k": self.config.top_k,
            }
            
            # Create model with system instruction if provided
            if system_instruction:
                model = genai.GenerativeModel(
                    model_name=self.model_name,
                    generation_config=gen_config,
                    system_instruction=system_instruction
                )
            else:
                model = genai.GenerativeModel(
                    model_name=self.model_name,
                    generation_config=gen_config
                )
            
            # Generate response
            response = model.generate_content(prompt)
            
            # Calculate latency
            latency_ms = (time.time() - start_time) * 1000
            
            # Extract text
            text = response.text if hasattr(response, 'text') else ""
            
            # Estimate tokens (rough estimate: 1 token ≈ 4 characters)
            tokens_used = len(prompt + text) // 4
            
            # Update stats
            self.total_requests += 1
            self.total_tokens += tokens_used
            self.total_latency_ms += latency_ms
            
            result = GenerationResult(
                text=text,
                model=self.model_name,
                tokens_used=tokens_used,
                latency_ms=latency_ms,
                finish_reason="complete",
                metadata={
                    "prompt_length": len(prompt),
                    "response_length": len(text),
                }
            )
            
            logger.debug(f"Generated {len(text)} chars in {latency_ms:.2f}ms")
            
            return result
            
        except Exception as e:
            logger.error(f"Generation error: {str(e)}")
            raise
    
    def generate_batch(
        self,
        prompts: List[str],
        **kwargs
    ) -> List[GenerationResult]:
        """
        Generate text for multiple prompts.
        
        Args:
            prompts: List of input prompts
            **kwargs: Additional generation parameters
            
        Returns:
            List of GenerationResult objects
        """
        results = []
        for prompt in prompts:
            try:
                result = self.generate(prompt, **kwargs)
                results.append(result)
            except Exception as e:
                logger.error(f"Batch generation error for prompt: {str(e)}")
                # Return empty result for failed generations
                results.append(GenerationResult(
                    text="",
                    model=self.model_name,
                    finish_reason="error",
                    metadata={"error": str(e)}
                ))
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics.
        
        Returns:
            Dictionary with performance metrics
        """
        avg_latency = (
            self.total_latency_ms / self.total_requests 
            if self.total_requests > 0 
            else 0
        )
        
        return {
            "total_requests": self.total_requests,
            "total_tokens": self.total_tokens,
            "total_latency_ms": self.total_latency_ms,
            "avg_latency_ms": avg_latency,
            "model": self.model_name,
        }
    
    def reset_stats(self):
        """Reset performance statistics."""
        self.total_requests = 0
        self.total_tokens = 0
        self.total_latency_ms = 0.0
        logger.info("Performance statistics reset")
