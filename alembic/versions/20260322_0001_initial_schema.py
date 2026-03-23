"""initial schema

Revision ID: 20260322_0001
Revises: None
Create Date: 2026-03-22 00:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.types import JSON


revision = "20260322_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=50), primary_key=True),
        sa.Column("email", sa.String(length=200), nullable=False, unique=True),
        sa.Column("display_name", sa.String(length=120), nullable=False),
    )
    op.create_table(
        "sessions",
        sa.Column("token", sa.String(length=120), primary_key=True),
        sa.Column("user_id", sa.String(length=50), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    )
    op.create_table(
        "projects",
        sa.Column("id", sa.String(length=50), primary_key=True),
        sa.Column("owner_user_id", sa.String(length=50), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("region", sa.String(length=120), nullable=True),
        sa.Column("budget", sa.String(length=120), nullable=True),
        sa.Column("notes", sa.String(length=1000), nullable=True),
    )
    op.create_table(
        "properties",
        sa.Column("id", sa.String(length=50), primary_key=True),
        sa.Column("project_id", sa.String(length=50), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("address", sa.String(length=240), nullable=False),
        sa.Column("listing_price", sa.Integer(), nullable=True),
        sa.Column("property_type", sa.String(length=80), nullable=True),
        sa.Column("source", sa.String(length=120), nullable=True),
    )
    op.create_table(
        "visits",
        sa.Column("id", sa.String(length=50), primary_key=True),
        sa.Column("property_id", sa.String(length=50), sa.ForeignKey("properties.id", ondelete="CASCADE"), nullable=False),
        sa.Column("visit_date", sa.String(length=40), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("red_flags", JSON(), nullable=False),
        sa.Column("recommendation_notes", sa.String(length=1000), nullable=True),
        sa.Column("section_scores", JSON(), nullable=False),
        sa.Column("section_notes", JSON(), nullable=False),
    )
    op.create_table(
        "attachments",
        sa.Column("id", sa.String(length=50), primary_key=True),
        sa.Column("visit_id", sa.String(length=50), sa.ForeignKey("visits.id", ondelete="CASCADE"), nullable=False),
        sa.Column("filename", sa.String(length=200), nullable=False),
        sa.Column("content_type", sa.String(length=120), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("storage_backend", sa.String(length=40), nullable=False),
        sa.Column("storage_key", sa.String(length=400), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("attachments")
    op.drop_table("visits")
    op.drop_table("properties")
    op.drop_table("projects")
    op.drop_table("sessions")
    op.drop_table("users")
