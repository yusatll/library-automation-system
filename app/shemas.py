from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Temel kitap bilgileri için şema sınıfı
class BookBase(BaseModel):
    title: str
    author: str
    isbn: str

class BookCreate(BookBase):
    pass

# Kitap bilgileri için şema sınıfı
class Book(BookBase):
    id: int

    class Config:
        orm_mode = True

# Temel kullanıcı bilgileri için şema sınıfı
class PatronBase(BaseModel):
    name: str
    email: EmailStr

# Yeni kullanıcı ekleme şema sınıfı
class PatronCreate(PatronBase):
    pass

class Patron(PatronBase):
    id: int
    member_since: datetime

    class Config:
        orm_mode = True

# Temel kitap kiralama bilgileri için şema sınıfı
class CheckoutBase(BaseModel):
    book_id: int
    patron_id: int

# Yeni kiralama işlemi ekleme şema sınıfı
class CheckoutCreate(CheckoutBase):
    pass

# Kitap kiralama bilgileri için şema sınıfı
class Checkout(CheckoutBase):
    id: int
    checkout_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None

    class Config:
        orm_mode = True # SQLAlchemy modelleri ile uyumlu hale getirir