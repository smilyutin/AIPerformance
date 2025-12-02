"""
Ollama Model Wrapper for DeepEval

This module provides a custom DeepEval model that uses Ollama instead of OpenAI.
DeepEval's metrics (like AnswerRelevancyMetric, HallucinationMetric, etc.) can use
this model to avoid OpenAI API costs.

Usage:
    from deepeval.models.base_model import DeepEvalBaseLLM
    from src.ollama_deepeval_model import OllamaModel
    
    # Set as default for all metrics
    model = OllamaModel(model_name="llama3")
    
    # Use in metrics
    metric = AnswerRelevancyMetric(threshold=0.7, model=model)
"""
from typing import Optional
import ollama
from deepeval.models.base_model import DeepEvalBaseLLM


class OllamaModel(DeepEvalBaseLLM):
    """DeepEval model wrapper for Ollama"""
    
    def __init__(self, model_name: str = "llama3"):
        """
        Initialize Ollama model for DeepEval
        
        Args:
            model_name: Ollama model to use (llama3, mistral, etc.)
        """
        self.model_name = model_name
        
        # Verify Ollama is running and model is available
        try:
            ollama.list()
        except Exception as e:
            raise RuntimeError(
                f"Ollama server not running. Start it with: ollama serve\n{e}"
            )
    
    def load_model(self):
        """Load the model (no-op for Ollama as it's already running)"""
        return self
    
    def generate(self, prompt: str, schema: Optional[dict] = None) -> str:
        """
        Generate response using Ollama
        
        Args:
            prompt: The prompt to generate from
            schema: Optional JSON schema for structured output
            
        Returns:
            Generated text
        """
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            options={
                "temperature": 0.0,  # Deterministic for eval
                "num_predict": 1000,
            }
        )
        
        return response['message']['content']
    
    async def a_generate(self, prompt: str, schema: Optional[dict] = None) -> str:
        """
        Async generate (calls synchronous version for now)
        
        Args:
            prompt: The prompt to generate from
            schema: Optional JSON schema for structured output
            
        Returns:
            Generated text
        """
        # Ollama Python client doesn't have async support yet
        return self.generate(prompt, schema)
    
    def get_model_name(self) -> str:
        """Get the model name"""
        return self.model_name
