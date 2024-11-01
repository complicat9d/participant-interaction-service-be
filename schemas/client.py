from enum import Enum
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class ClientCreationSchema(BaseModel):
    pfp: Optional[str] = None
    gender: Optional[Gender] = None
    first_name: str
    last_name: str
    email: str
    password: str
    latitude: float
    longitude: float
    registration_date: datetime


class ClientSchema(ClientCreationSchema):
    id: int
