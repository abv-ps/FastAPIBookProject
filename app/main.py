from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
import asyncio

from app.db.session import SessionLocal, engine
from app.models.author import Base, Author, Book
from schemas import AuthorCreate, AuthorRead, BookCreate, BookRead, BookUpdate

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def long_task(book_title: str):
    await asyncio.sleep(5)
    print(f"Background task finished for book: {book_title}")

@app.post("/authors/", response_model=AuthorRead)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@app.get("/authors/", response_model=List[AuthorRead])
def list_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()

@app.post("/books/", response_model=BookRead)
async def create_book(book: BookCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_book = Book(title=book.title)
    db_book.authors = db.query(Author).filter(Author.id.in_(book.author_ids)).all()
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    background_tasks.add_task(long_task, db_book.title)
    return db_book

@app.get("/books/", response_model=List[BookRead])
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@app.patch("/books/{book_id}", response_model=BookRead)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.title is not None:
        db_book.title = book.title
    if book.author_ids is not None:
        db_book.authors = db.query(Author).filter(Author.id.in_(book.author_ids)).all()

    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)
    db.commit()
    return {"message": f"Book {book_id} deleted"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
