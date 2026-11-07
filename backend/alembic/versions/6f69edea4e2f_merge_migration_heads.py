"""Merge migration heads

Revision ID: 6f69edea4e2f
Revises: 713b978734ad, dd9cd52afa0c
Create Date: 2026-08-26 11:04:23.607916

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "6f69edea4e2f"
down_revision: str | Sequence[str] | None = ("713b978734ad", "dd9cd52afa0c")
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
