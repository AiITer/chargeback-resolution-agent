from openai import OpenAI

from app.config import settings


def get_openai_client() -> OpenAI:
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is not configured")

    return OpenAI(api_key=settings.openai_api_key)

def create_embedding(text: str) -> list[float]:
    if not text.strip():
        raise ValueError("Embedding text cannot be empty")

    client = get_openai_client()

    response = client.embeddings.create(
        model=settings.openai_embedding_model,
        input=text,
        encoding_format="float",
        dimensions=settings.openai_embedding_dimensions,
    )

    return response.data[0].embedding