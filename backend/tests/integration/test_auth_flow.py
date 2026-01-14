import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from uuid import uuid4
from passlib.context import CryptContext
from unittest.mock import patch

from src.models.user import User
from src.main import app
from src.db.database import get_session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_authentication_flow_complete(client: TestClient, session: Session):
    """Test the complete user authentication flow"""
    # Step 1: Register a new user
    response = client.post(
        "/api/auth/register",
        json={
            "email": "authflow@example.com",
            "password": "SecurePassword123!",
            "first_name": "Auth",
            "last_name": "Flow"
        }
    )
    assert response.status_code == 200
    user_data = response.json()
    user_id = user_data["id"]
    assert user_data["email"] == "authflow@example.com"
    assert user_data["first_name"] == "Auth"
    
    # Step 2: Login with the registered user
    response = client.post(
        "/api/auth/login",
        json={
            "email": "authflow@example.com",
            "password": "SecurePassword123!"
        }
    )
    assert response.status_code == 200
    login_data = response.json()
    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"
    token = login_data["access_token"]
    
    # Step 3: Use the token to access protected endpoint (get user info)
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    user_info = response.json()
    assert user_info["id"] == user_id
    assert user_info["email"] == "authflow@example.com"
    
    # Step 4: Use the token to create a task (requires authentication)
    response = client.post(
        f"/api/users/{user_id}/tasks",
        json={
            "title": "Auth Flow Test Task",
            "description": "Task created during auth flow test",
            "priority": 1
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    task_data = response.json()
    task_id = task_data["id"]
    assert task_data["title"] == "Auth Flow Test Task"
    
    # Step 5: Verify that the task was created for the correct user
    response = client.get(
        f"/api/users/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id
    assert tasks[0]["title"] == "Auth Flow Test Task"


def test_unauthenticated_access_denied(client: TestClient, session: Session):
    """Test that unauthenticated requests are denied access to protected endpoints"""
    # Try to access a protected endpoint without a token
    response = client.get("/api/auth/me")
    assert response.status_code == 401  # Unauthorized
    
    # Try to access a protected endpoint with an invalid token
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401  # Unauthorized
    
    # Create a user to test with
    user = User(
        id=uuid4(),
        email="protected@example.com",
        hashed_password=pwd_context.hash("password123"),
        first_name="Protected",
        last_name="User"
    )
    session.add(user)
    session.commit()
    
    # Try to access user's tasks without authentication
    response = client.get(f"/api/users/{user.id}/tasks")
    assert response.status_code == 401  # Unauthorized


def test_token_based_user_isolation(client: TestClient, session: Session):
    """Test that JWT tokens enforce user data isolation"""
    # Create two users
    user1 = User(
        id=uuid4(),
        email="isolation1@example.com",
        hashed_password=pwd_context.hash("password123"),
        first_name="Isolation",
        last_name="User1"
    )
    user2 = User(
        id=uuid4(),
        email="isolation2@example.com",
        hashed_password=pwd_context.hash("password123"),
        first_name="Isolation",
        last_name="User2"
    )
    session.add(user1)
    session.add(user2)
    session.commit()
    
    # Mock token verification to simulate user1's token
    with patch('src.middleware.auth_middleware.verify_token', return_value={'sub': str(user1.id)}):
        # User1 creates a task
        response = client.post(
            f"/api/users/{user1.id}/tasks",
            json={
                "title": "User1's Private Task",
                "description": "This should only be accessible by user1",
                "priority": 1
            },
            headers={"Authorization": "Bearer user1_token"}
        )
        assert response.status_code == 200
        task_data = response.json()
        task_id = task_data["id"]
        assert task_data["title"] == "User1's Private Task"
    
    # Now simulate user2 trying to access user1's task using the path parameter
    # This should fail because the token doesn't match the path user_id
    with patch('src.middleware.auth_middleware.verify_token', return_value={'sub': str(user2.id)}):
        response = client.get(
            f"/api/users/{user1.id}/tasks/{task_id}",  # Accessing user1's task
            headers={"Authorization": "Bearer user2_token"}
        )
        assert response.status_code == 403  # Forbidden - user2 can't access user1's task