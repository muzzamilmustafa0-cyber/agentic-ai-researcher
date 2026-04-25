"""Configuration for Agentic AI Researcher."""
import os
from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel

load_dotenv()


def get_llm(provider: str = None) -> BaseChatModel:
    """Get LLM — defaults to Groq (free)."""
    provider = provider or os.getenv("LLM_PROVIDER", "groq")

    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY", ""),
            model_name=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            temperature=0.1,
            max_tokens=2048,
        )
    elif provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY", ""),
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            temperature=0.1,
        )
    elif provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            google_api_key=os.getenv("GEMINI_API_KEY", ""),
            model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
            temperature=0.1,
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")
