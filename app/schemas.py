from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional, List, Tuple, Dict


class CreateUser(BaseModel):
    email: EmailStr
    password: str


# Response model for users
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Schema/Pydantic BaseModel defines the structure of request and response
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # optional. Default: True


class CreatePost(PostBase):
    pass


# Response model for posts
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    votes_count: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(
        le=1
    )  # direction of a vote (less than or equal to 1). 1 - add a vote, 0 - remove added vote
