import sqlalchemy as sa

from database.models import Base
from schemas import Gender


class Client(Base):
    __tablename__ = "client"

    id = sa.Column(sa.Integer, primary_key=True)
    pfp = sa.Column(sa.String, nullable=True)
    gender: Gender = sa.Column(sa.String, server_default=Gender.PREFER_NOT_TO_SAY)
    first_name = sa.Column(sa.String, nullable=False)
    last_name = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, nullable=False, unique=True)
    # the check for email uniqueness for better intractability will be made at api level
    # by handling exception on the unique constraint
