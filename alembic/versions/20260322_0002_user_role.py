"""add user role

Revision ID: 20260322_0002
Revises: 20260322_0001
Create Date: 2026-03-22 00:10:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260322_0002"
down_revision = "20260322_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("role", sa.String(length=40), nullable=False, server_default="buyer"))


def downgrade() -> None:
    op.drop_column("users", "role")
