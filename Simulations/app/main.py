from fastapi import FastAPI
from .api import machines, simulations, websockets

app = FastAPI()

app.include_router(machines.router, prefix="/machines", tags=["Machines"])
app.include_router(simulations.router, prefix="/simulations", tags=["Simulations"])
app.include_router(websockets.router)
