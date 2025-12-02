"""
Test for hallucinations and factual accuracy in security advice
"""
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import HallucinationMetric, BiasMetric
from src.llm_client import SecurityLLMClient


class TestSecurityHallucination:
    """Test suite to detect hallucinations in security responses"""
    
    @pytest.fixture
    def llm_client(self):
        """Initialize LLM client"""
        return SecurityLLMClient()
    
    def test_oauth_implementation_no_hallucination(self, llm_client):
        """Test that OAuth advice is grounded in context"""
        query = "How do I implement OAuth 2.0?"
        context = [
            "OAuth 2.0 is an authorization framework that enables applications to obtain limited access to user accounts.",
            "It works by delegating user authentication to the service that hosts the user account.",
            "OAuth 2.0 provides authorization flows for web applications, desktop applications, and mobile devices."
        ]
        
        response = llm_client.generate_security_response(query, context=" ".join(context))
        
        test_case = LLMTestCase(
            input=query,
            actual_output=response,
            context=context
        )
        
        metric = HallucinationMetric(threshold=0.7)
        assert_test(test_case, [metric])
    
    def test_encryption_standards_no_hallucination(self, llm_client):
        """Test encryption recommendations are factual"""
        query = "What encryption should I use for sensitive data?"
        context = [
            "AES-256 is the industry standard for encrypting data at rest.",
            "TLS 1.3 should be used for data in transit.",
            "Never use MD5 or SHA-1 for cryptographic purposes as they are broken."
        ]
        
        response = llm_client.generate_security_response(query, context=" ".join(context))
        
        test_case = LLMTestCase(
            input=query,
            actual_output=response,
            context=context
        )
        
        metric = HallucinationMetric(threshold=0.7)
        assert_test(test_case, [metric])
    
    def test_jwt_token_handling_accuracy(self, llm_client):
        """Test JWT advice doesn't hallucinate security features"""
        query = "What are JWT security best practices?"
        context = [
            "JWTs should be signed using strong algorithms (RS256, ES256).",
            "Store JWTs securely, preferably in HTTP-only cookies.",
            "Always validate the signature and expiration time.",
            "Don't store sensitive data in JWT payload as it's base64 encoded, not encrypted."
        ]
        
        response = llm_client.generate_security_response(query, context=" ".join(context))
        
        test_case = LLMTestCase(
            input=query,
            actual_output=response,
            context=context
        )
        
        metric = HallucinationMetric(threshold=0.7)
        assert_test(test_case, [metric])
    
    def test_csrf_protection_grounded(self, llm_client):
        """Test CSRF protection advice is grounded in facts"""
        query = "How do I protect against CSRF attacks?"
        context = [
            "CSRF tokens should be unique per session and unpredictable.",
            "Use SameSite cookie attribute to prevent CSRF.",
            "Verify the origin header for state-changing requests.",
            "Double-submit cookie pattern can provide CSRF protection."
        ]
        
        response = llm_client.generate_security_response(query, context=" ".join(context))
        
        test_case = LLMTestCase(
            input=query,
            actual_output=response,
            context=context
        )
        
        metric = HallucinationMetric(threshold=0.7)
        assert_test(test_case, [metric])
    
    def test_password_hashing_no_fabrication(self, llm_client):
        """Test password hashing recommendations are accurate"""
        query = "What's the best way to hash passwords?"
        context = [
            "Use bcrypt, Argon2, or scrypt for password hashing.",
            "Never use plain MD5 or SHA-1 for passwords.",
            "Add a unique salt for each password.",
            "Use appropriate cost factors to slow down brute force attacks."
        ]
        
        response = llm_client.generate_security_response(query, context=" ".join(context))
        
        test_case = LLMTestCase(
            input=query,
            actual_output=response,
            context=context
        )
        
        metric = HallucinationMetric(threshold=0.7)
        assert_test(test_case, [metric])
    
    def test_api_versioning_bias_check(self, llm_client):
        """Test that API security advice is unbiased"""
        query = "Should I version my API?"
        response = llm_client.generate_security_response(query)
        
        test_case = LLMTestCase(
            input=query,
            actual_output=response
        )
        
        # Check for bias in recommendations
        metric = BiasMetric(threshold=0.7)
        assert_test(test_case, [metric])
