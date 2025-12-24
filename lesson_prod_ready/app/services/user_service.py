from app.domain.models import User
from app.domain.unit_of_work import UnitOfWork


class UserService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def ensure_user(
        self, telegram_id: int, username: str | None, full_name: str | None
    ) -> User:
        existing = await self.uow.users.get_by_telegram_id(telegram_id)
        if existing:
            return existing

        user = User(
            telegram_id=telegram_id,
            username=username,
            full_name=full_name,
        )
        await self.uow.users.add(user)
        return user
