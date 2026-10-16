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

def create_embeddings(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    if any(not text.strip() for text in texts):
        raise ValueError("Embedding texts cannot contain empty text")

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
    )

    return embeddings.tolist()

def count_embedding_tokens(text: str) -> int:
    model = get_embedding_model()

    token_ids = model.tokenizer(
        text,
        add_special_tokens=True,
        truncation=False,
    )["input_ids"]

    return len(token_ids)