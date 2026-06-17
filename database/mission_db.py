from database.db_connection import ConnectionDB
from pydantic import BaseModel
from typing import Literal

class NewMission(BaseModel):
    name : str
    title : str
    description : str
    location : str
    difficulty : int
    importance : int
    status : Literal['NEW', 'ASSIGNED','PROGRESS_IN','COMPLETED', 'FAILED', 'CANCELLED'] |  None = None
    level_risk : str
    assigned_agent_id : None

class UpdateMission(BaseModel):
    title : str | None = None
    description : str |  None = None
    location : str |  None = None
    difficulty : int |  None = None
    importance : int |  None = None
    status : Literal['NEW', 'ASSIGNED','PROGRESS_IN','COMPLETED', 'FAILED', 'CANCELLED'] |  None = None
    level_risk : str
    assigned_agent_id : str | None

connector = ConnectionDB()

class MissionDB:
## not finished
    def create_mission(self,data: NewMission):
       conn =  connector.get_connection()
       cursor = conn.cursor(dictionary=True)


       level_risk = data.difficulty * 2 + data.importance
       if level_risk >= 0 or level_risk <= 9:
           data.level_risk = "LOW"
       elif level_risk >= 10 or level_risk <= 17:
           data.level_risk = "MEDIUM"
       elif level_risk >= 18 or level_risk <= 24:
           data.level_risk = "HIGH"
       elif level_risk >= 25:
           data.level_risk = "CRITICAL"

       query = f"""
            INSERT INTO missions (title, description, location, difficulty, importance, status, level_risk ,assigned_agent_id) 
            VALUES (%s, %s, %s, %s, %s, %s,{level_risk},%s)
                """

       cursor.execute(query,(data.title, data.description
                            ,data.location, data.difficulty, data.importance,
                             data.status,data.level_risk, data.assigned_agent_id))
       conn.commit()
       cursor.close()
       conn.close()
       return {"message": "Mission creation successful"}

    def get_all_missions(self) -> list[dict]:
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT * FROM missions
                """
        cursor.execute(query)
        agents = cursor.fetchall()
        cursor.close()
        conn.close()
        return agents

    def get_mission_by_id(self,id:int) -> dict:
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT * FROM missions WHERE id= %s
                """
        cursor.execute(query,(id,))
        mission = cursor.fetchone()
        cursor.close()
        conn.close()
        return mission