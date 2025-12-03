"""
Pytest configuration for DeepEval tests
"""
import pytest


@pytest.fixture
def llm_client():
    """Provide OpenAI LLM client for tests"""
    from src.llm_client import SecurityLLMClient
    return SecurityLLMClient()


@pytest.fixture
def rag_client():
    """Provide OpenAI RAG client for tests"""
    from src.rag_client import SecurityRAGClient
    return SecurityRAGClient()
