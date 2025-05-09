from sqlmodel import SQLModel, Field, Relationship

from app.models.author import Author, AuthorBookLink


class Book(SQLModel, table=True):
    __tablename__ = 'books'
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str|None = None

    owners: Author = Relationship(back_populates="items", link_model=AuthorBookLink)
