from database.db_connection import ConnectionDB
from pydantic import BaseModel
from typing import Literal

class NewAgent(BaseModel):
    name : str
    specialty : str
    is_active : bool
    completed_missions : int
    failed_missions : int
    agent_rank : Literal['junior', 'senior','commander']

class UpdateAgent(BaseModel):
    name : str | None = None
    specialty : str |  None = None
    is_active : bool |  None = None
    completed_missions : int |  None = None
    failed_missions : int |  None = None
    agent_rank : Literal['junior', 'senior','commander'] |  None = None

connector = ConnectionDB()

class AgentDB:

    def create_agent(self,data: NewAgent):
       conn =  connector.get_connection()
       cursor = conn.cursor(dictionary=True)
       query = """
            INSERT INTO agents (name, specialty, agent_rank) 
            VALUES (%s, %s, %s)
                """
       cursor.execute(query,(data.name, data.specialty,data.agent_rank))
       conn.commit()
       cursor.close()
       conn.close()
       return {"message": "Agent creation successful"}

    def get_all_agents(self) -> list[dict]:
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT * FROM agents
                """
        cursor.execute(query)
        agents = cursor.fetchall()
        cursor.close()
        conn.close()
        return agents

    def get_agent_by_id(self,id:int) -> dict:
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT * FROM agents WHERE id= %s
                """
        cursor.execute(query,(id,))
        agent = cursor.fetchone()
        cursor.close()
        conn.close()
        return agent

    def update_agent(self, id, data: UpdateAgent):
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)

        keys = [f"{key} =%s" for key in data.keys()]
        str_keys = ", ".join(keys)
        query = f"""
                  UPDATE agents SET {str_keys} WHERE id=%s
                 """
        values = list(data.values()) + [id]
        cursor.execute(query,values)
        conn.commit()
        has_update = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return has_update

    def deactivate_agent(self, id):
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = f"""
                 UPDATE agents SET is_active= FALSE WHERE id=%s
                 """
        cursor.execute(query, (id,))
        conn.commit()
        has_update = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return has_update

    def count_active_agents(self):
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = f"""
                SELECT COUNT(*) FROM agents WHERE is_active= TRUE
                """
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

#####
    def increment_completed(self,id):
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = f"""
                  UPDATE agents SET completed_missions= completed_missions + 1 WHERE id=%s
                """
        cursor.execute(query, (id,))
        conn.commit()
        has_update = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return has_update
#####
    def increment_failed(self,id):
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = f"""
                  UPDATE agents SET failed_missions = failed_missions + 1 WHERE id=%s
                """
        cursor.execute(query, (id,))
        conn.commit()
        has_update = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return has_update
#####
    def get_agent_performance(self,id):
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        pass