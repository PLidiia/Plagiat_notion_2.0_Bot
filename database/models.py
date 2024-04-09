from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
async_session = async_sessionmaker(engine)


class SqlalchemyBase(AsyncAttrs, DeclarativeBase):
    pass


class User(SqlalchemyBase):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class Task(SqlalchemyBase):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    owner: Mapped[int] = mapped_column(ForeignKey('users.id'))
    description: Mapped[str] = mapped_column()


async def create_tables():
    async with engine.begin() as con:
        await con.run_sync(SqlalchemyBase.metadata.create_all)
