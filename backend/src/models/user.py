from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = Field(default=True)
    email_verified: bool = Field(default=False)

class User(UserBase, table=True):
    """
    User model representing a registered user in the system
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    )

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "select"})