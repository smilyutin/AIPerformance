"""
Test RAG (Retrieval Augmented Generation) for Security Knowledge Base

This module tests the Retrieval Augmented Generation system's ability to:
- Retrieve relevant security documentation from the knowledge base
- Generate accurate responses based on retrieved context
- Evaluate context relevance and precision
- Maintain faithfulness to source material

RAG Pipeline Tested:
1. Query processing and keyword extraction
2. Context retrieval from security knowledge base
3. Response generation using retrieved context
4. Quality evaluation of retrieval and generation

Security Topics in Knowledge Base:
- SQL injection prevention techniques
- XSS (Cross-Site Scripting) protection
- Rate limiting strategies
- Authentication methods (OAuth, JWT, API keys)
- Principle of least privilege

Metrics used:
- ContextualPrecisionMetric: Measures retrieval precision
- ContextualRecallMetric: Evaluates retrieval completeness
- ContextualRelevancyMetric: Assesses overall retrieval quality
- FaithfulnessMetric: Ensures response fidelity to context
"""
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric,
    FaithfulnessMetric
)
from src.rag_client_ollama import OllamaSecurityRAGClient


class TestSecurityRAG:
    """Test suite for RAG-based security responses"""
    
    @pytest.fixture
    def rag_client(self):
        """Initialize Ollama RAG client"""
        return OllamaSecurityRAGClient()
    
    def test_sql_injection_rag_retrieval(self, rag_client, deepeval_model):
        """Test RAG retrieval and generation for SQL injection"""
        query = "How do I prevent SQL injection attacks?"
        
        result = rag_client.generate_rag_response(query)
        
        test_case = LLMTestCase(
            input=query,
            actual_output=result["response"],
            retrieval_context=result["retrieval_context"]
        )
        
        contextual_relevancy = ContextualRelevancyMetric(threshold=0.25, model=deepeval_model)
        faithfulness = FaithfulnessMetric(threshold=0.7, model=deepeval_model)
        
        assert_test(test_case, [contextual_relevancy, faithfulness])
    
    def test_xss_prevention_context_precision(self, rag_client, deepeval_model):
        """Test context precision for XSS prevention query"""
        query = "What are the best ways to prevent XSS attacks?"
        expected_output = "Prevent XSS by sanitizing input, encoding output, using Content Security Policy headers, and HTTP-only cookies."
        
        result = rag_client.generate_rag_response(query)
        
        test_case = LLMTestCase(
            input=query,
            actual_output=result["response"],
            expected_output=expected_output,
            retrieval_context=result["retrieval_context"]
        )
        
        precision_metric = ContextualPrecisionMetric(threshold=0.6, model=deepeval_model)
        assert_test(test_case, [precision_metric])
    
    def test_rate_limiting_context_recall(self, rag_client, deepeval_model):
        """Test context recall for rate limiting query"""
        query = "Why is rate limiting important for API security?"
        expected_output = "Rate limiting protects APIs from abuse, prevents DDoS attacks, and ensures fair resource usage."
        
        result = rag_client.generate_rag_response(query)
        
        test_case = LLMTestCase(
            input=query,
            actual_output=result["response"],
            expected_output=expected_output,
            retrieval_context=result["retrieval_context"]
        )
        
        recall_metric = ContextualRecallMetric(threshold=0.6, model=deepeval_model)
        assert_test(test_case, [recall_metric])
    
    def test_authentication_methods_rag(self, rag_client, deepeval_model):
        """Test RAG for authentication methods query"""
        query = "What authentication methods should I use for my API?"
        
        result = rag_client.generate_rag_response(query)
        
        test_case = LLMTestCase(
            input=query,
            actual_output=result["response"],
            retrieval_context=result["retrieval_context"]
        )
        
        relevancy = ContextualRelevancyMetric(threshold=0.5, model=deepeval_model)
        faithfulness = FaithfulnessMetric(threshold=0.6, model=deepeval_model)
        
        assert_test(test_case, [relevancy, faithfulness])
    
    def test_least_privilege_with_custom_context(self, rag_client, deepeval_model):
        """Test RAG with custom retrieval context"""
        query = "Explain the principle of least privilege"
        custom_context = [
            "The principle of least privilege (PoLP) requires minimal access rights for users and processes.",
            "Implementation includes RBAC, just-in-time access, and regular permission audits.",
            "Benefits: reduced attack surface, limited breach impact, better compliance."
        ]
        
        result = rag_client.generate_rag_response(query, retrieval_context=custom_context)
        
        test_case = LLMTestCase(
            input=query,
            actual_output=result["response"],
            expected_output="Least privilege means granting minimum necessary permissions to reduce security risks.",
            retrieval_context=custom_context
        )
        
        precision = ContextualPrecisionMetric(threshold=0.6, model=deepeval_model)
        recall = ContextualRecallMetric(threshold=0.6, model=deepeval_model)
        faithfulness = FaithfulnessMetric(threshold=0.7, model=deepeval_model)
        
        assert_test(test_case, [precision, recall, faithfulness])
    """test"""
    def test_context_relevance_evaluation(self, rag_client):
        """Test the context relevance evaluation function"""
        query = "How do I prevent SQL injection?"
        context = "SQL injection is prevented by using parameterized queries and input validation."
        
        relevance_score = rag_client.evaluate_context_relevance(query, context)
        
        # Assert that relevance score is reasonable (> 0.5 for relevant context)
        assert relevance_score > 0.5, f"Expected relevance > 0.5, got {relevance_score}"
    
    def test_irrelevant_context_detection(self, rag_client):
        """Test that irrelevant context is detected"""
        query = "How do I prevent SQL injection?"
        irrelevant_context = "Machine learning models require large datasets for training."
        
        relevance_score = rag_client.evaluate_context_relevance(query, irrelevant_context)
        
        # Assert that relevance score is low for irrelevant context
        assert relevance_score < 0.5, f"Expected relevance < 0.5, got {relevance_score}"
