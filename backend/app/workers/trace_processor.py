import asyncio
import json
import uuid
from app.services.queue import get_trace_queue
from app.db.session import SessionLocal
from app.models.schemas import Trace, Span, ToolCall
from datetime import datetime

async def process_traces():
    queue = get_trace_queue()
    print("Worker started: Listening for traces...")
    
    while True:
        trace_payload = await queue.pop()
        if not trace_payload:
            await asyncio.sleep(1)
            continue
            
        print(f"Processing trace: {trace_payload.get('correlation_id')}")
        
        db = SessionLocal()
        try:
            # Simplified OTLP -> DB mapping logic
            # In a real system, this would parse nested spans recursively
            
            trace_id = trace_payload.get("trace_id", "t-" + trace_payload["correlation_id"])
            
            new_trace = Trace(
                trace_id=trace_id,
                session_id=trace_payload.get("session_id"),
                correlation_id=trace_payload["correlation_id"],
                status="success",
                start_time=datetime.fromtimestamp(trace_payload["ingested_at"])
            )
            db.add(new_trace)
            db.commit()
            
            # Create a root span if data exists
            if "spans" in trace_payload:
                for span_data in trace_payload["spans"]:
                    new_span = Span(
                        trace_id=trace_id,
                        span_id=span_data.get("span_id", "s-" + str(uuid.uuid4())),
                        parent_span_id=span_data.get("parent_span_id"),
                        name=span_data.get("name", "unnamed_span"),
                        span_type=span_data.get("type", "llm"),
                        attributes=span_data.get("attributes", {}),
                        status=span_data.get("status", "success")
                    )
                    db.add(new_span)
            
            db.commit()
            print(f"Trace {trace_id} saved to DB.")
            
        except Exception as e:
            print(f"Error processing trace: {e}")
            db.rollback()
        finally:
            db.close()

if __name__ == "__main__":
    asyncio.run(process_traces())
