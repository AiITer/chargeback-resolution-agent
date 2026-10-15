from openai import OpenAI

from app.config import settings


def get_openai_client() -> OpenAI:
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is not configured")

    return OpenAI(api_key=settings.openai_api_key)