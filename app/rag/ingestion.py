from pathlib import Path
import re
from sqlalchemy import delete

from app.database import SessionLocal, check_database_connection
from app.integrations.embeddings import create_embeddings
from app.models.knowledge_chunk import KnowledgeChunkModel


def load_markdown_document(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Knowledge document not found: {path}")

    return path.read_text(encoding="utf-8")

def split_markdown_sections(text: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []

    current_heading = "Document"
    current_lines: list[str] = []

    for line in text.splitlines():
        if re.match(r"^#{1,6}\s+", line):
            if current_lines:
                content = "\n".join(current_lines).strip()

                if content:
                    sections.append((current_heading, content))

            current_heading = line.lstrip("#").strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        content = "\n".join(current_lines).strip()

        if content:
            sections.append((current_heading, content))

    return sections

def build_embedding_texts(
    sections: list[tuple[str, str]],
) -> list[str]:
    return [
        f"{heading}\n\n{content}"
        for heading, content in sections
    ]

def ingest_markdown_document(path: Path, source: str) -> int:
    check_database_connection()
    
    text = load_markdown_document(path)
    sections = split_markdown_sections(text)
    embedding_texts = build_embedding_texts(sections)
    embeddings = create_embeddings(embedding_texts)

    if len(sections) != len(embeddings):
        raise ValueError(
            "Section and embedding counts do not match"
        )

    with SessionLocal() as session:
        session.execute(
            delete(KnowledgeChunkModel).where(
                KnowledgeChunkModel.source == source
            )
        )

        chunks = [
            KnowledgeChunkModel(
                source=source,
                section=heading,
                content=content,
                embedding=embedding,
            )
            for (heading, content), embedding in zip(sections, embeddings)
        ]

        session.add_all(chunks)
        session.commit()

    return len(chunks)