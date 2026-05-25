from fastapi import APIRouter, Depends, BackgroundTasks, Request
from ..services.queue import get_trace_queue
from ..db.session import get_db
from ..models.schemas import Trace
from sqlalchemy.orm import Session
import uuid
import time

router = APIRouter()
queue = get_trace_queue()

@router.post("/v1/traces")
async def collect_trace(request: Request, background_tasks: BackgroundTasks):
    """
    OTLP-compatible trace ingestion endpoint.
    Accepts raw OTLP payloads and pushes them to the processing queue.
    """
    trace_data = await request.json()
    
    # Generate internal correlation if not present
    if "correlation_id" not in trace_data:
        trace_data["correlation_id"] = str(uuid.uuid4())
    
    trace_data["ingested_at"] = time.time()
    
    # Async push to Redis queue
    await queue.push(trace_data)
    
    return {"status": "accepted", "correlation_id": trace_data["correlation_id"]}

@router.get("/v1/traces")
async def get_traces(db: Session = Depends(get_db)):
    traces = db.query(Trace).all()
    return traces

@router.get("/health")
async def health_check():
    return {"status": "healthy"}
