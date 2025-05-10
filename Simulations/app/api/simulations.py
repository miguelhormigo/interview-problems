import asyncpg
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from datetime import datetime
from ..models import Simulation, SimulationCreate, ConvergenceDataPoint
from ..database import get_db

STATUS_PENDING = 'pending'
STATUS_RUNNING = 'running'
STATUS_FINISHED = 'finished'

router = APIRouter()

@router.get("/", response_model=List[Simulation])
async def list_simulations(
    status: Optional[str] = None,
    order_by: Optional[str] = None,
    order_direction: Optional[str] = 'asc',
    db: asyncpg.Connection = Depends(get_db)
):
    # Check fields
    if order_by and order_by not in Simulation.model_fields.keys():
        raise HTTPException(status_code=400, detail=f"Invalid order_by field")
    if order_direction and order_direction not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail=f"Invalid order_direction")
    if status and status not in [STATUS_PENDING, STATUS_RUNNING, STATUS_FINISHED]:
        raise HTTPException(status_code=400, detail=f"Invalid status")

    base_query = "SELECT * FROM simulations"
    conditions = []
    values = []

    # Filtering by status
    if status:
        conditions.append("status = $1")
        values.append(status)

    # Adding conditions to the query
    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    # Ordering
    if order_by:
        base_query += f" ORDER BY {order_by} {order_direction}"

    simulations = await db.fetch(base_query, *values)
    return [Simulation(**sim) for sim in simulations]

@router.get("/{simulation_id}", response_model=Simulation)
async def get_simulation(
    simulation_id: int,
    db: asyncpg.Connection = Depends(get_db)
):
    query = """
        SELECT id, name, status, machine_id, created_at, updated_at
        FROM simulations
        WHERE id = $1
    """
    simulation = await db.fetchrow(query, simulation_id)
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return Simulation(**simulation)

@router.post("/", response_model=Simulation)
async def create_simulation(
    simulation: SimulationCreate,
    db: asyncpg.Connection = Depends(get_db)
):
    # Check if machine exists
    machine_check_query = "SELECT id FROM machines WHERE id = $1"
    machine_exists = await db.fetchval(machine_check_query, simulation.machine_id)
    if not machine_exists:
        raise HTTPException(status_code=404, detail="Machine not found")

    created_at = datetime.utcnow()
    updated_at = created_at
    status = "pending"
    query = """
        INSERT INTO simulations (name, status, machine_id, created_at, 
            updated_at)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id, name, status, machine_id, created_at, updated_at
    """
    simulation_data = await db.fetchrow(query, simulation.name, status, 
        simulation.machine_id, created_at, updated_at)
    if not simulation_data:
        raise HTTPException(status_code=400,
            detail="Simulation could not be created")
    return Simulation(**simulation_data)

@router.get("/{simulation_id}/convergence", response_model=List[ConvergenceDataPoint])
async def get_simulation_convergence(
    simulation_id: int, 
    db: asyncpg.Connection = Depends(get_db)
):
    # Check if the simulation exists
    simulation_query = """
        SELECT status
        FROM simulations
        WHERE id = $1
    """
    simulation = await db.fetchrow(simulation_query, simulation_id)
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")

    # Check the state of the simulation
    if simulation['status'] != 'finished':
        raise HTTPException(status_code=400, detail="Simulation is not finished")

    query = """
        SELECT seconds, loss
        FROM convergence_data
        WHERE simulation_id = $1
        ORDER BY seconds
    """
    rows = await db.fetch(query, simulation_id)
    if not rows:
        raise HTTPException(status_code=404, detail="Convergence data not found")
    return [ConvergenceDataPoint(seconds=row['seconds'], loss=row['loss']) for row in rows]
