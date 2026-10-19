from langchain_ollama import ChatOllama

from app.config import settings


def get_chat_model() -> ChatOllama:
    if settings.llm_provider != "ollama":
        raise ValueError(
            f"Unsupported LLM provider: {settings.llm_provider}"
        )

    return ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
    )