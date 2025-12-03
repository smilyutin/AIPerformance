# DeepEval Security Testing Starter

A comprehensive testing framework for evaluating LLM responses on API security topics using DeepEval and OpenAI.

## 🔐 Overview

This project provides a complete testing suite for validating LLM-generated security advice and responses. It focuses on:

- **API Security**: Authentication, authorization, and common vulnerabilities
- **Accuracy Testing**: Ensuring responses are relevant and factually correct
- **Hallucination Detection**: Preventing fabricated or misleading security advice
- **RAG Evaluation**: Testing retrieval-augmented generation quality
- **Prompt Regression**: Comparing prompt versions and preventing regressions
- **Cost-Free Testing**: Uses Ollama for local LLM inference (zero API costs)

## 📁 Project Structure

```
startDeepEval/
├── .github/
│   └── workflows/
│       └── deepeval.yml          # CI/CD pipeline
├── datasets/
│   ├── golden_dataset.json       # Golden test cases for accuracy
│   └── rag_dataset.json          # RAG test cases with retrieval context
├── src/
│   ├── __init__.py
│   ├── llm_client.py             # OpenAI client for security responses
│   ├── rag_client.py             # OpenAI RAG client with knowledge base
│   └── prompt_versions.py        # Prompt version management
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures
│   ├── test_accuracy.py          # Accuracy and relevancy tests
│   ├── test_hallucination.py     # Hallucination detection tests
│   ├── test_rag.py               # RAG retrieval and generation tests
│   └── test_prompt_regression.py # Prompt version regression tests
├── deepeval_results/             # Test results output directory
├── .env.example                  # Environment variables template
├── requirements.txt              # Python dependencies
├── pyproject.toml                # Project configuration
├── pytest.ini                    # Pytest configuration
└── README.md                     # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- OpenAI API key

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd startDeepEval
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key:
   # OPENAI_API_KEY=your_api_key_here
   ```

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

### Troubleshooting

**Error: "Ollama server not running"**
- Start Ollama: `ollama serve` in a separate terminal
- Verify it's running: `curl http://localhost:11434/api/tags`

**Error: "Model not found"**
- Pull the model: `ollama pull llama3`
- List available models: `ollama list`

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
# Required: OpenAI API Key
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini

# DeepEval configuration
DEEPEVAL_TELEMETRY_OPT_OUT=true  # Optional
CONFIDENCE_THRESHOLD=0.7         # Optional: default threshold
```

**Note**: With Ollama, you don't need an OpenAI API key! The tests run entirely locally with zero API costs.

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

- Automatically installs and configures Ollama
- Pulls the llama3 model
- Runs on push to main/develop branches
- Runs on pull requests
- Executes weekly on Sunday (for regression detection)
- Requires OpenAI API key configured as GitHub secret

### Setting Up GitHub Actions

Add your OpenAI API key as a repository secret:

1. Go to your repository settings
2. Navigate to Secrets and variables > Actions
3. Add a new repository secret:
   - Name: `OPENAI_API_KEY`
   - Value: Your OpenAI API key

Then push to trigger automated testing:

```bash
git push origin dev
```

## 🎯 Use Cases

1. **Security Chatbot Validation**: Ensure your security chatbot provides accurate advice
2. **Documentation QA**: Validate generated security documentation
3. **Prompt Engineering**: Test and compare different prompt versions
4. **Compliance**: Verify responses align with security standards (OWASP, NIST)
5. **Regression Testing**: Catch quality degradation in model updates
6. **Cost-Free Development**: Develop and test LLM applications without API costs
7. **Privacy-First Testing**: Keep sensitive security data local with Ollama

## 🌟 Why Ollama?

- **Zero Cost**: No API fees, unlimited testing
- **Privacy**: All data stays on your machine
- **Speed**: Local inference with GPU support
- **Offline**: Works without internet connection
- **Flexible**: Support for multiple models (llama3, mistral, codellama, etc.)

## 📚 Additional Resources

- [DeepEval Documentation](https://docs.confident-ai.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

MIT License - feel free to use this starter template for your projects.
