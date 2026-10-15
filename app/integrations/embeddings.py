from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.config import settings


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(settings.embedding_model)


def create_embedding(text: str) -> list[float]:
    if not text.strip():
        raise ValueError("Embedding text cannot be empty")

    model = get_embedding_model()

    embedding = model.encode(
        text,
        normalize_embeddings=True,
    )

    return embedding.tolist()