from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .models import Base

# Veritabanı bağlantı adresi (SQLite kullanılıyor)
SQLALCHEMY_DATABASE_URL = "sqlite:///./library.db"

# Veritabanı bağlantısı oluştur
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Oturum oluşturma fonksiyonu
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tabloları oluşturma fonksiyonu (ilk çalıştırmada tablolar oluşturulabilir)
def create_tables():
    Base.metadata.create_all(bind=engine)

# Veritabanı oturumu sağlama fonksiyonu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()