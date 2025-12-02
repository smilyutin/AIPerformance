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
            schema: Optional JSON schema for structured output (Pydantic model)
            
        Returns:
            Generated text or structured object
        """
        # Determine format parameter for Ollama
        format_param = None
        if schema:
            # If schema is provided, use JSON format for structured output
            format_param = "json"
        
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            format=format_param,
            options={
                "temperature": 0.0,  # Deterministic for eval
                "num_predict": 1000,
            }
        )
        
        content = response['message']['content']
        
        # If schema is provided, parse the JSON response into the schema
        if schema:
            import json
            data = None
            try:
                # Parse JSON response
                data = json.loads(content)
                
                # Check if schema is a Pydantic model and convert
                if hasattr(schema, 'model_validate'):
                    # Pydantic v2
                    return schema.model_validate(data)
                elif hasattr(schema, 'parse_obj'):
                    # Pydantic v1
                    return schema.parse_obj(data)
                elif callable(schema):
                    # Regular class constructor
                    return schema(**data)
                else:
                    # Return parsed dict if schema is not a class
                    return data
                    
            except json.JSONDecodeError as e:
                # If JSON parsing fails, return raw content
                # This allows DeepEval to handle the error
                print(f"Warning: JSON decode failed: {e}")
                print(f"Raw content: {content[:200]}")
                return content
            except Exception as e:
                # If schema validation fails, return raw content
                print(f"Warning: Schema validation failed: {e}")
                print(f"Schema type: {type(schema)}")
                if data is not None:
                    print(f"Parsed data: {data}")
                return content
        
        return content
    
    async def a_generate(self, prompt: str, schema: Optional[dict] = None) -> str:
        """
        Async generate (calls synchronous version for now)
        
        Args:
            prompt: The prompt to generate from
            schema: Optional JSON schema for structured output
            
        Returns:
            Generated text or structured object
        """
        # Ollama Python client doesn't have async support yet
        return self.generate(prompt, schema)
    
    def get_model_name(self) -> str:
        """Get the model name"""
        return self.model_name
