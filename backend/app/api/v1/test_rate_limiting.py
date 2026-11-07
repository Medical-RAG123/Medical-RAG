from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_rate_limit_exceeded():
    # Example hitting a rate-limited endpoint repeatedly
    # (Adjust endpoint based on your routes, e.g., login or chat)
    response = None
    for _ in range(25):  # Assuming chat limit is 20/minute
        response = client.post("/api/v1/chat/", json={"prompt": "test"})

    # Once limit is breached, it should return 429
    assert response.status_code == 429
