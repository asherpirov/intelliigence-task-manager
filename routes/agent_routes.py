from fastapi import APIRouter, HTTPException
from database.db_connection import ConnectionDB
import uvicorn
from pydantic import BaseModel
from typing import Literal
from database.agent_db import AgentDB

agent_router = APIRouter()
agent_manager = AgentDB()

class NewAgent(BaseModel):
    name : str
    specialty : str
    agent_rank : Literal['junior', 'senior','commander']

class UpdateAgent(BaseModel):
    name : str | None = None
    specialty : str |  None = None
    is_active : bool |  None = None
    completed_missions : int |  None = None
    failed_missions : int |  None = None
    agent_rank : Literal['junior', 'senior','commander'] |  None = None

@agent_router.get("/agents")
def get_all():
    return agent_manager.get_all_agents()

@agent_router.post("/agents", status_code=201)
def create_new_agent(data: NewAgent):
    data = data.model_dump(exclude_unset=True)
    return agent_manager.create_agent(data)

@agent_router.get("/agents/{id}")
def get_by_id(id: int):
    agent = agent_manager.get_agent_by_id(id)
    if agent is None:
        raise HTTPException(status_code=404, detail="agent not found")
    return agent

@agent_router.put("/agents/{id}")
def update_agent(id: int, data: UpdateAgent):
    agent = agent_manager.get_agent_by_id(id)
    data = data.model_dump(exclude_unset=True)
    if agent is None:
        raise HTTPException(status_code=404, detail="agent not found")
    if not data:
        raise HTTPException(status_code=400, detail= "not update, the body is empty")
    return agent_manager.update_agent(id, data)

@agent_router.put("/agents/{id}/deactivate")
def deactivate_agent(id: int):
    agent = agent_manager.get_agent_by_id(id)
    if agent is None:
        raise HTTPException(status_code=404, detail="agent not found")
    return agent_manager.deactivate_agent(id)

@agent_router.get("/agents/{id}/performance")
def preform_agent(id: int):
    agent = agent_manager.get_agent_by_id(id)
    if agent is None:
        raise HTTPException(status_code=404, detail="agent not found")
    return agent_manager.get_agent_performance(id)
