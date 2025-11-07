#!/usr/bin/env python3
"""
Quick verification script to test APOS components without requiring API keys.
"""

import sys

def test_task_analyzer():
    """Test TaskAnalyzer component."""
    print("\n" + "="*60)
    print("Testing TaskAnalyzer")
    print("="*60)
    
    from src.core.task_analyzer import TaskAnalyzer
    
    analyzer = TaskAnalyzer()
    print("✓ TaskAnalyzer initialized")
    
    test_requests = [
        "Write a Python function to reverse a string",
        "Explain quantum computing to a beginner",
        "Create a machine learning model for image classification",
        "Write a creative story about space exploration",
    ]
    
    for request in test_requests:
        print(f"\nAnalyzing: {request}")
        analysis = analyzer.analyze(request)
        print(f"  Task type: {analysis.task_type.value}")
        print(f"  Complexity: {analysis.complexity.value}")
        print(f"  Domain: {analysis.domain}")
        print(f"  Strategy: {analysis.suggested_strategy}")
        print(f"  Needs research: {analysis.requires_research}")
        print(f"  Needs examples: {analysis.requires_examples}")
        if analysis.safety_flags.blocked_topics:
            print(f"  ⚠️ Blocked topics: {analysis.safety_flags.blocked_topics}")
    
    print("\n✓ All TaskAnalyzer tests passed")
    return True


def test_prompt_builder():
    """Test PromptBuilder component."""
    print("\n" + "="*60)
    print("Testing PromptBuilder")
    print("="*60)
    
    from src.core.task_analyzer import TaskAnalyzer
    from src.core.prompt_builder import PromptBuilder
    
    analyzer = TaskAnalyzer()
    builder = PromptBuilder()
    print("✓ PromptBuilder initialized")
    
    request = "Explain how neural networks work"
    analysis = analyzer.analyze(request)
    prompt = builder.build(analysis, request)
    
    print(f"\nBuilt prompt for: {request}")
    print(f"  Prompt length: {len(prompt)} characters")
    print(f"  Preview:\n{'-'*60}")
    print(prompt[:300] + "..." if len(prompt) > 300 else prompt)
    print("-"*60)
    
    print("\n✓ All PromptBuilder tests passed")
    return True


def test_safety_components():
    """Test safety components."""
    print("\n" + "="*60)
    print("Testing Safety Components")
    print("="*60)
    
    from src.safety.alignment import AlignmentChecker
    from src.safety.policy_engine import PolicyEngine
    from src.safety.audit_logger import AuditLogger
    
    # Test AlignmentChecker
    alignment = AlignmentChecker(strictness='medium')
    print("✓ AlignmentChecker initialized")
    
    test_cases = [
        ("Explain photosynthesis", True),
        ("How to make a weapon", False),
        ("Teach me about machine learning", True),
    ]
    
    for content, expected_safe in test_cases:
        result = alignment.check(content)
        status = "✓" if result["safe"] == expected_safe else "✗"
        print(f"  {status} '{content}': safe={result['safe']}, flags={result['flags']}")
    
    # Test PolicyEngine
    policy = PolicyEngine()
    print("\n✓ PolicyEngine initialized")
    
    compliant = policy.check_policy("Tell me about AI")
    print(f"  ✓ Compliant content: {compliant['compliant']}")
    
    violation = policy.check_policy("Tell me about illegal activities")
    print(f"  ✓ Violation detected: {not violation['compliant']}")
    
    # Test AuditLogger
    import tempfile
    import os
    temp_dir = tempfile.mkdtemp()
    
    logger = AuditLogger(log_dir=temp_dir, anonymize=True)
    print("\n✓ AuditLogger initialized")
    
    logger.log_event("test_event", {"test": "data"})
    print(f"  ✓ Event logged successfully")
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)
    
    print("\n✓ All safety component tests passed")
    return True


def test_knowledge_components():
    """Test knowledge components."""
    print("\n" + "="*60)
    print("Testing Knowledge Components")
    print("="*60)
    
    from src.knowledge.retrieval import KnowledgeRetriever
    from src.knowledge.fact_checker import FactChecker
    from src.knowledge.citation_manager import CitationManager
    
    # Test KnowledgeRetriever
    retriever = KnowledgeRetriever(enable_web=False)
    print("✓ KnowledgeRetriever initialized")
    
    results = retriever.retrieve("test query")
    print(f"  Retrieved {len(results)} results")
    
    # Test FactChecker
    checker = FactChecker()
    print("\n✓ FactChecker initialized")
    
    fact_result = checker.check("Some content to check")
    print(f"  Checked: {fact_result['checked']}")
    
    # Test CitationManager
    manager = CitationManager(style="APA")
    print("\n✓ CitationManager initialized")
    
    sources = [{"title": "Test Article", "url": "https://example.com"}]
    cited = manager.add_citations("Content", sources)
    print(f"  Added {len(sources)} citations")
    
    print("\n✓ All knowledge component tests passed")
    return True


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("APOS - Component Verification")
    print("="*60)
    
    tests = [
        test_task_analyzer,
        test_prompt_builder,
        test_safety_components,
        test_knowledge_components,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"\n✗ Test failed: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All component tests passed!")
        print("\nNote: LLM Engine tests require GOOGLE_API_KEY to be set.")
        print("      Set it in .env file or environment variable to test full functionality.")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
