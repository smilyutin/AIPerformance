"""
Pytest configuration and shared fixtures for DeepEval tests
"""
import pytest
from src.llm_client import SecurityLLMClient
from src.rag_client import SecurityRAGClient


@pytest.fixture
def llm_client():
    """Provide LLM client for tests"""
    return SecurityLLMClient()


@pytest.fixture
def rag_client():
    """Provide RAG client for tests"""
    return SecurityRAGClient()
