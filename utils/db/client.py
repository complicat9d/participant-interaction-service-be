import sqlalchemy as sa
from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Any, Sequence

import database.models as m
from schemas import ClientCreationSchema, ClientSchema
from schemas.exception import IncorrectEmailFormatException
from utils.email_verification import is_valid_email


async def create_client(request: ClientCreationSchema, session: AsyncSession):
    if not is_valid_email(request.email):
        raise IncorrectEmailFormatException

    q = sa.insert(m.Client).values(
        {
            m.Client.pfp: request.pfp,
            m.Client.gender: request.gender,
            m.Client.first_name: request.first_name,
            m.Client.last_name: request.last_name,
            m.Client.email: request.email,
            m.Client.password: request.password,
        }
    )

    await session.execute(q)


async def get_email_and_password(
    email: str, session: AsyncSession
) -> Sequence[Row[tuple[Any, Any]]]:
    q = sa.select(m.Client.email, m.Client.password).where(m.Client.email == email)
    return (await session.execute(q)).fetchall()


async def get_client(email: str, session: AsyncSession) -> Optional[ClientSchema]:
    q = sa.select(m.Client.__table__).where(m.Client.email == email)
    entity = (await session.execute(q)).mappings().first()

    if entity:
        return ClientSchema(**entity)
