"""
RAG (Retrieval Augmented Generation) client for security documentation
"""
import os
from typing import List, Optional
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


class SecurityRAGClient:
    """RAG client for security knowledge base"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize the RAG client
        
        Args:
            api_key: OpenAI API key
            model: Model to use for generation
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
        
        # Simulated knowledge base (in production, use vector DB)
        self.knowledge_base = [
            {
                "topic": "SQL Injection",
                "content": "SQL injection is a code injection technique that exploits vulnerabilities in database queries. Prevention: use parameterized queries, input validation, and ORM frameworks."
            },
            {
                "topic": "XSS Prevention",
                "content": "Cross-Site Scripting (XSS) attacks inject malicious scripts. Mitigation: sanitize input, encode output, use Content Security Policy headers, and HTTP-only cookies."
            },
            {
                "topic": "API Rate Limiting",
                "content": "Rate limiting controls API request frequency to prevent abuse. Strategies: fixed window, sliding window, token bucket. Protects against DDoS and ensures fair usage."
            },
            {
                "topic": "Authentication Best Practices",
                "content": "Use OAuth 2.0 for third-party access, JWT for stateless auth, secure password hashing (bcrypt, Argon2), MFA, and proper session management."
            },
            {
                "topic": "Least Privilege",
                "content": "Grant minimum necessary permissions. Implement RBAC, just-in-time access, regular audits. Reduces attack surface and breach impact."
            },
        ]
    
    def retrieve_context(self, query: str, top_k: int = 3) -> List[str]:
        """
        Retrieve relevant context from knowledge base
        
        Args:
            query: User query
            top_k: Number of top results to return
            
        Returns:
            List of relevant context strings
        """
        # Simple keyword matching (in production, use vector embeddings)
        query_lower = query.lower()
        
        scored_docs = []
        for doc in self.knowledge_base:
            score = 0
            # Simple scoring based on keyword presence
            if any(word in doc["content"].lower() for word in query_lower.split()):
                score += 1
            if any(word in doc["topic"].lower() for word in query_lower.split()):
                score += 2
            
            if score > 0:
                scored_docs.append((score, doc["content"]))
        
        # Sort by score and return top_k
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        return [doc[1] for doc in scored_docs[:top_k]]
    
    def generate_rag_response(self, query: str, retrieval_context: Optional[List[str]] = None) -> dict:
        """
        Generate response using retrieved context
        
        Args:
            query: User query
            retrieval_context: Optional pre-retrieved context
            
        Returns:
            Dict with response and context used
        """
        # Retrieve context if not provided
        if retrieval_context is None:
            retrieval_context = self.retrieve_context(query)
        
        # Build context string
        context_str = "\n\n".join([f"Context {i+1}: {ctx}" for i, ctx in enumerate(retrieval_context)])
        
        # Generate response with context
        system_prompt = """You are a security expert. Use the provided context to answer 
        the question accurately. If the context doesn't contain enough information, 
        acknowledge the limitations while providing the best answer possible."""
        
        user_message = f"""Context information:
{context_str}

Question: {query}

Provide a clear, accurate answer based on the context above."""
        
        messages: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3,
            max_tokens=500
        )
        
        return {
            "query": query,
            "response": response.choices[0].message.content or "",
            "retrieval_context": retrieval_context
        }
    
    def evaluate_context_relevance(self, query: str, context: str) -> float:
        """
        Evaluate how relevant a context is to a query
        
        Args:
            query: User query
            context: Context to evaluate
            
        Returns:
            Relevance score (0-1)
        """
        system_prompt = """Rate how relevant the given context is to answering the query.
        Return only a number between 0 and 1, where 0 is completely irrelevant and 1 is highly relevant."""
        
        messages: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Query: {query}\n\nContext: {context}\n\nRelevance score:"}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,
            max_tokens=10
        )
        
        try:
            content = response.choices[0].message.content
            if content is None:
                return 0.5
            score = float(content.strip())
            return max(0.0, min(1.0, score))  # Clamp between 0 and 1
        except (ValueError, AttributeError):
            return 0.5  # Default if parsing fails
