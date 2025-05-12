from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.crud.items import get_item, delete_item, list_items, update_item
from app.crud.book import create_book
from app.schemas.book import BookCreate, BookRead
from app.models.book import Book

router = APIRouter(prefix="/books", tags=["Books"])



@router.post("/", response_model=Book)
async def create(book: BookCreate, background_tasks: BackgroundTasks):
    return await create_book(Book(**book.model_dump()), background_tasks)


@router.get("/", response_model=list[BookRead])
async def list_all():
    return await list_items(Book)


@router.get("/{book_id}", response_model=BookRead)
async def get(book_id: int):
    book = await get_item(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/{book_id}")
async def delete(book_id: int):
    await delete_item(Book, book_id)
    return {"deleted": book_id}


@router.patch("/{book_id}", response_model=BookRead)
async def update(book_id: int, update_data: dict):
    updated = await update_item(Book, book_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated
