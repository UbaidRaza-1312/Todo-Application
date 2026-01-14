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


def test_task_completion_journey(client: TestClient, session: Session):
    """Test the complete task completion journey"""
    # Create a user
    user = User(
        id=uuid4(),
        email="completion@example.com",
        hashed_password="fake_hashed_password",
        first_name="Task",
        last_name="Completion"
    )
    session.add(user)
    session.commit()
    
    # Mock the authentication to return our test user
    with patch('src.middleware.auth_middleware.verify_token', return_value={'sub': str(user.id)}):
        # Step 1: Create a task
        response = client.post(
            f"/api/users/{user.id}/tasks",
            json={
                "title": "Completion Journey Task",
                "description": "Task for testing completion journey",
                "priority": 2
            },
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        task_data = response.json()
        task_id = task_data["id"]
        assert task_data["title"] == "Completion Journey Task"
        assert task_data["completed"] is False  # Should start as incomplete
        
        # Step 2: Verify the task is initially incomplete
        response = client.get(
            f"/api/users/{user.id}/tasks/{task_id}",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        retrieved_task = response.json()
        assert retrieved_task["completed"] is False
        
        # Step 3: Toggle completion status to complete
        response = client.patch(
            f"/api/users/{user.id}/tasks/{task_id}/complete",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["id"] == task_id
        assert updated_task["completed"] is True  # Should now be complete
        
        # Step 4: List tasks and filter by completion status (should appear in completed list)
        response = client.get(
            f"/api/users/{user.id}/tasks?completed=true",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        completed_tasks = response.json()
        assert len(completed_tasks) == 1
        assert completed_tasks[0]["id"] == task_id
        assert completed_tasks[0]["completed"] is True
        
        # Step 5: List tasks and filter by incomplete status (should not appear)
        response = client.get(
            f"/api/users/{user.id}/tasks?completed=false",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        incomplete_tasks = response.json()
        assert len(incomplete_tasks) == 0  # Task is now complete, so shouldn't appear here
        
        # Step 6: Toggle completion status back to incomplete
        response = client.patch(
            f"/api/users/{user.id}/tasks/{task_id}/complete",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["id"] == task_id
        assert updated_task["completed"] is False  # Should now be incomplete again
        
        # Step 7: Verify it now appears in incomplete list
        response = client.get(
            f"/api/users/{user.id}/tasks?completed=false",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        incomplete_tasks = response.json()
        assert len(incomplete_tasks) == 1
        assert incomplete_tasks[0]["id"] == task_id
        assert incomplete_tasks[0]["completed"] is False


def test_multiple_tasks_completion_tracking(client: TestClient, session: Session):
    """Test completion tracking with multiple tasks"""
    # Create a user
    user = User(
        id=uuid4(),
        email="multi-completion@example.com",
        hashed_password="fake_hashed_password",
        first_name="Multi",
        last_name="Completion"
    )
    session.add(user)
    session.commit()
    
    # Mock the authentication to return our test user
    with patch('src.middleware.auth_middleware.verify_token', return_value={'sub': str(user.id)}):
        # Create multiple tasks
        tasks = []
        for i in range(3):
            response = client.post(
                f"/api/users/{user.id}/tasks",
                json={
                    "title": f"Task {i+1}",
                    "description": f"Task {i+1} for multi-completion test",
                    "priority": 1
                },
                headers={"Authorization": "Bearer fake_token"}
            )
            assert response.status_code == 200
            task_data = response.json()
            tasks.append(task_data["id"])
        
        # Verify all tasks are initially incomplete
        response = client.get(
            f"/api/users/{user.id}/tasks?completed=false",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        all_tasks = response.json()
        assert len(all_tasks) == 3
        
        # Complete the first two tasks
        for i in range(2):
            response = client.patch(
                f"/api/users/{user.id}/tasks/{tasks[i]}/complete",
                headers={"Authorization": "Bearer fake_token"}
            )
            assert response.status_code == 200
            updated_task = response.json()
            assert updated_task["completed"] is True
        
        # Verify that 2 tasks are completed and 1 is incomplete
        response = client.get(
            f"/api/users/{user.id}/tasks?completed=true",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        completed_tasks = response.json()
        assert len(completed_tasks) == 2
        
        response = client.get(
            f"/api/users/{user.id}/tasks?completed=false",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        incomplete_tasks = response.json()
        assert len(incomplete_tasks) == 1


def test_completion_respects_user_isolation(client: TestClient, session: Session):
    """Test that task completion respects user data isolation"""
    # Create two users
    user1 = User(
        id=uuid4(),
        email="completion1@example.com",
        hashed_password="fake_hashed_password",
        first_name="Completion",
        last_name="User1"
    )
    user2 = User(
        id=uuid4(),
        email="completion2@example.com",
        hashed_password="fake_hashed_password",
        first_name="Completion",
        last_name="User2"
    )
    session.add(user1)
    session.add(user2)
    session.commit()
    
    # Create a task for user1
    task = Task(
        id=uuid4(),
        title="User1's Task",
        description="Task that belongs to user1",
        completed=False,
        user_id=user1.id
    )
    session.add(task)
    session.commit()
    
    # Mock the authentication to return user1's ID
    with patch('src.middleware.auth_middleware.verify_token', return_value={'sub': str(user1.id)}):
        # User1 should be able to toggle their own task
        response = client.patch(
            f"/api/users/{user1.id}/tasks/{task.id}/complete",  # Accessing own task
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["completed"] is True
    
    # Now try to access the same task as user2 (should fail)
    with patch('src.middleware.auth_middleware.verify_token', return_value={'sub': str(user2.id)}):
        response = client.patch(
            f"/api/users/{user1.id}/tasks/{task.id}/complete",  # Trying to access user1's task
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 403  # Forbidden - user2 can't access user1's task