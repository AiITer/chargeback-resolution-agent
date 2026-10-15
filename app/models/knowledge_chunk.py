from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import VECTOR

from app.models.base import Base


class KnowledgeChunkModel(Base):
    __tablename__ = "knowledge_chunks"

    chunk_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    source: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    section: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    embedding: Mapped[list[float]] = mapped_column(
        VECTOR(384),
        nullable=False,
    )