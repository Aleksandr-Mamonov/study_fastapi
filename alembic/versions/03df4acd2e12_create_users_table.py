"""create users table

Revision ID: 03df4acd2e12
Revises: 78015e013949
Create Date: 2023-02-01 19:16:50.333030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "03df4acd2e12"
down_revision = "78015e013949"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("users")
