import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from uuid import uuid4
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


def test_task_management_full_journey(client: TestClient, session: Session):
    """Test the complete task management user journey"""
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
        # Step 1: Create a task
        response = client.post(
            f"/api/users/{user.id}/tasks",
            json={
                "title": "Integration Test Task",
                "description": "This is an integration test task",
                "priority": 2
            },
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        task_data = response.json()
        task_id = task_data["id"]
        assert task_data["title"] == "Integration Test Task"
        assert task_data["description"] == "This is an integration test task"
        assert task_data["completed"] is False
        
        # Step 2: Get the task
        response = client.get(
            f"/api/users/{user.id}/tasks/{task_id}",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        retrieved_task = response.json()
        assert retrieved_task["id"] == task_id
        assert retrieved_task["title"] == "Integration Test Task"
        
        # Step 3: Update the task
        response = client.put(
            f"/api/users/{user.id}/tasks/{task_id}",
            json={
                "title": "Updated Integration Test Task",
                "description": "Updated description",
                "completed": True
            },
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["id"] == task_id
        assert updated_task["title"] == "Updated Integration Test Task"
        assert updated_task["completed"] is True
        
        # Step 4: List all tasks for the user
        response = client.get(
            f"/api/users/{user.id}/tasks",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        tasks_list = response.json()
        assert len(tasks_list) == 1
        assert tasks_list[0]["id"] == task_id
        assert tasks_list[0]["title"] == "Updated Integration Test Task"
        
        # Step 5: Toggle task completion status
        response = client.patch(
            f"/api/users/{user.id}/tasks/{task_id}/complete",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        toggled_task = response.json()
        assert toggled_task["id"] == task_id
        assert toggled_task["completed"] is False  # Should be toggled back to False
        
        # Step 6: Delete the task
        response = client.delete(
            f"/api/users/{user.id}/tasks/{task_id}",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        
        # Step 7: Verify the task is deleted
        response = client.get(
            f"/api/users/{user.id}/tasks/{task_id}",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 404


def test_user_data_isolation(client: TestClient, session: Session):
    """Test that users can only access their own tasks"""
    # Create two users
    user1 = User(
        id=uuid4(),
        email="user1@example.com",
        hashed_password="fake_hashed_password",
        first_name="User",
        last_name="One"
    )
    user2 = User(
        id=uuid4(),
        email="user2@example.com",
        hashed_password="fake_hashed_password",
        first_name="User",
        last_name="Two"
    )
    session.add(user1)
    session.add(user2)
    session.commit()
    
    # Mock the authentication to return user1
    with patch('src.middleware.auth_middleware.verify_token', return_value={'sub': str(user1.id)}):
        # Create a task for user1
        response = client.post(
            f"/api/users/{user1.id}/tasks",
            json={
                "title": "User1's Task",
                "description": "This belongs to user1",
                "priority": 1
            },
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        task_data = response.json()
        task_id = task_data["id"]
        assert task_data["title"] == "User1's Task"
    
    # Now try to access user1's task as user2 (should fail with 403)
    with patch('src.middleware.auth_middleware.verify_token', return_value={'sub': str(user2.id)}):
        response = client.get(
            f"/api/users/{user1.id}/tasks/{task_id}",  # Trying to access user1's task
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 403  # Forbidden