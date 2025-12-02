# DeepEval Security Testing Starter

A comprehensive testing framework for evaluating LLM responses on API security topics using DeepEval.

## 🔐 Overview

This project provides a complete testing suite for validating LLM-generated security advice and responses. It focuses on:

- **API Security**: Authentication, authorization, and common vulnerabilities
- **Accuracy Testing**: Ensuring responses are relevant and factually correct
- **Hallucination Detection**: Preventing fabricated or misleading security advice
- **RAG Evaluation**: Testing retrieval-augmented generation quality
- **Prompt Regression**: Comparing prompt versions and preventing regressions

## 📁 Project Structure

```
deepeval-starter/
├── .github/
│   └── workflows/
│       └── deepeval.yml          # CI/CD pipeline for automated testing
├── datasets/
│   ├── golden_dataset.json       # Golden test cases for accuracy
│   └── rag_dataset.json          # RAG test cases with retrieval context
├── src/
│   ├── llm_client.py             # LLM client for security responses
│   ├── prompt_versions.py        # Prompt version management
│   └── rag_client.py             # RAG client with knowledge base
├── tests/
│   ├── test_accuracy.py          # Accuracy and relevancy tests
│   ├── test_hallucination.py     # Hallucination detection tests
│   ├── test_rag.py               # RAG retrieval and generation tests
│   └── test_prompt_regression.py # Prompt version regression tests
├── .env.example                  # Environment variables template
├── requirements.txt              # Python dependencies
├── pytest.ini                    # Pytest configuration
└── README.md                     # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd deepeval-starter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Running Tests

Run all tests:
```bash
pytest
```

Run specific test categories:
```bash
# Accuracy tests
pytest tests/test_accuracy.py

# Hallucination detection
pytest tests/test_hallucination.py

# RAG tests
pytest tests/test_rag.py

# Prompt regression
pytest tests/test_prompt_regression.py
```

Run with markers:
```bash
# Run only security tests
pytest -m security

# Run everything except slow tests
pytest -m "not slow"
```

## 📊 Test Metrics

### Accuracy Tests
- **AnswerRelevancyMetric**: Measures how relevant the response is to the query
- **FaithfulnessMetric**: Ensures responses are grounded in provided context
- **ContextualRelevancyMetric**: Validates context relevance to the query

### Hallucination Tests
- **HallucinationMetric**: Detects fabricated information not supported by context
- **BiasMetric**: Identifies biased or unfair recommendations

### RAG Tests
- **ContextualPrecisionMetric**: Measures precision of retrieved context
- **ContextualRecallMetric**: Evaluates completeness of retrieved context
- **ContextualRelevancyMetric**: Assesses overall retrieval quality

### Prompt Regression Tests
- **GEval**: Custom criteria-based evaluation for comprehensiveness and quality
- **Version Comparison**: Ensures new prompts don't regress on key metrics

## 🔧 Configuration

### Pytest Configuration (`pytest.ini`)

- Test discovery patterns
- Output formatting
- Custom markers for organizing tests
- Logging configuration

### Environment Variables (`.env`)

```bash
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini  # Optional: default model
DEEPEVAL_TELEMETRY_OPT_OUT=true  # Optional
CONFIDENCE_THRESHOLD=0.7  # Optional: default threshold
```

## 📝 Writing Tests

### Basic Test Structure

```python
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

def test_my_security_feature(llm_client):
    query = "How do I secure my API?"
    response = llm_client.generate_security_response(query)
    
    test_case = LLMTestCase(
        input=query,
        actual_output=response
    )
    
    metric = AnswerRelevancyMetric(threshold=0.7)
    assert_test(test_case, [metric])
```

### RAG Test Structure

```python
def test_rag_retrieval(rag_client):
    query = "How do I prevent SQL injection?"
    result = rag_client.generate_rag_response(query)
    
    test_case = LLMTestCase(
        input=query,
        actual_output=result["response"],
        retrieval_context=result["retrieval_context"]
    )
    
    metric = ContextualRelevancyMetric(threshold=0.6)
    assert_test(test_case, [metric])
```

## 🤖 CI/CD Integration

The project includes a GitHub Actions workflow (`.github/workflows/deepeval.yml`) that:

- Runs on push to main/develop branches
- Runs on pull requests
- Executes weekly on Sunday (for regression detection)
- Uploads test results as artifacts

## 🎯 Use Cases

1. **Security Chatbot Validation**: Ensure your security chatbot provides accurate advice
2. **Documentation QA**: Validate generated security documentation
3. **Prompt Engineering**: Test and compare different prompt versions
4. **Compliance**: Verify responses align with security standards (OWASP, NIST)
5. **Regression Testing**: Catch quality degradation in model updates

## 📚 Additional Resources

- [DeepEval Documentation](https://docs.confident-ai.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

MIT License - feel free to use this starter template for your projects.

## 🔒 Security Note

Never commit your `.env` file or expose your API keys. Always use environment variables for sensitive configuration.
