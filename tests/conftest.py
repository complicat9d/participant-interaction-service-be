import asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from config import settings as st
from database.session import DATABASE_URL
from database.models import Base


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


def check_test_db():
    if (
        st.POSTGRES_HOST not in ("localhost", "127.0.0.1", "postgres")
        or "amazonaws" in st.POSTGRES_HOST
        or st.POSTGRES_DB != "test"
    ):
        print(DATABASE_URL)
        raise Exception("Use local database only!")


@pytest.fixture(scope="function")
async def engine():
    check_test_db()

    e = create_async_engine(DATABASE_URL, echo=False, max_overflow=25)

    try:
        async with e.begin() as con:
            await con.run_sync(Base.metadata.create_all)

        yield e
    finally:
        async with e.begin() as con:
            await con.run_sync(Base.metadata.drop_all)
