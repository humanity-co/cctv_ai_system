from fastapi import APIRouter, HTTPException
from pipeline.manager import PipelineManager
from typing import List

router = APIRouter()
manager = PipelineManager()

@router.get("/alerts")
async def get_alerts():
    return manager.alerts_history

@router.post("/streams/start")
async def start_stream(camera_id: int, source: str):
    manager.start_stream(camera_id, source)
    return {"status": "started", "camera_id": camera_id}

@router.post("/streams/stop")
async def stop_stream(camera_id: int):
    manager.stop_stream(camera_id)
    return {"status": "stopped", "camera_id": camera_id}
