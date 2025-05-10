import asyncio, pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from ..app.main import app
from ..app.database import get_db

client = TestClient(app)

mock_simulation_1 = {
    "name": "First simulation",
    "machine_id": 1,
    "id": 1,
    "status": "running",
    "created_at": "2024-06-26T21:05:26.007243",
    "updated_at": "2024-06-26T21:05:26.007243"
}

mock_simulation_2 = {
    "name": "Second simulation",
    "machine_id": 2,
    "id": 2,
    "status": "pending",
    "created_at": "2024-06-26T21:05:26.007243",
    "updated_at": "2024-06-26T21:05:26.007243"
}

async def override_get_db():
    mock_conn = AsyncMock()
    mock_conn.fetch.return_value = [mock_simulation_1, mock_simulation_2]
    mock_conn.fetchrow.return_value = mock_simulation_1
    try:
        yield mock_conn
    finally:
        await mock_conn.close()

@pytest.mark.asyncio
async def test_list_simulations():
    app.dependency_overrides[get_db] = override_get_db
    try:
        response = client.get("/simulations/")
        assert response.status_code == 200
        assert response.json() == [mock_simulation_1, mock_simulation_2]
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_list_simulations_invalid_order_by():
    app.dependency_overrides[get_db] = override_get_db
    try:
        response = client.get("/simulations/?order_by=nonexisting")
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid order_by field"}
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_list_simulations_invalid_status():
    app.dependency_overrides[get_db] = override_get_db
    try:
        response = client.get("/simulations/?status=nonexisting")
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid status"}
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_simulation():
    app.dependency_overrides[get_db] = override_get_db
    try:
        response = client.get("/simulations/1")
        assert response.status_code == 200
        assert response.json() == mock_simulation_1
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_simulation_wrong_id():
    async def override_get_db():
        mock_conn = AsyncMock()
        mock_conn.fetchrow.return_value = {}
        try:
            yield mock_conn
        finally:
            await mock_conn.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        response = client.get("/simulations/10")
        assert response.status_code == 404
        assert response.json() == {"detail": "Simulation not found"}
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_create_simulation():
    app.dependency_overrides[get_db] = override_get_db
    try:
        simulation_data = {
            "name": "New Simulation",
            "machine_id": 1
        }
        response = client.post("/simulations/", json=simulation_data)
        assert response.status_code == 200
        assert response.json() == mock_simulation_1
    finally:
        app.dependency_overrides.clear()
