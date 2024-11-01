from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str


class TokenData(BaseModel):
    sub: int
    iat: int
    exp: int
