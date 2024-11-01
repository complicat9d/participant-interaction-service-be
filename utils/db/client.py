import sqlalchemy as sa
from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Any, Sequence

import database.models as m
from schemas import ClientCreationSchema, ClientSchema
from schemas.exception import IncorrectEmailFormatException
from utils.email_verification import is_valid_email


async def create_client(request: ClientCreationSchema, session: AsyncSession) -> int:
    if not is_valid_email(request.email):
        raise IncorrectEmailFormatException

    q = (
        sa.insert(m.Client)
        .values(
            {
                m.Client.pfp: request.pfp,
                m.Client.gender: request.gender,
                m.Client.first_name: request.first_name,
                m.Client.last_name: request.last_name,
                m.Client.email: request.email,
                m.Client.password: request.password,
            }
        )
        .returning(m.Client.id)
    )

    client_id = (await session.execute(q)).scalar()

    return client_id


async def get_client(client_id: int, session: AsyncSession) -> ClientSchema:
    q = sa.select(m.Client.__table__).where(m.Client.id == client_id)
    entity = (await session.execute(q)).mappings().first()

    if entity:
        return ClientSchema(**entity)


async def get_client_by_email(email: str, session: AsyncSession) -> ClientSchema:
    q = sa.select(m.Client.__table__).where(m.Client.email == email)
    entity = (await session.execute(q)).mappings().first()

    if entity:
        return ClientSchema(**entity)


async def leave_reaction(client_id: int):
    pass
    # q = sa.select(sa.func.count(sa.and_(m.ClientMatch.my_email == m.)))
