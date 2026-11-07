from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_nonexistent_job():
    response = client.get("/api/v1/jobs/nonexistent-job-id")
    # Should return 404 if the job doesn't exist or is unauthorized
    assert response.status_code in [404, 403, 401]
