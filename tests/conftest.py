"""
Pytest configuration for DeepEval tests

This file configures DeepEval to use Ollama instead of OpenAI for all metrics.
This is automatically loaded by pytest before running tests.
"""
import pytest
import subprocess
import time
import requests
from src.ollama_deepeval_model import OllamaModel


def check_ollama_status():
    """Check if Ollama server is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except (requests.ConnectionError, requests.Timeout):
        return False


def start_ollama_server():
    """Start Ollama server if not running"""
    try:
        # Start Ollama in background
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        # Wait for server to be ready
        max_retries = 10
        for _ in range(max_retries):
            time.sleep(1)
            if check_ollama_status():
                print("✓ Ollama server started successfully")
                return True
        return False
    except FileNotFoundError:
        print("✗ Ollama not found. Please install: https://ollama.com/download")
        return False


@pytest.fixture(scope="session", autouse=True)
def ensure_ollama_running():
    """Ensure Ollama server is running before tests start"""
    if not check_ollama_status():
        print("⚠ Ollama server not running, attempting to start...")
        if not start_ollama_server():
            pytest.exit("Failed to start Ollama server. Please run 'ollama serve' manually.")
    else:
        print("✓ Ollama server is already running")


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


@pytest.fixture(scope="session")
def shared_llm_client():
    """Shared Ollama LLM client for test performance"""
    from src.llm_client_ollama import OllamaSecurityClient
    return OllamaSecurityClient(model="llama3")


@pytest.fixture(scope="session")
def shared_rag_client():
    """Shared Ollama RAG client for test performance"""
    from src.rag_client_ollama import OllamaSecurityRAGClient
    return OllamaSecurityRAGClient(model="llama3")
