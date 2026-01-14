# Todo App Backend

This is the backend for the multi-user task management application. It provides a secure API for managing tasks with JWT-based authentication.

## Tech Stack

- Python 3.8+
- FastAPI
- SQLModel
- PostgreSQL
- JWT Authentication

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and secret key
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## API Endpoints

The API provides the following endpoints:

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info
- `GET /api/users/{user_id}/tasks` - Get user's tasks
- `POST /api/users/{user_id}/tasks` - Create a new task
- `GET /api/users/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/users/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/users/{user_id}/tasks/{task_id}` - Delete a task
- `PATCH /api/users/{user_id}/tasks/{task_id}/complete` - Toggle task completion

## Authentication

All task-related endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

## Database Migrations

To create and run database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Migration message"

# Run migrations
alembic upgrade head
```