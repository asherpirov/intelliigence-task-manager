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
        try:
            return mysql.connector.connect(
                host= self.host,
                user= self.user ,
                password = self.password,
                database= self.database,
                port= self.port
            )
        except mysql.connector.Error as e:
            return e

    def create_database(self):

            conn = self.get_connection()
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
        difficulty INT,
        importance INT,
        status VARCHAR(50) DEFAULT 'NEW',
        level_risk VARCHAR(50),
        assigned_agent_id INT NULL 
        )
                """
        cursor.execute(missions_query)
        conn.commit()
        cursor.close()
        conn.close()

conne = ConnectionDB()
