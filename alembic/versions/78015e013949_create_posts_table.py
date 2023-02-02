"""create posts table

Revision ID: 78015e013949
Revises: 
Create Date: 2023-02-01 19:16:09.764799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "78015e013949"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("published", sa.Boolean(), server_default="TRUE", nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("posts")
