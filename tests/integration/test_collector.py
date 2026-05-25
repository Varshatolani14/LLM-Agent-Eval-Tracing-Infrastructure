import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.db.session import Base, engine, SessionLocal
import os

# Use a separate test database
TEST_DATABASE_URL = "sqlite:///./test_llm_eval.db"

@pytest.fixture(scope="module")
def client():
    # Setup test database
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    # Teardown
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test_llm_eval.db"):
        os.remove("./test_llm_eval.db")

def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_collect_trace(client):
    trace_payload = {
        "session_id": "test-session",
        "spans": [
            {
                "name": "test-span",
                "type": "llm",
                "attributes": {"prompt": "hello", "response": "hi"}
            }
        ]
    }
    response = client.post("/api/v1/traces", json=trace_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "accepted"
    assert "correlation_id" in response.json()
