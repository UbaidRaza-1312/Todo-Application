from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional, List
from ..db.database import get_async_session
from ..models.task import Task, TaskBase
from ..services.task_service import TaskService
from ..middleware.auth_middleware import get_current_user_id
from pydantic import BaseModel
from uuid import UUID
import uuid

router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: int = 1

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[str] = None
    priority: Optional[int] = None

class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str]
    completed: bool
    user_id: uuid.UUID
    created_at: str
    updated_at: str
    due_date: Optional[str]
    priority: int

@router.get("/users/{user_id}/tasks", response_model=List[TaskResponse])
async def get_tasks(
    user_id: UUID,
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    current_user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Get all tasks for a user, optionally filtered by completion status"""
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )
    
    async with session.begin():
        task_service = TaskService(session)
        tasks = await task_service.get_tasks_by_user(user_id, completed)
        
        return [
            TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                user_id=task.user_id,
                created_at=task.created_at.isoformat(),
                updated_at=task.updated_at.isoformat(),
                due_date=task.due_date.isoformat() if task.due_date else None,
                priority=task.priority
            ) for task in tasks
        ]

@router.post("/users/{user_id}/tasks", response_model=TaskResponse)
async def create_task(
    user_id: UUID,
    task_data: TaskCreate,
    current_user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Create a new task for a user"""
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )
    
    async with session.begin():
        task_service = TaskService(session)
        task_base = TaskBase(
            title=task_data.title,
            description=task_data.description,
            user_id=user_id,
            due_date=task_data.due_date,
            priority=task_data.priority
        )
        new_task = await task_service.create_task(task_base, user_id)
        
        return TaskResponse(
            id=new_task.id,
            title=new_task.title,
            description=new_task.description,
            completed=new_task.completed,
            user_id=new_task.user_id,
            created_at=new_task.created_at.isoformat(),
            updated_at=new_task.updated_at.isoformat(),
            due_date=new_task.due_date.isoformat() if new_task.due_date else None,
            priority=new_task.priority
        )

@router.get("/users/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: UUID,
    task_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Get a specific task for a user"""
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )
    
    async with session.begin():
        task_service = TaskService(session)
        task = await task_service.get_task_by_id(task_id, user_id)
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat(),
            due_date=task.due_date.isoformat() if task.due_date else None,
            priority=task.priority
        )

@router.put("/users/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: UUID,
    task_id: UUID,
    task_data: TaskUpdate,
    current_user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Update a specific task for a user"""
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )
    
    async with session.begin():
        task_service = TaskService(session)
        task_base = TaskBase(
            title=task_data.title or "",
            description=task_data.description,
            completed=task_data.completed,
            user_id=user_id,
            due_date=task_data.due_date,
            priority=task_data.priority or 1
        )
        updated_task = await task_service.update_task(task_id, task_base, user_id)
        
        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        return TaskResponse(
            id=updated_task.id,
            title=updated_task.title,
            description=updated_task.description,
            completed=updated_task.completed,
            user_id=updated_task.user_id,
            created_at=updated_task.created_at.isoformat(),
            updated_at=updated_task.updated_at.isoformat(),
            due_date=updated_task.due_date.isoformat() if updated_task.due_date else None,
            priority=updated_task.priority
        )

@router.delete("/users/{user_id}/tasks/{task_id}")
async def delete_task(
    user_id: UUID,
    task_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Delete a specific task for a user"""
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )
    
    async with session.begin():
        task_service = TaskService(session)
        success = await task_service.delete_task(task_id, user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        return {"message": "Task deleted successfully"}

@router.patch("/users/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    user_id: UUID,
    task_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Toggle the completion status of a task"""
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )
    
    async with session.begin():
        task_service = TaskService(session)
        task = await task_service.toggle_task_completion(task_id, user_id)
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat(),
            due_date=task.due_date.isoformat() if task.due_date else None,
            priority=task.priority
        )