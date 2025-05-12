from fastapi import BackgroundTasks
from app.models.book import Book
from app.crud.items import get_item, delete_item, list_items, update_item, send_notification
from app.db.session import async_session

async def create_book(book: Book, background_tasks: BackgroundTasks):
    async with async_session() as session:
        session.add(book)
        await session.commit()
        await session.refresh(book)
    background_tasks.add_task(send_notification, Book, book.title, book.book_id)
    return book


async def list_books():
    return await list_items(Book)

async def get_book(item_id: int):
    return await get_item(Book, item_id)

async def delete_book(item_id: int):
    await delete_item(Book, item_id)

async def update_book(item_id: int, update_data: dict):
    return await update_item(Book, item_id, update_data)
