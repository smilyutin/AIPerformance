"""
Test package for DeepEval security tests

Test suites included:
- test_accuracy: Response accuracy and relevancy tests
- test_hallucination: Hallucination detection tests
- test_rag: RAG retrieval and generation tests
- test_prompt_regression: Prompt version regression tests

Run all tests:
    pytest tests/ -v

Run specific suite:
    pytest tests/test_accuracy.py -v
"""

# Test package - no exports needed
# Tests are discovered automatically by pytest
__version__ = "0.1.0"
