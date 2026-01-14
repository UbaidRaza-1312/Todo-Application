from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    due_date: Optional[datetime] = None
    priority: int = Field(default=1, ge=1, le=5)  # Priority from 1 to 5

class Task(TaskBase, table=True):
    """
    Task model representing a task item owned by a specific user
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    )

    # Relationship to user
    user: "User" = Relationship(back_populates="tasks", sa_relationship_kwargs={"lazy": "select"})