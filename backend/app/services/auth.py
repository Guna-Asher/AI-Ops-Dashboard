from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_password, get_password_hash
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import UserCreate

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def register(self, user_in: UserCreate) -> User:
        user = await self.user_repo.get_by_email(email=user_in.email)
        if user:
            raise ValueError("Email already registered")
        hashed = get_password_hash(user_in.password)
        user = await self.user_repo.create({
            "email": user_in.email,
            "full_name": user_in.full_name,
            "hashed_password": hashed,
        })
        return user

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        user = await self.user_repo.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.user_repo.get(user_id)