import asyncpg
from fastapi import APIRouter, Depends
from typing import List
from ..models import Machine
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[Machine])
async def list_machines(db: asyncpg.Connection = Depends(get_db)):
    query = "SELECT * FROM machines"
    machines = await db.fetch(query)
    return [Machine(**machine) for machine in machines]
