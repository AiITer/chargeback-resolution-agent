from dataclasses import dataclass

from sqlalchemy import select

from app.database import SessionLocal
from app.integrations.embeddings import create_query_embedding
from app.models.knowledge_chunk import KnowledgeChunkModel


@dataclass(frozen=True)
class KnowledgeSearchResult:
    chunk_id: int
    source: str
    section: str | None
    content: str
    cosine_distance: float


def search_knowledge(
    query: str,
    top_k: int,
) -> list[KnowledgeSearchResult]:
    if top_k <= 0:
        raise ValueError("top_k must be greater than 0")

    query_embedding = create_query_embedding(query)

    distance = KnowledgeChunkModel.embedding.cosine_distance(
        query_embedding
    ).label("cosine_distance")

    statement = (
        select(KnowledgeChunkModel, distance)
        .order_by(distance)
        .limit(top_k)
    )

    with SessionLocal() as session:
        rows = session.execute(statement).all()

    return [
        KnowledgeSearchResult(
            chunk_id=chunk.chunk_id,
            source=chunk.source,
            section=chunk.section,
            content=chunk.content,
            cosine_distance=float(distance_value),
        )
        for chunk, distance_value in rows
    ]

def format_knowledge_results(
    results: list[KnowledgeSearchResult],
) -> str:
    return "\n\n".join(
        (
            f"Source: {result.source}\n"
            f"Section: {result.section or 'Unknown'}\n"
            f"Content:\n{result.content}"
        )
        for result in results
    )

