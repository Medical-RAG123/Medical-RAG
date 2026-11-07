from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_chat_api_exists():
    response = client.post("/api/v1/chat", json={"question": "What is diabetes?"})

    assert response.status_code in [200, 400, 422, 500]
