"""API endpoints for contract management."""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import logging
from datetime import datetime

from app.database import get_db
from app.models import Contract, Entity
from app.schemas import (
    ContractResponse,
    ContractSummary,
    UploadResponse,
    AnalyticsResponse,
    ErrorResponse,
)
from app.services import (
    PDFService,
    PDFExtractionError,
    get_nlp_service,
    EntityExtractionError,
)
from app.config import settings

router = APIRouter(prefix="/api", tags=["contracts"])
logger = logging.getLogger(__name__)


@router.post(
    "/contracts/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse},
        413: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def upload_contract(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> UploadResponse:
    """
    Upload and process a PDF contract.

    - **file**: PDF file to upload (max 10MB)

    Returns contract information with extracted entities count.
    """
    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are allowed"
        )

    # Read file content
    file_content = await file.read()
    file_size = len(file_content)

    # Validate file size
    if file_size > settings.max_upload_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=(
                f"File size exceeds maximum allowed size of "
                f"{settings.max_upload_size / 1024 / 1024}MB"
            ),
        )

    # Validate PDF
    if not PDFService.validate_pdf(file_content):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid PDF file"
        )

    # Create contract record
    contract = Contract(
        filename=file.filename, file_size=file_size, status="processing"
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)

    try:
        # Extract text from PDF
        logger.info(f"Extracting text from {file.filename}")
        text_content = PDFService.extract_text(file_content, file.filename)
        contract.text_content = text_content

        # Extract entities using NLP
        logger.info(f"Extracting entities from {file.filename}")
        nlp_service = get_nlp_service(settings.nlp_model_name)
        entities_data = nlp_service.extract_entities(text_content)

        # Save entities to database
        for entity_data in entities_data:
            entity = Entity(
                contract_id=contract.id,
                text=entity_data["text"],
                entity_type=entity_data["entity_type"],
                position=entity_data["position"],
                confidence=entity_data["confidence"],
            )
            db.add(entity)

        # Update contract status
        contract.status = "processed"
        db.commit()
        db.refresh(contract)

        logger.info(
            f"Successfully processed {file.filename}: "
            f"{len(entities_data)} entities extracted"
        )

        return UploadResponse(
            id=contract.id,
            filename=contract.filename,
            upload_date=contract.upload_date,
            entities_extracted=len(entities_data),
            status=contract.status,
        )

    except (PDFExtractionError, EntityExtractionError) as e:
        contract.status = "failed"
        contract.error_message = str(e)
        db.commit()
        logger.error(f"Error processing {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    except Exception as e:
        contract.status = "failed"
        contract.error_message = str(e)
        db.commit()
        logger.error(f"Unexpected error processing {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during processing",
        )


@router.get(
    "/contracts/{contract_id}",
    response_model=ContractResponse,
    responses={404: {"model": ErrorResponse}},
)
def get_contract(
    contract_id: str,
    db: Session = Depends(get_db),
) -> ContractResponse:
    """
    Get details of a specific contract including all extracted entities.

    - **contract_id**: UUID of the contract
    """
    contract = db.query(Contract).filter(Contract.id == contract_id).first()

    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contract with ID {contract_id} not found",
        )

    return contract


@router.get(
    "/contracts",
    response_model=List[ContractSummary],
)
def list_contracts(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
) -> List[ContractSummary]:
    """
    List all contracts with summary information.

    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    """
    contracts = (
        db.query(Contract)
        .order_by(Contract.upload_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Build summary with entity counts
    summaries = []
    for contract in contracts:
        entities_count = (
            db.query(Entity).filter(Entity.contract_id == contract.id).count()
        )
        summaries.append(
            ContractSummary(
                id=contract.id,
                filename=contract.filename,
                upload_date=contract.upload_date,
                file_size=contract.file_size,
                status=contract.status,
                entities_count=entities_count,
            )
        )

    return summaries


@router.get(
    "/analytics",
    response_model=AnalyticsResponse,
)
def get_analytics(db: Session = Depends(get_db)) -> AnalyticsResponse:
    """
    Get analytics on extracted entities across all contracts.

    Returns:
    - Total number of contracts
    - Total number of entities
    - Distribution of entity types
    - Most frequent entities
    - Contracts missing key entity types
    """
    # Total counts
    total_contracts = db.query(Contract).count()
    total_entities = db.query(Entity).count()

    # Entity type distribution
    entity_type_counts = (
        db.query(Entity.entity_type, func.count(Entity.id))
        .group_by(Entity.entity_type)
        .all()
    )
    entity_type_distribution = {
        entity_type: count for entity_type, count in entity_type_counts
    }

    # Most frequent entities
    frequent_entities = (
        db.query(Entity.text, func.count(Entity.id))
        .group_by(Entity.text)
        .order_by(func.count(Entity.id).desc())
        .limit(10)
        .all()
    )
    most_frequent_entities = [
        {"text": text, "count": count} for text, count in frequent_entities
    ]

    # Find contracts missing key entity types
    key_entity_types = {"PERSON", "ORG", "DATE", "MONEY"}
    all_contracts = db.query(Contract).filter(Contract.status == "processed").all()

    contracts_missing_key_entities = []
    for contract in all_contracts:
        entity_types = {
            entity.entity_type
            for entity in db.query(Entity)
            .filter(Entity.contract_id == contract.id)
            .all()
        }
        missing_types = key_entity_types - entity_types

        if missing_types:
            contracts_missing_key_entities.append(
                {
                    "id": contract.id,
                    "filename": contract.filename,
                    "missing_types": list(missing_types),
                }
            )

    return AnalyticsResponse(
        total_contracts=total_contracts,
        total_entities=total_entities,
        entity_type_distribution=entity_type_distribution,
        most_frequent_entities=most_frequent_entities,
        contracts_missing_key_entities=contracts_missing_key_entities,
    )
