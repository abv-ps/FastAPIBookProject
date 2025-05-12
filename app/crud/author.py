from fastapi import BackgroundTasks
from app.models.author import Author
from app.crud.items import get_item, delete_item, list_items, update_item, send_notification
from app.db.session import async_session

async def create_author(author: Author, background_tasks: BackgroundTasks):
    async with async_session() as session:
        session.add(author)
        await session.commit()
        await session.refresh(author)
    background_tasks.add_task(send_notification, Author, author.author_name, author.author_id)
    return author

async def list_authors():
    return await list_items(Author)

async def get_author(item_id: int):
    return await get_item(Author, item_id)

async def delete_author(item_id: int):
    await delete_item(Author, item_id)

async def update_author(item_id: int, update_data: dict):
    return await update_item(Author, item_id, update_data)
