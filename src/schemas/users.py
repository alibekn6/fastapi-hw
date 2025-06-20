from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserGetSchema(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    username: str
    password: str
