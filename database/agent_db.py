from database.db_connection import ConnectionDB

connector = ConnectionDB()

class AgentDB:

    def create_agent(self,data: dict)-> dict:
       conn =  connector.get_connection()
       cursor = conn.cursor(dictionary=True)
       query = """
            INSERT INTO agents (name, specialty, agent_rank) 
            VALUES (%s, %s, %s)
                """
       cursor.execute(query,(data["name"], data["specialty"],data["agent_rank"]))
       new_id = cursor.lastrowid
       conn.commit()
       cursor.close()
       conn.close()
       return self.get_agent_by_id(new_id)

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

    def update_agent(self, id, data: dict)-> bool:
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
                SELECT COUNT(*) as count FROM agents WHERE is_active= TRUE
                """
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row


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

    def get_agent_performance(self,id) -> dict:
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = f"""
                SELECT completed_missions, failed_missions FROM agents WHERE id=%s
                """
        cursor.execute(query,(id,))
        data = cursor.fetchone()
        completed = data["completed_missions"]
        failed = data["failed_missions"]
        total = completed + failed
        if total == 0:
            success_rate = 0
        else:
            success_rate = (completed/total) * 100

        preform_data = {"completed": completed,
                        "failed": failed,
                        "total": total,
                        "success_rate": success_rate}

        return preform_data
