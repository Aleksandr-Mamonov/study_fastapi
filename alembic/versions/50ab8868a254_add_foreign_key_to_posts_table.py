"""add foreign key to posts table

Revision ID: 50ab8868a254
Revises: 03df4acd2e12
Create Date: 2023-02-01 19:18:08.986448

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "50ab8868a254"
down_revision = "03df4acd2e12"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
