from enum import Enum
from typing import Optional
from pydantic import BaseModel


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


class ClientSchema(ClientCreationSchema):
    id: int
