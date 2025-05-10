import asyncpg, time, random
from fastapi import APIRouter, BackgroundTasks, Depends, WebSocket, WebSocketDisconnect
from ..database import get_db

router = APIRouter()

@router.websocket("/ws/simulation/{simulation_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    simulation_id: int,
    background_tasks: BackgroundTasks,
    db: asyncpg.Connection = Depends(get_db)
):
    await websocket.accept()

    # Set the simulation state to "running"
    update_state_query = """
        UPDATE simulations
        SET status = 'running'
        WHERE id = $1
    """
    await db.execute(update_state_query, simulation_id)

    try:
        for seconds in range(10, 100, 10):
            loss = round(random.uniform(0.1, 0.9), 3)
            query = """
                INSERT INTO convergence_data (simulation_id, seconds, loss)
                VALUES ($1, $2, $3)
                RETURNING seconds, loss
            """
            convergence_data = await db.fetchrow(query, simulation_id, seconds, loss)
            if convergence_data:
                await websocket.send_json(
                    {"seconds": convergence_data["seconds"], 
                    "loss": convergence_data["loss"]})
            time.sleep(1)  # Simulate real-time data generation
    except WebSocketDisconnect:
        # Set the simulation state to "finished" when the WebSocket disconnects
        update_state_query = """
            UPDATE simulations
            SET status = 'finished'
            WHERE id = $1
        """
        await db.execute(update_state_query, simulation_id)
        print("Client disconnected")
