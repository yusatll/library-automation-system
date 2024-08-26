from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class Book(BaseModel):
    id: int
    title: str
    author: str
    isbn: str

# Fake bir kitap listesi (gerçek uygulamada veritabanı kullanılmalı)
books = []

# Yeni bir kitap ekleme işlemi
@router.post("/books/", response_model=Book)
async def create_book(book: Book):
    books.append(book)
    return book

# Tüm kitapları listeleme işlemini tanımla
@router.get("/books/", response_model=list[Book])
async def read_books():
    return books

# Belirli bir kimliğe sahip kitabı getirme işlemini tanımla
@router.get("/books/{book_id}", response_model=Book)
async def read_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# Belirli bir kimliğe sahip kitabı güncelleme işlemini tanımla
@router.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, updated_book: Book):
    for i, book in enumerate(books):
        if book.id == book_id:
            books[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

# Belirli bir kimliğe sahip kitabı silme işlemini tanımla
@router.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i, book in enumerate(books):
        if book.id == book_id:
            del books[i]
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")