import sqlalchemy as sa

from database.models import Base
from schemas import Gender


class Client(Base):
    __tablename__ = "client"

    email = sa.Column(sa.String, primary_key=True)
    password = sa.Column(sa.String, nullable=False)
    pfp = sa.Column(sa.String, nullable=True)
    gender: Gender = sa.Column(sa.String, server_default=Gender.PREFER_NOT_TO_SAY)
    first_name = sa.Column(sa.String, nullable=False)
    last_name = sa.Column(sa.String, nullable=False)
