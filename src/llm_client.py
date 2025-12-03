"""
LLM Client for Security-Focused Responses

This module provides a specialized LLM client for generating security-related
responses with a focus on API security, authentication, and common vulnerabilities.

Key Features:
- Security-focused system prompts
- Configurable temperature for consistent advice
- Context-aware response generation
- Sensitive data exposure detection
- Security advice validation

The client is optimized for:
- Providing accurate security guidance
- Following industry best practices (OWASP, NIST)
- Maintaining consistent, actionable advice
- Avoiding misleading or insecure recommendations

Usage:
    client = SecurityLLMClient(api_key="your-key", model="gpt-4o-mini")
    response = client.generate_security_response(
        query="How do I prevent SQL injection?",
        context="Use parameterized queries..."
    )

Configuration:
- Default model: gpt-4o-mini
- Temperature: 0.3 (for consistency)
- Max tokens: 500 per response
"""
import os
from typing import Optional, List, Dict, Any, cast
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


class SecurityLLMClient:
    """Client for generating security-focused responses"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize the LLM client
        
        Args:
            api_key: OpenAI API key (defaults to env var)
            model: Model to use for generation
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
    
    def get_security_advice(self, query: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate security advice with optional custom system prompt
        
        Args:
            query: User's security question
            system_prompt: Optional custom system prompt (for prompt version testing)
            
        Returns:
            Generated response
        """
        if system_prompt is None:
            system_prompt = """You are a security expert assistant. Provide accurate, 
            concise answers about API security, authentication, authorization, and 
            common vulnerabilities. Focus on practical, actionable advice."""
        
        messages: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=cast(List[ChatCompletionMessageParam], messages),
            temperature=0.3,
            max_tokens=500
        )
        
        return response.choices[0].message.content or ""
    
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
        
        messages: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_prompt},
        ]
        
        if context:
            messages.append({
                "role": "user", 
                "content": f"Context: {context}\n\nQuestion: {query}"
            })
        else:
            messages.append({"role": "user", "content": query})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=cast(List[ChatCompletionMessageParam], messages),
            temperature=0.3,  # Lower temperature for more consistent security advice
            max_tokens=500
        )
        
        return response.choices[0].message.content or ""
    
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
        
        messages: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=cast(List[ChatCompletionMessageParam], messages),
            temperature=0.1
        )
        
        return {"analysis": response.choices[0].message.content or "", "text": text}
    
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
        
        messages: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": advice}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=cast(List[ChatCompletionMessageParam], messages),
            temperature=0.2
        )
        
        return response.choices[0].message.content or ""
