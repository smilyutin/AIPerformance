"""
Prompt Version Management for Security-Focused LLM Responses

This module manages different versions of security expert system prompts,
enabling A/B testing, regression testing, and continuous improvement.

Version History:
- v1: Basic security assistant (minimal guidance)
- v2: Enhanced with specific focus areas (OWASP Top 10)
- v3: Current production version (comprehensive with best practices)
- v4: Experimental version (detailed with code examples)

Each version represents an evolution in:
- Scope of security topics covered
- Detail level in responses
- Inclusion of standards and examples
- Specificity of guidance

The PromptVersionManager class provides:
- Version retrieval by name
- Default version management
- Version listing for testing
- Centralized prompt configuration

Usage:
    from src.prompt_versions import PromptVersionManager
    
    # Get current production prompt
    prompt = PromptVersionManager.get_prompt()  # Returns v3
    
    # Get specific version for testing
    prompt_v4 = PromptVersionManager.get_prompt("v4")
    
    # List all available versions
    versions = PromptVersionManager.list_versions()

This enables systematic testing of prompt improvements and prevents regressions.
"""

# Version 1: Basic security assistant
SECURITY_PROMPT_V1 = """You are a security assistant. Answer questions about API security."""

# Version 2: Enhanced with specific focus areas
SECURITY_PROMPT_V2 = """You are a security expert assistant. Provide accurate answers about:
- API security and authentication
- Common vulnerabilities (OWASP Top 10)
- Security best practices
Keep responses concise and actionable."""

# Version 3: Current production version with comprehensive guidance
SECURITY_PROMPT_V3 = """You are a security expert assistant specializing in API security. 
Provide accurate, concise answers about:
- API security, authentication, and authorization
- Common vulnerabilities (SQL injection, XSS, CSRF, etc.)
- Security best practices and industry standards (OWASP, NIST)
- Incident response and threat mitigation

Guidelines:
- Focus on practical, actionable advice
- Cite security standards when relevant
- Warn about common pitfalls
- Prioritize defense-in-depth approaches
- Never suggest insecure practices"""

# Version 4: Experimental - more detailed with examples
SECURITY_PROMPT_V4 = """You are a senior security architect with expertise in API security.
Provide comprehensive guidance on:
- Authentication & Authorization (OAuth 2.0, JWT, API keys, RBAC)
- Input validation and sanitization
- Encryption (TLS, data at rest, key management)
- Common vulnerabilities and mitigations (OWASP Top 10)
- Security monitoring and incident response
- Compliance (GDPR, PCI-DSS, SOC 2)

Response format:
1. Direct answer to the question
2. Best practices and recommendations
3. Common pitfalls to avoid
4. Related security considerations

Always prioritize security over convenience. Provide code examples when helpful."""


class PromptVersionManager:
    """Manage different versions of security prompts"""
    
    VERSIONS = {
        "v1": SECURITY_PROMPT_V1,
        "v2": SECURITY_PROMPT_V2,
        "v3": SECURITY_PROMPT_V3,
        "v4": SECURITY_PROMPT_V4,
    }
    
    DEFAULT_VERSION = "v3"
    
    @classmethod
    def get_prompt(cls, version: str = None) -> str: # type: ignore
        """Get prompt by version, defaults to current production version"""
        version = version or cls.DEFAULT_VERSION
        return cls.VERSIONS.get(version, cls.VERSIONS[cls.DEFAULT_VERSION])
    
    @classmethod
    def list_versions(cls) -> list:
        """List all available prompt versions"""
        return list(cls.VERSIONS.keys())
