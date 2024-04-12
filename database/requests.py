from typing import Union

from sqlalchemy import select, BigInteger

from database.models import User, Task
from database.models import async_session


async def set_user(tg_id: Union[BigInteger, int]) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
            return False
        return True


async def add_task_db(tg_id: Union[BigInteger, int], name: str, description='') -> None:
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.name == name))
        if not task:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            id = user.id
            session.add(Task(owner=id, name=name, description=description))
            await session.commit()


async def show_tasks_db(tg_id: Union[BigInteger, int]):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        tasks = await session.scalars(select(Task).order_by(Task.name).where(Task.owner == user.id))
        await session.commit()
        return tasks
