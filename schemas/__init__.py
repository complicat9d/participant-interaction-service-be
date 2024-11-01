from .client import Gender, ClientSchema, ClientCreationSchema

from enum import Enum


class SortType(str, Enum):
    ASC = "asc"
    DESC = "desc"
