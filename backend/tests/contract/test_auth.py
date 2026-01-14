import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from uuid import uuid4
from passlib.context import CryptContext

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


def test_register_new_user_success(client: TestClient, session: Session):
    """Test successful user registration"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "SecurePassword123!",
            "first_name": "New",
            "last_name": "User"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["first_name"] == "New"
    assert data["last_name"] == "User"
    # Verify that the user was actually created in the database
    user_in_db = session.get(User, data["id"])
    assert user_in_db is not None
    assert user_in_db.email == "newuser@example.com"


def test_register_duplicate_email_fails(client: TestClient, session: Session):
    """Test that registering with an existing email fails"""
    # Create a user first
    existing_user = User(
        id=uuid4(),
        email="existing@example.com",
        hashed_password=pwd_context.hash("password123"),
        first_name="Existing",
        last_name="User"
    )
    session.add(existing_user)
    session.commit()
    
    # Try to register with the same email
    response = client.post(
        "/api/auth/register",
        json={
            "email": "existing@example.com",  # Same email as existing user
            "password": "AnotherPassword123!",
            "first_name": "Another",
            "last_name": "User"
        }
    )
    
    assert response.status_code == 400  # Bad request
    data = response.json()
    assert "detail" in data
    assert "already registered" in data["detail"].lower()


def test_login_valid_credentials(client: TestClient, session: Session):
    """Test successful login with valid credentials"""
    # Create a user in the database
    hashed_password = pwd_context.hash("ValidPassword123!")
    user = User(
        id=uuid4(),
        email="loginuser@example.com",
        hashed_password=hashed_password,
        first_name="Login",
        last_name="User"
    )
    session.add(user)
    session.commit()
    
    response = client.post(
        "/api/auth/login",
        json={
            "email": "loginuser@example.com",
            "password": "ValidPassword123!"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient, session: Session):
    """Test login failure with invalid credentials"""
    # Create a user in the database
    hashed_password = pwd_context.hash("CorrectPassword123!")
    user = User(
        id=uuid4(),
        email="wronglogin@example.com",
        hashed_password=hashed_password,
        first_name="Wrong",
        last_name="Login"
    )
    session.add(user)
    session.commit()
    
    # Try to login with wrong password
    response = client.post(
        "/api/auth/login",
        json={
            "email": "wronglogin@example.com",
            "password": "WrongPassword123!"  # Wrong password
        }
    )
    
    assert response.status_code == 401  # Unauthorized


def test_login_nonexistent_user(client: TestClient, session: Session):
    """Test login failure with nonexistent user"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "AnyPassword123!"
        }
    )
    
    assert response.status_code == 401  # Unauthorized