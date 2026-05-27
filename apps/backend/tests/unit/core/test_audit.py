import pytest
from fastapi import FastAPI, Request, Response
from fastapi.testclient import TestClient

from edulafia.core.audit import AuditMiddleware

app = FastAPI()
app.add_middleware(AuditMiddleware)

@app.post("/test-post")
async def test_post():
    return {"status": "ok"}

@app.get("/test-get")
async def test_get():
    return {"status": "ok"}

client = TestClient(app)

def test_audit_middleware_logs_state_changing_requests(mocker):
    # We want to mock the DB insertion
    mock_insert = mocker.patch("edulafia.core.audit.insert_audit_log")
    
    response = client.post("/test-post", json={"data": "test"})
    assert response.status_code == 200
    
    # Verify insert_audit_log was called
    assert mock_insert.called
    args, kwargs = mock_insert.call_args
    assert kwargs["method"] == "POST"
    assert kwargs["path"] == "/test-post"

def test_audit_middleware_skips_get_requests(mocker):
    mock_insert = mocker.patch("edulafia.core.audit.insert_audit_log")
    
    response = client.get("/test-get")
    assert response.status_code == 200
    
    # GET requests shouldn't create an audit log
    assert not mock_insert.called
