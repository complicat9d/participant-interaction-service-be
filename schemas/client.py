from enum import Enum
from pydantic import BaseModel


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"
