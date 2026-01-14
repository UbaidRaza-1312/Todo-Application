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


def test_toggle_task_completion_success(client: TestClient, session: Session):
    """Test successful toggling of task completion status"""
    # Create a user and task
    user = User(
        id=uuid4(),
        email="test@example.com",
        hashed_password="fake_hashed_password",
        first_name="Test",
        last_name="User"
    )
    session.add(user)
    session.commit()
    
    task = Task(
        id=uuid4(),
        title="Test Task",
        description="Test Description",
        completed=False,  # Initially incomplete
        user_id=user.id
    )
    session.add(task)
    session.commit()
    
    # Mock the authentication to return our test user
    with patch('src.middleware.auth_middleware.verify_token', return_value={'sub': str(user.id)}):
        # Toggle the task completion status
        response = client.patch(
            f"/api/users/{user.id}/tasks/{task.id}/complete",
            headers={"Authorization": "Bearer fake_token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(task.id)
        assert data["completed"] is True  # Should now be completed


def test_toggle_task_completion_twice(client: TestClient, session: Session):
    """Test toggling task completion twice (incomplete -> complete -> incomplete)"""
    # Create a user and task
    user = User(
        id=uuid4(),
        email="test@example.com",
        hashed_password="fake_hashed_password",
        first_name="Test",
        last_name="User"
    )
    session.add(user)
    session.commit()
    
    task = Task(
        id=uuid4(),
        title="Test Task",
        description="Test Description",
        completed=False,  # Initially incomplete
        user_id=user.id
    )
    session.add(task)
    session.commit()
    
    # Mock the authentication to return our test user
    with patch('src.middleware.auth_middleware.verify_token', return_value={'sub': str(user.id)}):
        # First toggle: incomplete -> complete
        response = client.patch(
            f"/api/users/{user.id}/tasks/{task.id}/complete",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True  # Now complete
        
        # Second toggle: complete -> incomplete
        response = client.patch(
            f"/api/users/{user.id}/tasks/{task.id}/complete",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is False  # Now incomplete again


def test_toggle_nonexistent_task_fails(client: TestClient, session: Session):
    """Test toggling completion for a non-existent task"""
    # Create a user
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
        # Try to toggle completion for a non-existent task
        response = client.patch(
            f"/api/users/{user.id}/tasks/{uuid4()}/complete",  # Non-existent task ID
            headers={"Authorization": "Bearer fake_token"}
        )
        
        assert response.status_code == 404  # Not found


def test_update_task_completion_with_body(client: TestClient, session: Session):
    """Test updating task completion status with request body"""
    # Create a user and task
    user = User(
        id=uuid4(),
        email="test@example.com",
        hashed_password="fake_hashed_password",
        first_name="Test",
        last_name="User"
    )
    session.add(user)
    session.commit()
    
    task = Task(
        id=uuid4(),
        title="Test Task",
        description="Test Description",
        completed=False,  # Initially incomplete
        user_id=user.id
    )
    session.add(task)
    session.commit()
    
    # Mock the authentication to return our test user
    with patch('src.middleware.auth_middleware.verify_token', return_value={'sub': str(user.id)}):
        # Update the task completion status directly
        response = client.put(
            f"/api/users/{user.id}/tasks/{task.id}",
            json={
                "completed": True
            },
            headers={"Authorization": "Bearer fake_token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(task.id)
        assert data["completed"] is True  # Should now be completed