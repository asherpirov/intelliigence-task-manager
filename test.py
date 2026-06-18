from fastapi import FastAPI
from database.db_connection import ConnectionDB
import uvicorn
from pydantic import BaseModel
from typing import Literal
from database.agent_db import AgentDB
from database.mission_db import MissionDB

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

agent_maneger = AgentDB()
mission_manager = MissionDB()
app = FastAPI()


@app.get("/agents/top")
def get_top():
    return mission_manager.get_top_agent()



@app.post("/agents")
def create(data: NewAgent):
    data = data.model_dump(exclude_unset=True)
    return agent_maneger.create_agent(data)

@app.post("/missions")
def create_mission(data : NewMission):
    data = data.model_dump(exclude_unset=True)
    return mission_manager.create_mission(data)

@app.get("/agents/{id}/preform")
def preform(id):
    return agent_maneger.get_agent_performance(id)

@app.get("/agents/{id}")
def get_by_id(id):
    agent_maneger.get_agent_by_id(id)

@app.put("/agents/{id}")
def update(id, data:UpdateAgent):
    data = data.model_dump(exclude_unset=True)
    return agent_maneger.update_agent(id,data)



if __name__=="__main__":
    connector = ConnectionDB()
    connector.create_database()
    connector.create_tables()
    uvicorn.run(app)



