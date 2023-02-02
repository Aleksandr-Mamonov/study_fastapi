"""add content column to posts table

Revision ID: 16f898cac990
Revises: 50ab8868a254
Create Date: 2023-02-01 19:27:56.959526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "16f898cac990"
down_revision = "50ab8868a254"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
