import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from uuid import uuid4
from datetime import datetime
from unittest.mock import patch

from src.models.user import User
from src.models.task import Task
from src.main import app
from src.db.database import get_session


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


def test_create_task_success(client: TestClient, session: Session):
    """Test successful task creation"""
    # Create a user first
    user = User(
        id=uuid4(),
        email="test@example.com",
        hashed_password="fake_hashed_password",
        first_name="Test",
        last_name="User"
    )
    session.add(user)
    session.commit()
    
    # Mock the authentication to return our test user
    with patch('src.middleware.auth_middleware.verify_token', return_value={'sub': str(user.id)}):
        response = client.post(
            f"/api/users/{user.id}/tasks",
            json={
                "title": "Test Task",
                "description": "Test Description",
                "due_date": "2024-12-31T23:59:59",
                "priority": 3
            },
            headers={"Authorization": "Bearer fake_token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "Test Description"
        assert data["priority"] == 3


def test_create_task_missing_title(client: TestClient, session: Session):
    """Test task creation with missing title (should fail validation)"""
    # Create a user first
    user = User(
        id=uuid4(),
        email="test@example.com",
        hashed_password="fake_hashed_password",
        first_name="Test",
        last_name="User"
    )
    session.add(user)
    session.commit()
    
    # Mock the authentication to return our test user
    with patch('src.middleware.auth_middleware.verify_token', return_value={'sub': str(user.id)}):
        response = client.post(
            f"/api/users/{user.id}/tasks",
            json={
                "title": "",  # Empty title should fail validation
                "description": "Test Description"
            },
            headers={"Authorization": "Bearer fake_token"}
        )
        
        # Should return 422 for validation error
        assert response.status_code == 422


def test_create_task_invalid_priority(client: TestClient, session: Session):
    """Test task creation with invalid priority (should fail validation)"""
    # Create a user first
    user = User(
        id=uuid4(),
        email="test@example.com",
        hashed_password="fake_hashed_password",
        first_name="Test",
        last_name="User"
    )
    session.add(user)
    session.commit()
    
    # Mock the authentication to return our test user
    with patch('src.middleware.auth_middleware.verify_token', return_value={'sub': str(user.id)}):
        response = client.post(
            f"/api/users/{user.id}/tasks",
            json={
                "title": "Test Task",
                "description": "Test Description",
                "priority": 10  # Invalid priority (should be 1-5)
            },
            headers={"Authorization": "Bearer fake_token"}
        )
        
        # Should return 422 for validation error
        assert response.status_code == 422