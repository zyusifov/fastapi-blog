from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str


class UserShow(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True

class AuthUser(BaseModel):
    email: str
    password: str

    class Config():
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None