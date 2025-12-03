"""
Ollama LLM Client for Security-Focused Responses

This module provides a local LLM client using Ollama for generating security-related
responses without requiring OpenAI API keys.

Key Features:
- Uses local Ollama models (llama3, mistral, etc.)
- No API costs
- Privacy-focused (data stays local)
- Same interface as SecurityLLMClient

Usage:
    client = OllamaSecurityClient(model="llama3")
    response = client.generate_security_response(
        query="How do I prevent SQL injection?"
    )
"""
import os
from typing import Optional, List, Dict, Any
try:
    import ollama
except ImportError:
    raise ImportError("Please install ollama: pip install ollama")


class OllamaSecurityClient:
    """Client for generating security-focused responses using Ollama"""
    
    def __init__(self, model: str = "llama3"):
        """
        Initialize the Ollama client
        
        Args:
            model: Ollama model to use (llama3, mistral, codellama, etc.)
        """
        self.model = model
        # Verify model is available
        try:
            ollama.list()
        except Exception as e:
            raise RuntimeError(f"Ollama server not running. Start it with: ollama serve\n{e}")
    
    def generate_security_response(self, query: str, context: Optional[str] = None) -> str:
        """
        Generate a security-focused response
        
        Args:
            query: User's security question
            context: Optional context for the response
            
        Returns:
            Generated response
        """
        system_prompt = """You are a security expert assistant. Provide accurate, 
        concise answers about API security, authentication, authorization, and 
        common vulnerabilities. Focus on practical, actionable advice."""
        
        if context:
            user_message = f"Context: {context}\n\nQuestion: {query}"
        else:
            user_message = query
        
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            options={
                "temperature": 0.3,
                "num_predict": 800,  # Optimized for faster responses
                "num_ctx": 2048,
            }
        )
        
        return response['message']['content']
    
    def check_sensitive_data_exposure(self, text: str) -> dict:
        """
        Check if text contains potentially sensitive information
        
        Args:
            text: Text to analyze
            
        Returns:
            Analysis results
        """
        system_prompt = """Analyze the following text for potential sensitive data exposure.
        Check for: API keys, passwords, tokens, email addresses, IP addresses, 
        personal information. Return a JSON-like assessment."""
        
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            options={"temperature": 0.1}
        )
        
        return {"analysis": response['message']['content'], "text": text}
    
    def validate_security_advice(self, advice: str, category: str) -> str:
        """
        Validate that security advice follows best practices
        
        Args:
            advice: Security advice to validate
            category: Category (e.g., 'authentication', 'authorization', 'encryption')
            
        Returns:
            Validation result
        """
        system_prompt = f"""You are a security auditor. Review the following 
        {category} advice and verify it follows industry best practices and 
        standards (OWASP, NIST, etc.). Point out any issues or improvements."""
        
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": advice}
            ],
            options={"temperature": 0.2}
        )
        
        return response['message']['content']


# Alias for compatibility
SecurityLLMClient = OllamaSecurityClient
