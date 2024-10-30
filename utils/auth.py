from fastapi import Depends
from typing import Annotated
from pydantic import BaseModel

from database.session import SessionDep
from utils.hash import hasher
from utils.db.client import get_email_and_password
from schemas.exception import IncorrectPasswordException


class AuthScheme(BaseModel):
    is_new: bool
    email: str
    password: str


class APIAuthentication:
    async def __call__(
        self, email: str, password: str, session: SessionDep
    ) -> AuthScheme:
        result = await get_email_and_password(email, session)
        if result:
            email, user_password = result[0]
            if not hasher.verify_password(password, user_password):
                raise IncorrectPasswordException
            return AuthScheme(is_new=False, password=password, email=email)

        return AuthScheme(is_new=True, password=password, email=email)


schema = APIAuthentication()

Auth = Annotated[APIAuthentication, Depends(schema)]
