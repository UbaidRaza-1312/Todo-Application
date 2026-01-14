# API Contract: Task Management Endpoints

**Feature**: 001-console-to-web-platform  
**Date**: 2026-01-11  
**Version**: 1.0  
**Status**: Draft

## Overview

This document defines the API contract for the task management functionality in the multi-user web platform. All endpoints require JWT authentication and enforce user data isolation.

## Authentication

All endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <JWT_TOKEN>
```

The token must contain the user ID which is used to enforce data isolation.

## Base URL

```
http://localhost:8000/api/{user_id}/
```

## Common Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional message"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "details": "Optional details"
}
```

## Endpoints

### 1. List User Tasks

**Endpoint**: `GET /tasks`

**Description**: Retrieve all tasks belonging to the authenticated user

**Authentication**: Required

**Path Parameters**:
- `user_id`: The ID of the user whose tasks to retrieve (from JWT)

**Query Parameters**:
- `completed` (optional): Filter by completion status (true/false)
- `limit` (optional): Number of tasks to return (default: 50, max: 100)
- `offset` (optional): Number of tasks to skip (for pagination)

**Response**:
```json
{
  "success": true,
  "data": [
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
  ],
  "message": "Tasks retrieved successfully"
}
```

**Status Codes**:
- 200: Success
- 401: Unauthorized
- 403: Forbidden (trying to access another user's tasks)
- 500: Internal server error

### 2. Create Task

**Endpoint**: `POST /tasks`

**Description**: Create a new task for the authenticated user

**Authentication**: Required

**Path Parameters**:
- `user_id`: The ID of the user creating the task (from JWT)

**Request Body**:
```json
{
  "title": "Task title (required)",
  "description": "Task description (optional)",
  "due_date": "2023-12-31T23:59:59Z (optional)",
  "priority": 3 (optional, default: 1)
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "uuid-string",
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "user_id": "uuid-string",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "due_date": "2023-01-01T00:00:00Z",
    "priority": 3
  },
  "message": "Task created successfully"
}
```

**Status Codes**:
- 201: Created
- 400: Bad request (invalid input)
- 401: Unauthorized
- 403: Forbidden (trying to create task for another user)
- 500: Internal server error

### 3. Get Task Details

**Endpoint**: `GET /tasks/{task_id}`

**Description**: Retrieve details of a specific task

**Authentication**: Required

**Path Parameters**:
- `user_id`: The ID of the user (from JWT)
- `task_id`: The ID of the task to retrieve

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "uuid-string",
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "user_id": "uuid-string",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "due_date": "2023-01-01T00:00:00Z",
    "priority": 3
  },
  "message": "Task retrieved successfully"
}
```

**Status Codes**:
- 200: Success
- 401: Unauthorized
- 403: Forbidden (trying to access another user's task)
- 404: Task not found
- 500: Internal server error

### 4. Update Task

**Endpoint**: `PUT /tasks/{task_id}`

**Description**: Update details of a specific task

**Authentication**: Required

**Path Parameters**:
- `user_id`: The ID of the user (from JWT)
- `task_id`: The ID of the task to update

**Request Body**:
```json
{
  "title": "Updated task title (optional)",
  "description": "Updated task description (optional)",
  "due_date": "2023-12-31T23:59:59Z (optional)",
  "priority": 4 (optional)
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "uuid-string",
    "title": "Updated task title",
    "description": "Updated task description",
    "completed": false,
    "user_id": "uuid-string",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "due_date": "2023-01-01T00:00:00Z",
    "priority": 4
  },
  "message": "Task updated successfully"
}
```

**Status Codes**:
- 200: Success
- 400: Bad request (invalid input)
- 401: Unauthorized
- 403: Forbidden (trying to update another user's task)
- 404: Task not found
- 500: Internal server error

### 5. Delete Task

**Endpoint**: `DELETE /tasks/{task_id}`

**Description**: Delete a specific task

**Authentication**: Required

**Path Parameters**:
- `user_id`: The ID of the user (from JWT)
- `task_id`: The ID of the task to delete

**Response**:
```json
{
  "success": true,
  "data": null,
  "message": "Task deleted successfully"
}
```

**Status Codes**:
- 200: Success
- 401: Unauthorized
- 403: Forbidden (trying to delete another user's task)
- 404: Task not found
- 500: Internal server error

### 6. Toggle Task Completion

**Endpoint**: `PATCH /tasks/{task_id}/complete`

**Description**: Toggle the completion status of a specific task

**Authentication**: Required

**Path Parameters**:
- `user_id`: The ID of the user (from JWT)
- `task_id`: The ID of the task to update

**Request Body**:
```json
{
  "completed": true (optional - if omitted, toggles current status)
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "uuid-string",
    "title": "Task title",
    "description": "Task description",
    "completed": true,
    "user_id": "uuid-string",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "due_date": "2023-01-01T00:00:00Z",
    "priority": 3
  },
  "message": "Task completion status updated successfully"
}
```

**Status Codes**:
- 200: Success
- 400: Bad request (invalid input)
- 401: Unauthorized
- 403: Forbidden (trying to update another user's task)
- 404: Task not found
- 500: Internal server error

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| 400 | Validation Error | Request body failed validation |
| 401 | Unauthorized | Missing or invalid JWT token |
| 403 | Forbidden | User trying to access another user's data |
| 404 | Not Found | Requested resource does not exist |
| 409 | Conflict | Request conflicts with current state |
| 500 | Internal Server Error | Unexpected server error |

## Security Considerations

1. All endpoints require JWT authentication
2. User ID from JWT is validated against path parameter
3. All data access is scoped by user ID
4. Input validation is performed on all request bodies
5. SQL injection protection is implemented via parameterized queries