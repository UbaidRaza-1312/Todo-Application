# Quickstart Guide: Console to Web Platform

**Feature**: 001-console-to-web-platform  
**Date**: 2026-01-11  
**Status**: Draft

## Overview

This quickstart guide provides instructions for setting up, running, and validating the multi-user task management web application. The application consists of a Next.js frontend and a FastAPI backend with Neon PostgreSQL database.

## Prerequisites

Before getting started, ensure you have the following installed:

- Node.js (version 18.x or higher)
- Python (version 3.11 or higher)
- pnpm (recommended) or npm/yarn
- PostgreSQL client tools (for database operations)
- Git

## Environment Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Dependencies

#### Frontend Dependencies
```bash
cd frontend
pnpm install
# or if using npm
npm install
```

#### Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Environment Variables

Create `.env` files in both frontend and backend directories with the following variables:

#### Frontend (.env.local)
```env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-super-secret-jwt-token-with-at-least-32-characters-long
BETTER_AUTH_TRUST_HOST=true
```

#### Backend (.env)
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app_db
BETTER_AUTH_SECRET=your-super-secret-jwt-token-with-at-least-32-characters-long
ACCESS_TOKEN_EXPIRE_MINUTES=30
SERVER_HOST=http://localhost:8000
```

## Database Setup

### 1. Set up Neon PostgreSQL

1. Create a Neon account at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string to your `.env` file

### 2. Run Database Migrations

```bash
cd backend
python -m src.db.migrate
```

This will create the necessary tables for users and tasks based on the data model.

## Running the Application

### 1. Start the Backend

```bash
cd backend
python -m src.main
```

The backend API will be available at `http://localhost:8000`.

### 2. Start the Frontend

In a new terminal:

```bash
cd frontend
pnpm dev
```

The frontend will be available at `http://localhost:3000`.

## API Endpoints

Once running, the backend provides the following user-scoped endpoints:

- `GET /api/{user_id}/tasks` - Retrieve all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task for a user
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a specific task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a specific task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion status

## Testing the Application

### 1. Automated Tests

#### Backend Tests
```bash
cd backend
pytest
```

#### Frontend Tests
```bash
cd frontend
pnpm test
```

### 2. Manual Testing Steps

1. Navigate to `http://localhost:3000`
2. Register a new user account
3. Log in with the new account
4. Create a new task
5. Verify the task appears in your task list
6. Update the task details
7. Mark the task as complete
8. Create another account in an incognito window
9. Verify the second user cannot see the first user's tasks

## Validation Checklist

Before considering the setup complete, verify:

- [ ] Backend server starts without errors
- [ ] Frontend server starts without errors
- [ ] Database connection is established
- [ ] User registration works
- [ ] User authentication works
- [ ] Task creation works
- [ ] Task retrieval works
- [ ] Task update works
- [ ] Task deletion works
- [ ] Task completion toggle works
- [ ] User data isolation is enforced (one user cannot see another's tasks)
- [ ] JWT authentication is required for all API endpoints

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify your Neon PostgreSQL connection string is correct
   - Ensure your database is running and accessible
   - Check that environment variables are properly set

2. **Authentication Issues**
   - Verify that `BETTER_AUTH_SECRET` is the same in both frontend and backend
   - Ensure JWT tokens are being properly passed in API requests

3. **API Connection Issues**
   - Check that backend is running on the expected port
   - Verify `NEXT_PUBLIC_API_BASE_URL` is set correctly in frontend environment

### Resetting the Database

To reset the database to a clean state:

```bash
cd backend
python -m src.db.reset
```

## Next Steps

1. Review the API documentation at `http://localhost:8000/docs`
2. Explore the data model in `specs/data-model.md`
3. Check the full API contracts in the `contracts/` directory
4. Review the security implementation in the authentication module