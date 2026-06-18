from database.db_connection import ConnectionDB

connector = ConnectionDB()

class MissionDB:
    def create_mission(self,data: dict) -> dict:
       conn =  connector.get_connection()
       cursor = conn.cursor(dictionary=True)

       score = (data["difficulty"] * 2) + data["importance"]
       risk = "LOW"
       if 0 <= score <= 9:
           risk = "LOW"
       elif 10 <= score <= 17:
           risk = "MEDIUM"
       elif 18 <= score <= 24:
           risk = "HIGH"
       elif score >= 25:
           risk = "CRITICAL"

       status = "NEW"
       assigned_agent_id = None

       query = f"""
            INSERT INTO missions (title, description, location, difficulty, importance, status, risk_level ,assigned_agent_id) 
            VALUES (%s, %s, %s, %s, %s, %s ,%s ,%s)
                """

       cursor.execute(query,
                      (data["title"],
                       data["description"],
                       data["location"],
                       data["difficulty"],
                       data["importance"],
                       status,
                       risk,
                       assigned_agent_id))
       conn.commit()
       new_id = cursor.lastrowid
       cursor.close()
       conn.close()
       return self.get_mission_by_id(new_id)

    def get_all_missions(self) -> list[dict]:
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT * FROM missions
                """
        cursor.execute(query)
        missions = cursor.fetchall()
        cursor.close()
        conn.close()
        return missions

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

    def assign_mission(self,m_id, a_id):
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                 UPDATE missions SET assigned_agent_id= %s WHERE id= %s
                 """
        cursor.execute(query, (a_id,m_id))
        conn.commit()
        has_update = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return has_update

    def update_mission_status(self, id, status):
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                UPDATE missions SET status= %s WHERE id= %s
                """
        cursor.execute(query, (status, id))
        conn.commit()
        has_update = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return has_update

    def get_open_missions_by_agent(self, id)->list[dict]:
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                  SELECT * FROM missions WHERE id= %s AND status = "ASSIGNED" OR status = "IN_PROGRESS"
                   """
        cursor.execute(query, (id,))
        missions = cursor.fetchall()
        cursor.close()
        conn.close()
        return missions

    def count_all_missions(self):
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                 SELECT COUNT(*) as count FROM missions
                 """
        cursor.execute(query)
        missions = cursor.fetchall()
        cursor.close()
        conn.close()
        return missions

    def count_by_status(self, status):
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                 SELECT COUNT(*) as count FROM missions WHERE status= %s
                 """
        cursor.execute(query,(status,))
        missions = cursor.fetchone()
        cursor.close()
        conn.close()
        return missions

    def count_open_missions(self):
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
               SELECT COUNT(*) as count FROM missions WHERE status IN ("NEW", "ASSIGNED","IN_PROGRESS")
               
                 """
        cursor.execute(query)
        missions = cursor.fetchone()
        cursor.close()
        conn.close()
        return missions

    def count_critical_missions(self):
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT COUNT(*) as count FROM agents WHERE risk_level= "CRITICAL"
               """
        cursor.execute(query)
        missions = cursor.fetchone()
        cursor.close()
        conn.close()
        return missions

    def get_top_agent(self):
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                 SELECT * FROM agents WHERE completed_missions ORDER BY completed_missions DESC LIMIT 1
                """

        cursor.execute(query)
        top_agent = cursor.fetchone()
        cursor.close()
        conn.close()
        return top_agent


if __name__ == "__main__":
    m = MissionDB()

