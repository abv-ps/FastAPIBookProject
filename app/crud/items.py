from typing import Type, TypeVar, Optional, Any
from sqlmodel import SQLModel, select
from app.db.session import async_session

ModelType = TypeVar("ModelType", bound=SQLModel)


def send_notification(model: Type[SQLModel], item_name: str, item_id: int):
    print(
        f"{model.__name__} created: '{item_name}' (ID: {item_id}) → Notification sent."
    )


async def get_item(model: Type[ModelType], item_id: int) -> Optional[ModelType]:
    async with async_session() as session:
        return await session.get(model, item_id)


async def delete_item(model: Type[ModelType], item_id: int) -> None:
    async with async_session() as session:
        item = await session.get(model, item_id)
        if item:
            await session.delete(item)
            await session.commit()


async def list_items(model: Type[ModelType]) -> list[ModelType]:
    async with async_session() as session:
        result = await session.execute(select(model))
        return result.scalars().all()


async def update_item(model: Type[ModelType], item_id: int, update_data: dict[str, Any]) -> Optional[ModelType]:
    async with async_session() as session:
        db_item = await session.get(model, item_id)
        if db_item:
            for key, value in update_data.items():
                setattr(db_item, key, value)
            session.add(db_item)
            await session.commit()
            await session.refresh(db_item)
        return db_item


async def get_author_books(
        author_id: Optional[int] = None,
        author_ids: Optional[list[int]] = None
):
    async with async_session() as session:
        from app.models.book import Book
        from app.models.author import AuthorBookLink
        author_book_list = select(Book).join(AuthorBookLink, AuthorBookLink.author_id == author_id)

        if author_id is not None:
            author_book_list = author_book_list.where(AuthorBookLink.author_id == author_id)
        elif author_ids is not None:
            author_book_list = author_book_list.where(AuthorBookLink.author_id.in_(author_ids))

        result = await session.execute(author_book_list)
        return result.scalars().all()
