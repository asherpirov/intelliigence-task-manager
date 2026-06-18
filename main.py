import uvicorn
from fastapi import FastAPI
from routes.agent_routes import agent_router
from routes.mission_routes import mission_router
from routes.report_rautes import report_router
from database.db_connection import ConnectionDB

app = FastAPI()
app.include_router(agent_router)
app.include_router(mission_router)
app.include_router(report_router)
conn = ConnectionDB()

if __name__=="__main__":
    uvicorn.run(app)
    conn.create_database()
    conn.create_tables()
