from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    isbn = Column(String, unique=True, index=True)
    # Kitap kiralama işlemleriyle ilişki (bir kitap birden fazla kiralama kaydıyla ilişkili olabilir)
    checkouts = relationship("Checkout", back_populates="book")

class Patron(Base):
    __tablename__ = "patrons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    member_since = Column(DateTime)
    # Kitap kiralama işlemleriyle ilişki (bir kullanıcı birden fazla kiralama kaydıyla ilişkili olabilir)
    checkouts = relationship("Checkout", back_populates="patron")

class Checkout(Base):
    __tablename__ = "checkouts"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    patron_id = Column(Integer, ForeignKey("patrons.id"))
    checkout_date = Column(DateTime)
    due_date = Column(DateTime)
    return_date = Column(DateTime, nullable=True)

    # Kitap ve kullanıcı modelleriyle ilişkiler (her kiralama kaydı bir kitap ve bir kullanıcıyla ilişkilidir)
    book = relationship("Book", back_populates="checkouts")
    patron = relationship("Patron", back_populates="checkouts")