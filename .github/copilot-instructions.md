# Copilot / AI-Agent Instructions for AIPerformance  

## 🧩 Project Overview — Big Picture  

-- This repo is a **LLM evaluation & security-testing harness** built on top of **DeepEval** using OpenAI for inference.  
-- Purpose: validate AI-generated responses (accuracy, hallucination, RAG retrieval, prompt regression) especially in security / API guidance contexts.  
- Core workflow:  
  1. AI generates output (via `src/llm_client.py` or `src/rag_client.py`)  
  2. Tests (under `tests/`) convert output into a `LLMTestCase`, run metrics (relevancy, faithfulness, hallucination etc.), and assert outcomes.  
  3. Results are saved under `deepeval_results/`.  
  4. CI pipeline (`.github/workflows/deepeval.yml`) runs this automatically on pushes, PRs, and weekly regression cycles.

## 🛠️ Key Project Structure & Conventions  
/src
llm_client.py       # Interface to LLM (OpenAI) → generates responses
rag_client.py       # Interface for RAG-based generation + retrieval context
prompt_versions.py  # Manage different prompt versions
/tests
test_accuracy.py          # Relevancy / correctness tests
test_hallucination.py     # Hallucination / fact-fabrication checks
test_rag.py               # RAG retrieval + generation tests
test_prompt_regression.py # Checks that new prompt versions do not regress
/datasets
golden_dataset.json       # “Ground truth” inputs + expected outputs for accuracy tests
rag_dataset.json          # Inputs + retrieval context for RAG tests
/deepeval_results            # Test output artifacts
.github/workflows/deepeval.yml # CI pipeline
.env.example                 # Example env config (API key, model, thresholds)

### 🧵 Naming / Test Patterns  

- Use `LLMTestCase` to wrap prompt / response / (optionally) `retrieval_context` for RAG.  
- Metrics from DeepEval (e.g., `AnswerRelevancyMetric`, `FaithfulnessMetric`, `HallucinationMetric`, `ContextualPrecisionMetric`, `ContextualRecallMetric`) drive pass/fail logic.  
- Prompt regression tests compare output of `prompt_versions.py` variants against golden data or expected behavior.  
- Do **not** rely on implicit output — always wrap with test cases + metric assertions.  

### ✅ Test Design Guidance (Modern Python / pytest)

- **Prefer function-based tests:** Do not introduce `unittest`-style test classes. Use plain functions with `pytest` fixtures for setup and teardown. Function-based tests are easier to parametrize and read.
- **Use Page Object Model (POM) for helpers:** Encapsulate interaction logic (API calls, prompt builders, request sequences) in small, focused helper modules under `tests/pages/` or `tests/helpers/`. These helpers (page objects) should expose clear actions and queries, keeping tests declarative.
- **Keep logic out of tests:** Tests should orchestrate scenarios and assert outcomes. Put complex message construction, data transformation, and client utilities in `src/` or helper modules.
- **Use fixtures for shared resources:** Provide `pytest.fixture` for clients, contexts, and test data. Prefer `scope='function'` or `scope='module'` depending on isolation needs. Avoid global mutable state.
- **Example layout:**
  - `tests/test_feature_x.py` — function-based tests
  - `tests/pages/` — POM-style helpers (e.g., `prompt_builder.py`, `api_client.py`)
  - `tests/fixtures.py` — shared fixtures and test data

**Rationale:** Function-based pytest tests combined with POM-style helpers reduce brittle inheritance, improve readability, make parametrization straightforward, and keep the test-suite maintainable as prompt versions evolve.

## 📦 Developer Workflow  

````instructions
# Copilot / AI-Agent Instructions for AIPerformance  

## 🧩 Project Overview — Big Picture  

- This repo is a **LLM evaluation & security-testing harness** built on top of **DeepEval** using OpenAI for inference.  
- Purpose: validate AI-generated responses (accuracy, hallucination, RAG retrieval, prompt regression) especially in security / API guidance contexts.  
- Core workflow:  
  1. AI generates output (via `src/llm_client.py` or `src/rag_client.py`)  
  2. Tests (under `tests/`) convert output into a `LLMTestCase`, run metrics (relevancy, faithfulness, hallucination etc.), and assert outcomes.  
  3. Results are saved under `deepeval_results/`.  
  4. CI pipeline (`.github/workflows/deepeval.yml`) runs this automatically on pushes, PRs, and weekly regression cycles.

## 🛠️ Key Project Structure & Conventions  
/src
llm_client.py       # Interface to LLM (OpenAI) → generates responses
rag_client.py       # Interface for RAG-based generation + retrieval context
prompt_versions.py  # Manage different prompt versions
/tests
test_accuracy.py          # Relevancy / correctness tests
test_hallucination.py     # Hallucination / fact-fabrication checks
test_rag.py               # RAG retrieval + generation tests
test_prompt_regression.py # Checks that new prompt versions do not regress
/datasets
golden_dataset.json       # “Ground truth” inputs + expected outputs for accuracy tests
rag_dataset.json          # Inputs + retrieval context for RAG tests
/deepeval_results            # Test output artifacts
.github/workflows/deepeval.yml # CI pipeline
.env.example                 # Example env config (API key, model, thresholds)

### 🧵 Naming / Test Patterns  

- Use `LLMTestCase` to wrap prompt / response / (optionally) `retrieval_context` for RAG.  
- Metrics from DeepEval (e.g., `AnswerRelevancyMetric`, `FaithfulnessMetric`, `HallucinationMetric`, `ContextualPrecisionMetric`, `ContextualRecallMetric`) drive pass/fail logic.  
- Prompt regression tests compare output of `prompt_versions.py` variants against golden data or expected behavior.  
- Do **not** rely on implicit output — always wrap with test cases + metric assertions.  

## 📦 Developer Workflow  

### ✅ Local setup  

```bash
git clone <repo>
cd AIPerformance
python3 -m venv venv  # or your preferred env
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env to set necessary variables (e.g. OPENAI_API_KEY)
````