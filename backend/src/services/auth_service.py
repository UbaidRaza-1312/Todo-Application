from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from typing import Optional
from datetime import timedelta
from ..models.user import User, UserBase
from ..utils.auth import verify_password, get_password_hash, create_access_token
from uuid import UUID
from ..utils.logging import log_info, log_error

class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password"""
        try:
            log_info(f"Authenticating user with email: {email}")
            statement = select(User).where(User.email == email)
            result = await self.session.execute(statement)
            user = result.scalar_one_or_none()

            if not user or not verify_password(password, user.hashed_password):
                log_info(f"Authentication failed for email: {email}")
                return None

            log_info(f"Authentication successful for user: {user.id}")
            return user
        except Exception as e:
            log_error(f"Error authenticating user with email {email}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred during authentication"
            )

    async def create_user(self, user_data: UserBase, password: str) -> User:
        """Create a new user with hashed password"""
        try:
            log_info(f"Creating new user with email: {user_data.email}")
            hashed_password = get_password_hash(password)
            db_user = User(
                email=user_data.email,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                hashed_password=hashed_password
            )
            self.session.add(db_user)
            await self.session.commit()
            await self.session.refresh(db_user)
            log_info(f"User created successfully: {db_user.id}")
            return db_user
        except Exception as e:
            log_error(f"Error creating user with email {user_data.email}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the user"
            )

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        try:
            log_info(f"Retrieving user by email: {email}")
            statement = select(User).where(User.email == email)
            result = await self.session.execute(statement)
            user = result.scalar_one_or_none()
            if user:
                log_info(f"User found by email: {email}")
            else:
                log_info(f"No user found by email: {email}")
            return user
        except Exception as e:
            log_error(f"Error retrieving user by email {email}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while retrieving the user"
            )

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get a user by ID"""
        try:
            log_info(f"Retrieving user by ID: {user_id}")
            statement = select(User).where(User.id == user_id)
            result = await self.session.execute(statement)
            user = result.scalar_one_or_none()
            if user:
                log_info(f"User found by ID: {user_id}")
            else:
                log_info(f"No user found by ID: {user_id}")
            return user
        except Exception as e:
            log_error(f"Error retrieving user by ID {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while retrieving the user"
            )

    async def create_access_token_for_user(self, user: User) -> str:
        """Create an access token for a user"""
        try:
            log_info(f"Creating access token for user: {user.id}")
            data = {"sub": str(user.id), "email": user.email}
            token = create_access_token(
                data=data,
                expires_delta=timedelta(minutes=30)
            )
            log_info(f"Access token created for user: {user.id}")
            return token
        except Exception as e:
            log_error(f"Error creating access token for user {user.id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the access token"
            )

