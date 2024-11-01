import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_mail.errors import ConnectionErrors
from datetime import datetime

import database.models as m
from schemas import ClientCreationSchema, ClientSchema
from schemas.exception import (
    IncorrectEmailFormatException,
    ReactionsAmountExceededException,
)
from utils.email_utils import is_valid_email, send_message
from utils.log import logger
from config import settings


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


async def leave_reaction(
    client: ClientSchema, liked_client_id: int, session: AsyncSession
):
    start_of_day = datetime.combine(datetime.now(), datetime.min.time())
    end_of_day = datetime.combine(datetime.now(), datetime.max.time())
    q = sa.select(
        sa.func.count(
            sa.and_(
                m.ClientMatch.client_id == client.id,
                m.ClientMatch.timestamp >= start_of_day,
                m.ClientMatch.timestamp <= end_of_day,
            )
        )
    )
    amount = (await session.execute(q)).scalar()

    if amount >= settings.REACTIONS_LIMIT:
        raise ReactionsAmountExceededException

    q = sa.insert(m.ClientMatch).values(
        {
            m.ClientMatch.client_id: client.id,
            m.ClientMatch.liked_client_id: liked_client_id,
        }
    )

    await session.execute(q)

    q = sa.select(
        sa.exists().where(
            sa.and_(
                m.ClientMatch.client_id == liked_client_id,
                m.ClientMatch.liked_client_id == client.id,
            )
        )
    )
    exists = (await session.execute(q)).scalar()
    if exists:
        q = sa.select(m.Client.__table__).where(m.Client.id == liked_client_id)
        entity = (await session.execute(q)).mappings().first()
        if entity is not None:
            recipient = ClientSchema(**entity)
            fullname = client.first_name + (
                " " + client.last_name if client.last_name else ""
            )
            try:
                await send_message(
                    client,
                    recipient,
                    "Вы понравились {}! Почта у участника：{}".format(
                        fullname, client.email
                    ),
                )
            except ConnectionErrors as e:
                logger.error(
                    "There was an error with servers while sending mail from {} to {}. Error: {}".format(
                        client.email, recipient.email, e
                    )
                )
