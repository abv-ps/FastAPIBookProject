from sqlalchemy import select

from app.db.session import async_session
from app.models.author import Author

async def create_author(author: Author):
    async with async_session() as session:
        session.add(author)
        await session.commit()
        await session.refresh(author)

    return author

async def list_authors():
    async with async_session() as session:
        authors = await session.execute(select(Author))
        return authors.scalars().all()
