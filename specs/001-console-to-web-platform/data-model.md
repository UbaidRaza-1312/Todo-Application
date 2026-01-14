# Data Model: Console to Web Platform

**Feature**: 001-console-to-web-platform  
**Date**: 2026-01-11  
**Status**: Completed

## Overview

This document defines the data model for the multi-user task management web application. The model includes entities for users and tasks with appropriate relationships and constraints to ensure data integrity and user isolation.

## Entity Definitions

### User Entity

**Description**: Represents a registered user in the system

**Fields**:
- `id` (UUID, Primary Key): Unique identifier for the user
- `email` (String, Unique, Not Null): User's email address for login
- `hashed_password` (String, Not Null): BCrypt hashed password
- `first_name` (String): User's first name
- `last_name` (String): User's last name
- `created_at` (DateTime, Not Null): Timestamp of account creation
- `updated_at` (DateTime, Not Null): Timestamp of last update
- `is_active` (Boolean, Default: True): Account active status
- `email_verified` (Boolean, Default: False): Email verification status

**Constraints**:
- Email must be unique across all users
- Email must follow standard email format
- Password must meet minimum security requirements (8+ characters)
- Created and updated timestamps are automatically managed

**Relationships**:
- One-to-Many: A user can have many tasks

### Task Entity

**Description**: Represents a task item owned by a specific user

**Fields**:
- `id` (UUID, Primary Key): Unique identifier for the task
- `title` (String, Not Null): Task title (max 200 characters)
- `description` (Text): Detailed task description (optional)
- `completed` (Boolean, Default: False): Completion status
- `user_id` (UUID, Foreign Key, Not Null): Reference to owning user
- `created_at` (DateTime, Not Null): Timestamp of task creation
- `updated_at` (DateTime, Not Null): Timestamp of last update
- `due_date` (DateTime): Optional due date for the task
- `priority` (Integer, Default: 1): Priority level (1-5, 1 being lowest)

**Constraints**:
- Title must not be empty
- User ID must reference an existing user
- Priority must be between 1 and 5
- Due date must be in the future if provided

**Relationships**:
- Many-to-One: A task belongs to one user (via user_id foreign key)

## Database Schema

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE NOT NULL
);

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    due_date TIMESTAMP WITH TIME ZONE,
    priority INTEGER DEFAULT 1 NOT NULL CHECK (priority >= 1 AND priority <= 5)
);

-- Indexes for performance
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_priority ON tasks(priority);
```

## Validation Rules

### User Validation
- Email format: Must match standard email regex pattern
- Password strength: Minimum 8 characters, with at least one uppercase, one lowercase, and one number
- Name fields: Maximum 100 characters each
- Unique constraint: Email must be unique across all users

### Task Validation
- Title: Required, maximum 200 characters, minimum 1 character
- Description: Optional, maximum 1000 characters
- User ownership: Task must belong to an existing user
- Priority: Must be an integer between 1 and 5
- Due date: If provided, must be in the future

## State Transitions

### Task State Transitions
- `incomplete` → `completed`: When user marks task as complete
- `completed` → `incomplete`: When user unmarks task as complete

**Transition Rules**:
- Only the task owner can change the completion status
- Updated timestamp is automatically updated on any change

## Relationships and Constraints

### Referential Integrity
- Tasks are deleted when their owning user is deleted (CASCADE DELETE)
- Attempting to create a task for a non-existent user will fail

### Data Isolation
- All queries must be scoped by user ID to ensure data isolation
- Users cannot access tasks owned by other users
- API endpoints require user authentication and enforce user ID matching

## API Data Contracts

### User Data Contract
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "is_active": true,
  "email_verified": true
}
```

### Task Data Contract
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "user_id": "uuid-string",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "due_date": "2023-01-01T00:00:00Z",
  "priority": 3
}
```

## Security Considerations

### Data Access
- All data access must be filtered by authenticated user ID
- Direct database access should enforce user ID constraints
- API responses should not expose other users' data

### Data Encryption
- Sensitive data (passwords) must be encrypted using industry-standard algorithms
- Communication between services must use TLS encryption
- Database connections must use encrypted transport

## Performance Considerations

### Indexing Strategy
- Primary keys are automatically indexed
- Foreign keys (user_id) are indexed for join performance
- Frequently queried fields (completed, due_date, priority) are indexed
- Email field is indexed due to uniqueness constraint

### Query Optimization
- All queries should include user_id in WHERE clause for partitioning
- Pagination should be implemented for large result sets
- Consider caching frequently accessed user data