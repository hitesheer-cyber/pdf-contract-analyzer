"""SQLAlchemy ORM models for contracts and extracted entities."""

import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def _generate_uuid() -> str:
    """Generate a string UUID for primary keys."""
    return str(uuid.uuid4())


class Contract(Base):
    """A PDF contract that has been uploaded and processed."""

    __tablename__ = "contracts"

    id = Column(String, primary_key=True, default=_generate_uuid, index=True)
    filename = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default="processing")
    text_content = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    upload_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    entities = relationship(
        "Entity",
        back_populates="contract",
        cascade="all, delete-orphan",
    )


class Entity(Base):
    """A named entity extracted from a contract's text."""

    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(
        String, ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    text = Column(String, nullable=False)
    entity_type = Column(String, nullable=False, index=True)
    position = Column(Integer, nullable=False)
    confidence = Column(Float, nullable=True)

    contract = relationship("Contract", back_populates="entities")
