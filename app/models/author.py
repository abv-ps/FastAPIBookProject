from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlmodel import SQLModel, Field, Relationship

from app.models.book import Book


class AuthorBookLink(SQLModel, table=True):
    author_id: int = Field(foreign_key="author.id", primary_key=True)
    book_id: int = Field(foreign_key="book.id", primary_key=True)


class Author(SQLModel, table=True):
    __tablename__ = 'authors'
    id: int = Field(default=None, primary_key=True)
    name: str

    books: Book = Relationship(back_populates="owners", link_model=AuthorBookLink)



