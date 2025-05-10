from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Machine(BaseModel):
    id: int
    name: str
    description: Optional[str]

class SimulationBase(BaseModel):
    name: str
    machine_id: int

class SimulationCreate(SimulationBase):
    pass

class Simulation(SimulationBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

class ConvergenceDataPoint(BaseModel):
    seconds: int
    loss: float
