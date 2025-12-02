"""
Ollama RAG Client for Security Documentation

Local RAG client using Ollama instead of OpenAI API.
"""
from typing import List, Optional
try:
    import ollama
except ImportError:
    raise ImportError("Please install ollama: pip install ollama")


class OllamaSecurityRAGClient:
    """RAG client for security knowledge base using Ollama"""
    
    def __init__(self, model: str = "llama3"):
        """
        Initialize the Ollama RAG client
        
        Args:
            model: Ollama model to use
        """
        self.model = model
        
        # Knowledge base (same as original)
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
        """Retrieve relevant context (same logic as original)"""
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        scored_docs = []
        for doc in self.knowledge_base:
            score = 0
            topic_lower = doc["topic"].lower()
            content_lower = doc["content"].lower()
            
            topic_words = set(topic_lower.split())
            topic_overlap = len(query_words & topic_words)
            score += topic_overlap * 3
            
            for word in query_words:
                if len(word) > 3:
                    if word in content_lower:
                        score += 1
                    if word in topic_lower:
                        score += 2
            
            keyword_mappings = {
                "authentication": ["authentication", "auth", "oauth", "jwt"],
                "sql": ["sql", "injection", "database"],
                "xss": ["xss", "cross-site", "scripting"],
                "rate": ["rate", "limiting", "ddos"],
                "privilege": ["privilege", "rbac", "access"],
            }
            
            for key, keywords in keyword_mappings.items():
                if key in query_lower:
                    for kw in keywords:
                        if kw in topic_lower or kw in content_lower:
                            score += 2
            
            if score > 0:
                scored_docs.append((score, doc["content"]))
        
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        return [doc[1] for doc in scored_docs[:top_k]]
    
    def generate_rag_response(self, query: str, retrieval_context: Optional[List[str]] = None) -> dict:
        """Generate response using Ollama with retrieved context"""
        if retrieval_context is None:
            retrieval_context = self.retrieve_context(query)
        
        context_str = "\n\n".join([f"Context {i+1}: {ctx}" for i, ctx in enumerate(retrieval_context)])
        
        system_prompt = """You are a security expert. Use the provided context to answer 
        the question accurately. If the context doesn't contain enough information, 
        acknowledge the limitations while providing the best answer possible."""
        
        user_message = f"""Context information:
{context_str}

Question: {query}

Provide a clear, accurate answer based on the context above."""
        
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            options={
                "temperature": 0.3,
                "num_predict": 500
            }
        )
        
        return {
            "query": query,
            "response": response['message']['content'],
            "retrieval_context": retrieval_context
        }
    
    def evaluate_context_relevance(self, query: str, context: str) -> float:
        """Evaluate context relevance using Ollama"""
        system_prompt = """Rate how relevant the given context is to answering the query.
        Return only a number between 0 and 1, where 0 is completely irrelevant and 1 is highly relevant."""
        
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Query: {query}\n\nContext: {context}\n\nRelevance score:"}
            ],
            options={"temperature": 0.1}
        )
        
        try:
            score = float(response['message']['content'].strip())
            return max(0.0, min(1.0, score))
        except ValueError:
            return 0.5


# Alias for compatibility
SecurityRAGClient = OllamaSecurityRAGClient
