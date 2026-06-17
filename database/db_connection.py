import mysql.connector
from mysql.connector import Error


class ConnectionDB:
    def __init__(self, port = 3306):
        self.host = "localhost"
        self.user = "root"
        self.password = "1234"
        self.database = "Intelligence_db"
        self.port = port

    def get_connection(self):
        return mysql.connector.connect(
            host= self.host,
            user= self.user ,
            password = self.password,
            database= self.database,
            port= self.port
        )

    def create_database(self) -> None:
            conn = mysql.connector.connect(
                host= "localhost",
                user= "root",
                password= "1234",
                port= 3306
            )
            cursor = conn.cursor()
            query = """
            CREATE DATABASE IF NOT EXISTS Intelligence_db
                    """
            cursor.execute(query)
            conn.commit()
            cursor.close()
            conn.close()

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        agent_query = """
        CREATE TABLE IF NOT EXISTS agents (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL,
        specialty VARCHAR(50) NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        completed_missions INT DEFAULT 0,
        failed_missions INT DEFAULT 0,
        agent_rank ENUM('junior', 'senior', 'commander')
        )
                """
        cursor.execute(agent_query)

        missions_query = """
        CREATE TABLE IF NOT EXISTS missions (
        id INT PRIMARY KEY AUTO_INCREMENT,
        title VARCHAR(50) NOT NULL,
        description TEXT,
        location VARCHAR(50),
        difficulty INT NOT NULL,
        importance INT NOT NULL,
        status VARCHAR(50) DEFAULT 'NEW',
        level_risk VARCHAR(50) NOT NULL,
        assigned_agent_id INT NULL 
        )
                """
        cursor.execute(missions_query)
        conn.commit()
        cursor.close()
        conn.close()

if __name__ == "__main__":
    connector = ConnectionDB()
    connector.create_database()
    connector.create_tables()