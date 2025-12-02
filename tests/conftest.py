"""
Pytest configuration for DeepEval tests

This file configures DeepEval to use Ollama instead of OpenAI for all metrics.
This is automatically loaded by pytest before running tests.
"""
import pytest
from src.ollama_deepeval_model import OllamaModel


@pytest.fixture(scope="session", autouse=True)
def configure_deepeval_model():
    """
    Configure DeepEval to use Ollama model globally
    
    This fixture runs once per test session and sets the default model
    for all DeepEval metrics to use Ollama instead of OpenAI.
    """
    # Create Ollama model instance
    ollama_model = OllamaModel(model_name="llama3")
    
    # This model will be used when metrics are initialized
    return ollama_model


@pytest.fixture(scope="session")
def deepeval_model():
    """Provide Ollama model for explicit use in tests"""
    return OllamaModel(model_name="llama3")
