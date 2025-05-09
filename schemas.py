from typing import List, Optional
from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str


class BookCreate(BookBase):
    author_ids: List[int]


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author_ids: Optional[List[int]] = None


class BookRead(BookBase):
    id: int
    authors: List[AuthorRead]

    class Config:
        orm_mode = True
