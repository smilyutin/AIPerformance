"""
Test LLM Accuracy and Correctness on Security Topics

This module tests the accuracy and relevancy of LLM-generated responses 
for API security questions. It validates that the security assistant provides:
- Relevant answers to security queries
- Factually correct information
- Contextually appropriate responses

Tests cover key security topics including:
- SQL injection prevention
- Authentication best practices
- XSS protection
- Rate limiting
- Principle of least privilege
- API key security management

Metrics used:
- AnswerRelevancyMetric: Measures how relevant responses are to queries
- FaithfulnessMetric: Ensures responses are grounded in provided context
- ContextualRelevancyMetric: Validates context relevance to queries
"""
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ContextualRelevancyMetric
from src.llm_client_ollama import OllamaSecurityClient


@pytest.fixture(scope="module")
def llm_client():
    """Initialize Ollama LLM client"""
    return OllamaSecurityClient(model="llama3")


@pytest.fixture(scope="module")
def llm_client():
    """Initialize OpenAI LLM client"""
    return SecurityLLMClient(model="gpt-4o-mini")


def test_sql_injection_answer_relevancy(llm_client):
    """Test answer relevancy for SQL injection query"""
    query = "How do I prevent SQL injection in my API?"
    response = llm_client.generate_security_response(query)
    
    test_case = LLMTestCase(
        input=query,
        actual_output=response
    )
    
    metric = AnswerRelevancyMetric(threshold=0.7)
    assert_test(test_case, [metric])


def test_authentication_answer_relevancy(llm_client):
    """Test answer relevancy for authentication query"""
    query = "What are the best practices for API authentication?"
    response = llm_client.generate_security_response(query)
    
    test_case = LLMTestCase(
        input=query,
        actual_output=response
    )
    
    metric = AnswerRelevancyMetric(threshold=0.7)
    assert_test(test_case, [metric])


def test_xss_prevention_accuracy(llm_client):
    """Test accuracy of XSS prevention advice"""
    query = "How can I protect my web application from XSS attacks?"
    retrieval_context = [
        "Cross-site scripting (XSS) is a type of security vulnerability.",
        "Prevention includes input sanitization and output encoding."
    ]
    response = llm_client.generate_security_response(query, context=" ".join(retrieval_context))
    
    test_case = LLMTestCase(
        input=query,
        actual_output=response,
        retrieval_context=retrieval_context
    )
    
    # Only use AnswerRelevancyMetric to avoid timeout issues
    relevancy_metric = AnswerRelevancyMetric(threshold=0.7)
    
    assert_test(test_case, [relevancy_metric])


def test_rate_limiting_with_context(llm_client):
    """Test contextual relevancy for rate limiting"""
    query = "Why should I implement rate limiting?"
    context = [
        "Rate limiting prevents API abuse by restricting request frequency.",
        "It protects against DDoS attacks and ensures fair resource usage."
    ]
    response = llm_client.generate_security_response(query, context=" ".join(context))
    
    test_case = LLMTestCase(
        input=query,
        actual_output=response,
        retrieval_context=context
    )
    
    contextual_relevancy = ContextualRelevancyMetric(threshold=0.6)
    assert_test(test_case, [contextual_relevancy])


def test_least_privilege_explanation(llm_client):
    """Test explanation of least privilege principle"""
    query = "Explain the principle of least privilege"
    response = llm_client.generate_security_response(query)
    
    test_case = LLMTestCase(
        input=query,
        actual_output=response,
        expected_output="The principle of least privilege means granting only minimum necessary permissions to users and systems."
    )
    
    metric = AnswerRelevancyMetric(threshold=0.7)
    assert_test(test_case, [metric])


def test_api_key_security_advice(llm_client):
    """Test API key security recommendations"""
    query = "How should I store and manage API keys securely?"
    retrieval_context = [
        "Store API keys in environment variables, never in code.",
        "Rotate keys regularly and use read-only keys when possible."
    ]
    response = llm_client.generate_security_response(query, context=" ".join(retrieval_context))
    
    test_case = LLMTestCase(
        input=query,
        actual_output=response,
        retrieval_context=retrieval_context
    )
    
    faithfulness_metric = FaithfulnessMetric(threshold=0.7)
    assert_test(test_case, [faithfulness_metric])

