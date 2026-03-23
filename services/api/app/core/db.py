from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker
from sqlalchemy.types import JSON

from services.api.app.core.config import settings


class Base(DeclarativeBase):
    pass


class UserRecord(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    display_name: Mapped[str] = mapped_column(String(120))
    role: Mapped[str] = mapped_column(String(40), default="buyer")

    sessions: Mapped[list["SessionRecord"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    projects: Mapped[list["ProjectRecord"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
    )


class SessionRecord(Base):
    __tablename__ = "sessions"

    token: Mapped[str] = mapped_column(String(120), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped[UserRecord] = relationship(back_populates="sessions")


class ProjectRecord(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    owner_user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(120))
    region: Mapped[str | None] = mapped_column(String(120), nullable=True)
    budget: Mapped[str | None] = mapped_column(String(120), nullable=True)
    notes: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    owner: Mapped[UserRecord] = relationship(back_populates="projects")
    properties: Mapped[list["PropertyRecord"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )


class PropertyRecord(Base):
    __tablename__ = "properties"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    address: Mapped[str] = mapped_column(String(240))
    listing_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    property_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    source: Mapped[str | None] = mapped_column(String(120), nullable=True)

    project: Mapped[ProjectRecord] = relationship(back_populates="properties")
    visits: Mapped[list["VisitRecord"]] = relationship(
        back_populates="property",
        cascade="all, delete-orphan",
    )


class VisitRecord(Base):
    __tablename__ = "visits"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    property_id: Mapped[str] = mapped_column(ForeignKey("properties.id", ondelete="CASCADE"))
    visit_date: Mapped[str] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(40), default="draft")
    red_flags: Mapped[list[str]] = mapped_column(JSON, default=list)
    recommendation_notes: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    section_scores: Mapped[dict[str, int]] = mapped_column(JSON, default=dict)
    section_notes: Mapped[dict[str, str]] = mapped_column(JSON, default=dict)

    property: Mapped[PropertyRecord] = relationship(back_populates="visits")
    attachments: Mapped[list["AttachmentRecord"]] = relationship(
        back_populates="visit",
        cascade="all, delete-orphan",
    )


class AttachmentRecord(Base):
    __tablename__ = "attachments"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    visit_id: Mapped[str] = mapped_column(ForeignKey("visits.id", ondelete="CASCADE"))
    filename: Mapped[str] = mapped_column(String(200))
    content_type: Mapped[str] = mapped_column(String(120))
    category: Mapped[str] = mapped_column(String(80))
    storage_backend: Mapped[str] = mapped_column(String(40))
    storage_key: Mapped[str] = mapped_column(String(400))
    size_bytes: Mapped[int] = mapped_column(Integer)

    visit: Mapped[VisitRecord] = relationship(back_populates="attachments")


connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def reset_db() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
