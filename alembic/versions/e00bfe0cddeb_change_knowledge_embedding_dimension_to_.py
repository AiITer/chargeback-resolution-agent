"""Change knowledge embedding dimension to 384

Revision ID: e00bfe0cddeb
Revises: f703f382241b
Create Date: 2026-10-15 17:13:24.526218

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e00bfe0cddeb'
down_revision: Union[str, Sequence[str], None] = 'f703f382241b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        ALTER TABLE knowledge_chunks
        ALTER COLUMN embedding TYPE vector(384);
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        ALTER TABLE knowledge_chunks
        ALTER COLUMN embedding TYPE vector(1536);
        """
    )
