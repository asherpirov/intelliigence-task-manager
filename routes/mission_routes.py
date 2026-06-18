from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
from database.agent_db import AgentDB
from database.mission_db import MissionDB

mission_router = APIRouter()
agent_manager = AgentDB()
mission_manager = MissionDB()

class NewMission(BaseModel):
    title : str
    description : str
    location : str
    difficulty : int
    importance : int

class UpdateMission(BaseModel):
    title : str | None = None
    description : str |  None = None
    location : str |  None = None
    difficulty : int |  None = None
    importance : int |  None = None
    status : Literal['NEW', 'ASSIGNED','PROGRESS_IN','COMPLETED', 'FAILED', 'CANCELLED'] |  None = None

@mission_router.get("/missions")
def get_all_missions():
    return mission_manager.get_all_missions()

@mission_router.get("/missions/{id}")
def get_by_id(id: int):
    mission = mission_manager.get_mission_by_id(id)
    if mission is None:
        raise HTTPException(status_code=404, detail="mission not found")
    return mission

@mission_router.post("/missions", status_code=201)
def create_mission(data: NewMission):
        data = data.model_dump(exclude_unset=True)
        if 0 >= data["difficulty"] <= 11:
            raise HTTPException(status_code=400, detail="The difficulty value can only be between 1-10.")
        elif 0 >= data["importance"] <= 11:
            raise HTTPException(status_code=400, detail="The importance value can only be between 1-10.")
        elif data is None:
            raise HTTPException(status_code=422, detail="The body is empty.")
        return mission_manager.create_mission(data)

@mission_router.put("/missions/{id}/start")
def mission_start(id: int):
    mission = mission_manager.get_mission_by_id(id)
    if mission is None:
        raise HTTPException(status_code=404, detail="mission not found")
    elif mission["status"] == "ASSIGNED":
        return mission_manager.update_mission_status(id, "IN_PROGRESS")
    else:
        raise HTTPException(status_code=400, detail="The mission cannot start.")

@mission_router.put("/missions/{id}/complete")
def mission_completed(id: int):
    mission = mission_manager.get_mission_by_id(id)
    if mission is None:
        raise HTTPException(status_code=404, detail="mission not found")
    elif mission["status"] == "IN_PROGRESS":
        agent_manager.increment_completed(id)
        return mission_manager.update_mission_status(id, "COMPLETED")
    else:
        raise HTTPException(status_code=400, detail="The mission cannot completed.")



@mission_router.put("/missions/{id}/fail")
def mission_failed(id: int):
    mission = mission_manager.get_mission_by_id(id)
    if mission is None:
        raise HTTPException(status_code=404, detail="mission not found")
    elif mission["status"] == "IN_PROGRESS":
        agent_manager.increment_failed(id)
        return mission_manager.update_mission_status(id, "FAILED")
    else:
        raise HTTPException(status_code=400, detail="The mission cannot failed.")


@mission_router.put("/missions/{id}/cancel")
def mission_cancel(id: int):
    mission = mission_manager.get_mission_by_id(id)
    if mission is None:
        raise HTTPException(status_code=404, detail="mission not found")
    elif mission["status"] == "NEW" or mission["status"] == "ASSIGNED" :
        return mission_manager.update_mission_status(id, "CANCELLED")
    else:
        raise HTTPException(status_code=400, detail="The mission cannot cancelled.")

@mission_router.put("/missions/{id}/assign/{agent_id}")
def assign_mission_to_agent(m_id: int, a_id: int):
    mission = mission_manager.get_mission_by_id(m_id)
    agent = agent_manager.get_agent_by_id(a_id)

    if mission is None:
        raise HTTPException(status_code=404, detail="mission not found")
    elif agent is None:
        raise HTTPException(status_code=404, detail="agent not found")
    elif mission["status"] != "NEW":
        raise HTTPException(status_code=400, detail="The mission has already been assigned or is in progress")
    elif agent["is_active"] is False:
        raise HTTPException(status_code=400, detail="The agent not active")
    elif agent["agent_rank"] != "commander" and mission["risk_level"] == "CRITICAL":
        raise HTTPException(status_code=400, detail="Only a commander can handle a critical.")
    open_mission_by_agent = mission_manager.get_open_missions_by_agent(a_id)
    count_open = len(open_mission_by_agent)
    if count_open >= 3:
        raise HTTPException(status_code=400, detail="The agent already has 3 missions")
    return mission_manager.assign_mission(m_id, a_id)