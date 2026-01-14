from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
import os
from contextlib import asynccontextmanager

# Get database URL from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./todo_app.db")

# Create async engine
# For SQLite, we need to handle the URL differently
if DATABASE_URL.startswith("postgresql"):
    engine = create_async_engine(DATABASE_URL)
else:
    # For SQLite, we need to ensure proper format and add query parameters for async operations
    if "sqlite+aiosqlite://" in DATABASE_URL:
        # Ensure proper SQLite URL format for aiosqlite
        engine = create_async_engine(DATABASE_URL, echo=True)
    else:
        engine = create_async_engine(DATABASE_URL, echo=True)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

async def create_db_and_tables():
    """Create database tables"""
    from ..models.user import User  # noqa: F401
    from ..models.task import Task  # noqa: F401
    
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session"""
    async with AsyncSessionLocal() as session:
        yield session