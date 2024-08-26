from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models, schemas

# Belirli bir tarihten diğerine kiralanan kitapları getir
def get_checkouts_in_period(db: Session, start_date: datetime, end_date: datetime):
    return db.query(models.Checkout).filter(
        models.Checkout.checkout_date >= start_date,
        models.Checkout.checkout_date <= end_date
    ).all()

# Belirli bir tarihten diğerine iade edilen kitapları getir
def get_returns_in_period(db: Session, start_date: datetime, end_date: datetime):
    return db.query(models.Checkout).filter(
        models.Checkout.return_date >= start_date,
        models.Checkout.return_date <= end_date
    ).all()

def update_book(db: Session, book_id: int, book: schemas.BookCreate):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    db.delete(db_book)
    db.commit()

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_patron(db: Session, patron_id: int):
    return db.query(models.Patron).filter(models.Patron.id == patron_id).first()

def get_patrons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Patron).offset(skip).limit(limit).all()

def create_patron(db: Session, patron: schemas.PatronCreate):
    db_patron = models.Patron(**patron.dict(), member_since=datetime.now())
    db.add(db_patron)
    db.commit()
    db.refresh(db_patron)
    return db_patron

def create_checkout(db: Session, checkout: schemas.CheckoutCreate):
    db_checkout = models.Checkout(
        **checkout.dict(),
        checkout_date=datetime.now(),
        due_date=datetime.now() + timedelta(days=14)
    )
    db.add(db_checkout)
    db.commit()
    db.refresh(db_checkout)
    return db_checkout

def get_checkouts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Checkout).offset(skip).limit(limit).all()

def get_overdue_checkouts(db: Session):
    return db.query(models.Checkout).filter(
        models.Checkout.due_date < datetime.now(),
        models.Checkout.return_date == None
    ).all()

def return_book(db: Session, checkout_id: int):
    db_checkout = db.query(models.Checkout).filter(models.Checkout.id == checkout_id).first()
    if db_checkout:
        db_checkout.return_date = datetime.now()
        db.commit()
        db.refresh(db_checkout)
    return db_checkout