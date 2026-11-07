import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Provides a FastAPI test client using the application router."""
    with TestClient(app) as c:
        yield c

@pytest.fixture
def test_db():
    """Configures an isolated test database session or mock store."""
    # Setup isolated test database / mock vector store here
    yield
    # Teardown / cleanup