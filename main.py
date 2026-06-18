import uvicorn
from fastapi import FastAPI
from routes.agent_routes import agent_router
from routes.mission_routes import mission_router


app = FastAPI()
app.include_router(agent_router)
app.include_router(mission_router)



if __name__=="__main__":
    uvicorn.run(app)