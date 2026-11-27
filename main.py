from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional
from database import Book, get_db
import shutil

app = FastAPI(title="Personal Library API", description="API for managing a personal library")

class BookModel(BaseModel):
    title: str
    author: str
    year: int = Field(..., ge=1800, le=2025)  # Feature 3: Validation

class BookResponse(BookModel):
    id: int
    cover_url: Optional[str] = None
    class Config:
        from_attributes = True

@app.post("/books/", response_model=BookResponse)
def create_book(book: BookModel, db: Session = Depends(get_db)):
    db_book = Book(title=book.title, author=book.author, year=book.year)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books/", response_model=List[BookResponse])
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):  # Feature 4: Pagination
    return db.query(Book).offset(skip).limit(limit).all()

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookModel, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db_book.title = book.title
    db_book.author = book.author
    db_book.year = book.year
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
    return {"message": "Book deleted"}

# Feature 1: Search by Author (Case-insensitive)
@app.get("/books/author/{author}", response_model=List[BookResponse])
def search_author(author: str, db: Session = Depends(get_db)):
    return db.query(Book).filter(Book.author.ilike(f"%{author}%")).all()

# Feature 2: Year Range Filter
@app.get("/books/year/{start_year}/{end_year}", response_model=List[BookResponse])
def filter_years(start_year: int, end_year: int, db: Session = Depends(get_db)):
    return db.query(Book).filter(Book.year.between(start_year, end_year)).all()

# Feature 5: Book Cover Upload (Local Mock/Cloud Upload Endpoint)
@app.post("/books/{book_id}/cover")
def upload_cover(book_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    file_path = f"docs/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    db_book.cover_url = file_path
    db.commit()
    return {"message": "Cover uploaded successfully", "cover_url": file_path}