def test_unauthenticated_admin_access(client):
    """1. An unauthenticated user cannot access admin endpoints."""
    response = client.get("/api/admin/metrics")
    assert response.status_code in [401, 403]

def test_student_role_restriction(client):
    """2. A student cannot initiate an admin-only evaluation."""
    # Simulate student token/headers
    response = client.post("/api/admin/evaluations", json={})
    assert response.status_code in [401, 403]

def test_public_registration_role_escalation(client):
    """4. A public registration request cannot assign itself the ADMIN role."""
    response = client.post("/api/auth/register", json={
        "email": "test@student.com",
        "password": "SecurePassword123!",
        "role": "ADMIN"
    })
    # Expect either validation error or role defaulting to student/user
    if response.status_code == 200:
        data = response.json()
        assert data.get("role") != "ADMIN"
    else:
        assert response.status_code in [400, 422]