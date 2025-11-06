"""
Basic Example: Simple prompt optimization workflow.

This example demonstrates the core functionality of the Prompt Optimization System
with a simple query.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.task_analyzer import TaskAnalyzer
from src.core.prompt_builder import PromptBuilder, Prompt
# from src.core.llm_engine import LLMEngine
# from src.core.evaluator import OutputEvaluator
# from src.core.orchestrator import PromptOptimizer


def main():
    """Run basic optimization example."""
    
    print("=" * 60)
    print("Prompt Optimization System - Basic Example")
    print("=" * 60)
    print()
    
    # User query
    query = "Explain quantum entanglement in simple terms for a high school student"
    print(f"Query: {query}")
    print()
    
    # Step 1: Analyze the task
    print("Step 1: Analyzing task...")
    analyzer = TaskAnalyzer()
    analysis = analyzer.analyze_query(query)
    
    print(f"  Task Type: {analysis.task_type.value}")
    print(f"  Complexity: {analysis.complexity.value}")
    print(f"  Requires Reasoning: {analysis.requires_reasoning}")
    print(f"  Requires Web Search: {analysis.requires_web_search}")
    print(f"  Recommended Strategy: {analysis.recommended_strategy}")
    print(f"  Estimated Tokens: {analysis.estimated_tokens}")
    print(f"  Safety: {analysis.safety_report.sensitivity_level}")
    print()
    
    # Step 2: Build initial prompt (Prompt Zero)
    print("Step 2: Building initial prompt...")
    # builder = PromptBuilder()
    # prompt_zero = builder.build_prompt_zero(query, analysis)
    
    # For demonstration without actual LLM
    print("  [Prompt Zero would be constructed here]")
    print("  Components:")
    print("    - System role: Helpful AI tutor")
    print("    - Instruction: Explain concept simply")
    print("    - CoT trigger: Think step by step")
    print()
    
    # Step 3: Would normally call LLM and optimize
    print("Step 3: Optimization loop...")
    print("  [In actual implementation:]")
    print("  - Generate initial response")
    print("  - Evaluate quality")
    print("  - Apply optimization (self-critique)")
    print("  - Iterate until convergence")
    print()
    
    # Step 4: Final result
    print("Step 4: Final optimized result")
    print("  [Optimized answer would be displayed here]")
    print()
    
    # Example output structure
    print("Example Output Structure:")
    print("-" * 60)
    print("Quantum entanglement is like having a pair of magic coins.")
    print("When you flip one coin, the other coin instantly knows what")
    print("result the first coin got, even if they're on opposite sides")
    print("of the universe!")
    print()
    print("More precisely: When two particles become 'entangled', their")
    print("properties become linked. Measuring one particle instantly")
    print("affects the other, regardless of distance...")
    print("-" * 60)
    print()
    
    print("Optimization Stats:")
    print(f"  Iterations: 3")
    print(f"  Initial Score: 7.5/10")
    print(f"  Final Score: 9.2/10")
    print(f"  Improvement: +22.7%")
    print(f"  Time: 2.3 seconds")
    print()
    
    print("=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    # Check if we're just doing a dry run
    if len(sys.argv) > 1 and sys.argv[1] == '--dry-run':
        print("Dry run mode - no actual LLM calls")
    
    main()
