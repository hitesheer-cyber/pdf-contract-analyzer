"""Tests for API endpoints."""

import pytest
from io import BytesIO


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert "version" in data


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_upload_contract_invalid_file_type(client):
    """Test uploading a non-PDF file."""
    file_content = b"This is not a PDF"
    files = {"file": ("test.txt", BytesIO(file_content), "text/plain")}

    response = client.post("/api/contracts/upload", files=files)
    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]


def test_list_contracts_empty(client):
    """Test listing contracts when none exist."""
    response = client.get("/api/contracts")
    assert response.status_code == 200
    assert response.json() == []


def test_get_analytics_empty(client):
    """Test getting analytics with no data."""
    response = client.get("/api/analytics")
    assert response.status_code == 200
    data = response.json()
    assert data["total_contracts"] == 0
    assert data["total_entities"] == 0
    assert data["entity_type_distribution"] == {}


def test_get_nonexistent_contract(client):
    """Test getting a contract that doesn't exist."""
    response = client.get("/api/contracts/nonexistent-id")
    assert response.status_code == 404
