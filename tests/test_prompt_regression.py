"""
Test Prompt Version Regression and Consistency

This module ensures that prompt updates don't degrade performance on critical
security topics. It compares different prompt versions to validate improvements
and prevent regressions.

Prompt Versions Tested:
- v1: Basic security assistant
- v2: Enhanced with specific focus areas
- v3: Current production version (comprehensive guidance)
- v4: Experimental version with detailed examples

Testing Strategy:
1. Baseline performance measurement (v3)
2. Version comparison (v3 vs v4)
3. Consistency checks across versions
4. Detailed advice evaluation
5. Code example quality assessment
6. Critical topic regression testing

Key Security Topics:
- Password storage and hashing
- SQL injection prevention
- JWT authentication implementation
- XSS attack mitigation
- API key management
- REST API security

Metrics used:
- AnswerRelevancyMetric: Validates response relevance
- GEval: Custom criteria-based evaluation for comprehensiveness and code quality
"""
import pytest
from typing import List
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, GEval
from deepeval.test_case import LLMTestCaseParams
from openai.types.chat import ChatCompletionMessageParam
from src.prompt_versions import PromptVersionManager
from src.llm_client import SecurityLLMClient


class TestPromptRegression:
    """Test suite for prompt version regression testing"""
    
    @pytest.fixture
    def llm_client(self):
        """Initialize Ollama LLM client"""
        return SecurityLLMClientOllama()
    
    def generate_response_with_version(self, client, query: str, version: str) -> str:
        """Generate response using specific prompt version"""
        prompt = PromptVersionManager.get_prompt(version)
        
        messages: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": query}
        ]
        
        response = client.client.chat.completions.create(
            model=client.model,
            messages=messages,
            temperature=0.3,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    def test_v3_baseline_performance(self, llm_client):
        """Test baseline performance of v3 (production) prompt"""
        query = "What are the security risks of storing passwords in plain text?"
        response = self.generate_response_with_version(llm_client, query, "v3")
        
        test_case = LLMTestCase(
            input=query,
            actual_output=response
        )
        
        relevancy = AnswerRelevancyMetric(threshold=0.7)
        assert_test(test_case, [relevancy])
    
    def test_v4_vs_v3_comparison(self, llm_client):
        """Compare v4 experimental prompt against v3 baseline"""
        query = "How should I implement JWT authentication?"
        
        v3_response = self.generate_response_with_version(llm_client, query, "v3")
        v4_response = self.generate_response_with_version(llm_client, query, "v4")
        
        # Test v3 (baseline)
        test_case_v3 = LLMTestCase(
            input=query,
            actual_output=v3_response
        )
        
        # Test v4 (experimental)
        test_case_v4 = LLMTestCase(
            input=query,
            actual_output=v4_response
        )
        
        relevancy_metric = AnswerRelevancyMetric(threshold=0.7)
        
        # Both versions should meet threshold
        assert_test(test_case_v3, [relevancy_metric])
        assert_test(test_case_v4, [relevancy_metric])
    
    def test_prompt_consistency_across_versions(self, llm_client):
        """Test that different versions maintain consistency on core topics"""
        query = "What is SQL injection?"
        
        responses = {}
        for version in ["v2", "v3", "v4"]:
            responses[version] = self.generate_response_with_version(llm_client, query, version)
        
        # All versions should provide relevant answers
        # Lower threshold (0.5) because security prompts often include prevention tips
        # along with definitions, which is actually desirable for security topics
        for version, response in responses.items():
            test_case = LLMTestCase(
                input=query,
                actual_output=response
            )
            
            metric = AnswerRelevancyMetric(threshold=0.5)
            assert_test(test_case, [metric])
    
    def test_v3_detailed_security_advice(self, llm_client):
        """Test v3 provides detailed security advice"""
        query = "How do I secure my REST API?"
        response = self.generate_response_with_version(llm_client, query, "v3")
        
        test_case = LLMTestCase(
            input=query,
            actual_output=response
        )
        
        # Use G-Eval to assess comprehensiveness
        comprehensiveness_metric = GEval(
            name="Comprehensiveness",
            criteria="Evaluate how comprehensive and detailed the security advice is. Consider coverage of authentication, authorization, encryption, input validation, and monitoring.",
            evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
            threshold=0.7
        )
        
        assert_test(test_case, [comprehensiveness_metric])
    
    def test_v4_code_examples_quality(self, llm_client):
        """Test v4 prompt provides quality code examples when appropriate"""
        query = "Show me how to implement rate limiting in Python"
        response = self.generate_response_with_version(llm_client, query, "v4")
        
        test_case = LLMTestCase(
            input=query,
            actual_output=response
        )
        
        # G-Eval for code quality (lower threshold due to max_tokens limit)
        code_quality_metric = GEval(
            name="Code Quality",
            criteria="Evaluate if the response includes practical, secure code examples when requested. Code should follow best practices and be production-ready.",
            evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
            threshold=0.55
        )
        
        assert_test(test_case, [code_quality_metric])
    
    def test_no_regression_on_critical_topics(self, llm_client):
        """Ensure no regression on critical security topics"""
        critical_queries = [
            "How do I prevent XSS attacks?",
            "What's the best way to hash passwords?",
            "How should I manage API keys?"
        ]
        
        for query in critical_queries:
            v3_response = self.generate_response_with_version(llm_client, query, "v3")
            
            test_case = LLMTestCase(
                input=query,
                actual_output=v3_response
            )
            
            # High threshold for critical security topics
            relevancy = AnswerRelevancyMetric(threshold=0.75)
            assert_test(test_case, [relevancy])
    
    def test_prompt_version_manager(self):
        """Test prompt version manager functionality"""
        # Test default version
        default_prompt = PromptVersionManager.get_prompt()
        assert default_prompt == PromptVersionManager.VERSIONS["v3"]
        
        # Test specific version retrieval
        v2_prompt = PromptVersionManager.get_prompt("v2")
        assert "OWASP Top 10" in v2_prompt
        
        # Test version listing
        versions = PromptVersionManager.list_versions()
        assert len(versions) >= 4
        assert "v3" in versions
