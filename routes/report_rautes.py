from fastapi import APIRouter, HTTPException
from database.agent_db import AgentDB
from database.mission_db import MissionDB

agent_manager = AgentDB()
mission_manager = MissionDB()
report_router = APIRouter()

@report_router.get("/reports/summary")
def get_all_summary():
    active_agent_count = agent_manager.count_active_agents()
    total_missions = mission_manager.count_all_missions()
    open_missions = mission_manager.count_open_missions()
    completed_missions = mission_manager.count_by_status("COMPLETED")
    failed_missions = mission_manager.count_by_status("FAILED")
    cancel_missions = mission_manager.count_cancelled_missions()

    summary = {"active_agent_count": active_agent_count["count"],
               "total_missions": len(total_missions),
               "open_missions": open_missions["count"],
               "completed_missions": completed_missions["count"],
               "failed_missions": failed_missions["count"],
               "cancel_missions": cancel_missions["count"]}
    if not summary:
        return {{"active_agent_count": 0,
               "total_missions": 0,
               "open_missions": 0,
               "completed_missions": 0,
               "failed_missions": 0,
               "cancel_missions": 0}}
    return summary


@report_router.get("/reports/missions-by-status")
def mission_by_status():
    open = mission_manager.count_open_missions()
    in_progress = mission_manager.count_by_status("IN_PROGRESS")
    completed = mission_manager.count_by_status("COMPLETED")
    failed = mission_manager.count_by_status("FAILED")
    cancel = mission_manager.count_cancelled_missions()

    missions_status = {"open": open["count"],
               "in_progress": in_progress["count"],
               "completed": completed["count"],
               "failed": failed["count"],
               "cancel": cancel["count"]}
    if not missions_status:
        return {"open": 0,
               "in_progress": 0,
               "completed": 0,
               "failed": 0,
               "cancel":0}
    return missions_status

@report_router.get("/reports/top-agent")
def top_agent():
    agent = mission_manager.get_top_agent()
    if agent is None:
        raise HTTPException(status_code=404, detail="not found")
    return mission_manager.get_top_agent()
