import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from ..app.main import app
from ..app.database import get_db

client = TestClient(app)

async def override_get_db():
    mock_conn = AsyncMock()
    mock_conn.fetch.return_value = [
        {"id": 1, "name": "Machine 1", "description": "Test machine 1"},
        {"id": 2, "name": "Machine 2", "description": "Test machine 2"},
    ]
    try:
        yield mock_conn
    finally:
        await mock_conn.close()

@pytest.mark.asyncio
async def test_list_machines():
    app.dependency_overrides[get_db] = override_get_db
    try:
        response = client.get("/machines")
        assert response.status_code == 200
        assert response.json() == [
            {"id": 1, "name": "Machine 1", "description": "Test machine 1"},
            {"id": 2, "name": "Machine 2", "description": "Test machine 2"},
        ]
    finally:
        app.dependency_overrides.clear()
