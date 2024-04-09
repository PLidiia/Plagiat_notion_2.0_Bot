from sqlalchemy import select, BigInteger

from database.models import User, Task
from database.models import async_session


async def set_user(tg_id: BigInteger) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
            return False
        return True


async def add_task(tg_id: BigInteger, name: str, description='') -> None:
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.name == name))
        if not task:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            id = user.id
            session.add(Task(owner=id, name=name, description=description))
            await session.commit()
