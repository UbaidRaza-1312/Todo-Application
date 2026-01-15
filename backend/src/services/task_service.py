from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from typing import List, Optional
from uuid import UUID
from ..models.task import Task, TaskBase
from ..models.user import User
from ..utils.logging import log_info, log_error

class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, task_data: TaskBase, user_id: UUID) -> Task:
        """Create a new task for a user"""
        try:
            log_info(f"Creating task for user {user_id} with title '{task_data.title}'")
            db_task = Task(
                title=task_data.title,
                description=task_data.description,
                completed=task_data.completed,
                user_id=user_id,
                due_date=task_data.due_date,
                priority=task_data.priority
            )
            self.session.add(db_task)
            # Don't commit here as the caller handles the transaction
            await self.session.flush()  # Ensure the task gets an ID without committing
            log_info(f"Task {db_task.id} created successfully for user {user_id}")
            return db_task
        except Exception as e:
            log_error(f"Error creating task for user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the task"
            )

    async def get_tasks_by_user(self, user_id: UUID, completed: Optional[bool] = None) -> List[Task]:
        """Get all tasks for a specific user, optionally filtered by completion status"""
        try:
            log_info(f"Retrieving tasks for user {user_id}, completed={completed}")
            query = select(Task).where(Task.user_id == user_id)

            if completed is not None:
                query = query.where(Task.completed == completed)

            result = await self.session.execute(query)
            tasks = result.scalars().all()  # Use scalars() to get Task objects instead of Row objects
            log_info(f"Found {len(tasks)} tasks for user {user_id}")
            return tasks
        except Exception as e:
            log_error(f"Error retrieving tasks for user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while retrieving tasks"
            )

    async def get_task_by_id(self, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """Get a specific task by ID for a specific user"""
        try:
            log_info(f"Retrieving task {task_id} for user {user_id}")
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await self.session.execute(statement)
            task = result.scalar_one_or_none()  # Use scalar_one_or_none() to get a single Task object
            if task:
                log_info(f"Task {task_id} found for user {user_id}")
            else:
                log_info(f"Task {task_id} not found for user {user_id}")
            return task
        except Exception as e:
            log_error(f"Error retrieving task {task_id} for user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while retrieving the task"
            )

    async def update_task(self, task_id: UUID, task_data: TaskBase, user_id: UUID) -> Optional[Task]:
        """Update a specific task for a user"""
        try:
            log_info(f"Updating task {task_id} for user {user_id}")
            db_task = await self.get_task_by_id(task_id, user_id)
            if not db_task:
                log_error(f"Task {task_id} not found for user {user_id} during update")
                return None

            # Update task fields
            for field, value in task_data.dict(exclude_unset=True).items():
                setattr(db_task, field, value)

            self.session.add(db_task)
            # Don't commit here as the caller handles the transaction
            await self.session.flush()  # Ensure changes are applied without committing
            log_info(f"Task {task_id} updated successfully for user {user_id}")
            return db_task
        except Exception as e:
            log_error(f"Error updating task {task_id} for user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the task"
            )

    async def delete_task(self, task_id: UUID, user_id: UUID) -> bool:
        """Delete a specific task for a user"""
        try:
            log_info(f"Deleting task {task_id} for user {user_id}")
            db_task = await self.get_task_by_id(task_id, user_id)
            if not db_task:
                log_error(f"Task {task_id} not found for user {user_id} during deletion")
                return False

            await self.session.delete(db_task)
            # Don't commit here as the caller handles the transaction
            await self.session.flush()  # Ensure changes are applied without committing
            log_info(f"Task {task_id} deleted successfully for user {user_id}")
            return True
        except Exception as e:
            log_error(f"Error deleting task {task_id} for user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while deleting the task"
            )

    async def toggle_task_completion(self, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """Toggle the completion status of a task"""
        try:
            log_info(f"Toggling completion status for task {task_id} for user {user_id}")
            db_task = await self.get_task_by_id(task_id, user_id)
            if not db_task:
                log_error(f"Task {task_id} not found for user {user_id} during toggle completion")
                return None

            new_status = not db_task.completed
            db_task.completed = new_status
            self.session.add(db_task)
            # Don't commit here as the caller handles the transaction
            await self.session.flush()  # Ensure changes are applied without committing
            log_info(f"Task {task_id} completion status toggled to {new_status} for user {user_id}")
            return db_task
        except Exception as e:
            log_error(f"Error toggling completion status for task {task_id} for user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the task completion status"
            )