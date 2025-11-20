from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional, Dict, Any


class EntityBase(BaseModel):
    """Base schema for entity data."""

    text: str = Field(..., description="The extracted entity text")
    entity_type: str = Field(
        ..., description="Type of entity (PERSON, ORG, DATE, MONEY, LOC, MISC)"
    )
    position: int = Field(..., description="Character position in the document")
    confidence: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Model confidence score"
    )


class EntityCreate(EntityBase):
    """Schema for creating a new entity."""

    contract_id: str


class EntityResponse(EntityBase):
    """Schema for entity response."""

    id: int
    contract_id: str

    model_config = ConfigDict(from_attributes=True)


class ContractBase(BaseModel):
    """Base schema for contract data."""

    filename: str = Field(..., description="Name of the uploaded PDF file")


class ContractCreate(ContractBase):
    """Schema for creating a new contract."""

    file_size: int = Field(..., description="Size of the file in bytes")


class ContractResponse(ContractBase):
    """Schema for contract response."""

    id: str
    upload_date: datetime
    file_size: int
    status: str
    error_message: Optional[str] = None
    entities: List[EntityResponse] = []

    model_config = ConfigDict(from_attributes=True)


class ContractSummary(BaseModel):
    """Schema for contract summary (without entities)."""

    id: str
    filename: str
    upload_date: datetime
    file_size: int
    status: str
    entities_count: int

    model_config = ConfigDict(from_attributes=True)


class UploadResponse(BaseModel):
    """Schema for upload response."""

    id: str
    filename: str
    upload_date: datetime
    entities_extracted: int
    status: str


class AnalyticsResponse(BaseModel):
    """Schema for analytics response."""

    total_contracts: int
    total_entities: int
    entity_type_distribution: Dict[str, int]
    most_frequent_entities: List[Dict[str, Any]]
    contracts_missing_key_entities: List[Dict[str, Any]]


class ErrorResponse(BaseModel):
    """Schema for error responses."""

    detail: str
    error_type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
