from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta

router = APIRouter()

# Kitap kiralama işlemini temsil eden bir veri modeli sınıfı tanımla
class CheckoutOperation(BaseModel):
    book_id: int
    patron_id: int
    checkout_date: datetime
    due_date: datetime

# Kitap iade işlemini temsil eden bir veri modeli sınıfı tanımla
class ReturnOperation(BaseModel):
    book_id: int
    patron_id: int
    return_date: datetime

checkout_operations = []

# Kitap kiralama işlemi oluşturma API ucu
@router.post("/checkout/", response_model=CheckoutOperation)
async def checkout_book(book_id: int, patron_id: int):
    checkout_date = datetime.now()
    due_date = checkout_date + timedelta(days=14)  # 2 hafta teslim süresi
    checkout = CheckoutOperation(
        book_id=book_id,
        patron_id=patron_id,
        checkout_date=checkout_date,
        due_date=due_date
    )
    checkout_operations.append(checkout)
    return checkout

# Kitap iade işlemi oluşturma API ucu
@router.post("/return/", response_model=ReturnOperation)
async def return_book(book_id: int, patron_id: int):
    for checkout in checkout_operations:
        if checkout.book_id == book_id and checkout.patron_id == patron_id:
            checkout_operations.remove(checkout)
            return ReturnOperation(
                book_id=book_id,
                patron_id=patron_id,
                return_date=datetime.now()
            )
    raise HTTPException(status_code=404, detail="Checkout record not found")

# Kiralanan kitaplar listesi API ucu
@router.get("/checked-out-books/", response_model=list[CheckoutOperation])
async def list_checked_out_books():
    return checkout_operations

# Gecikmiş kitaplar listesi API ucu
@router.get("/overdue-books/", response_model=list[CheckoutOperation])
async def list_overdue_books():
    current_date = datetime.now()
    return [checkout for checkout in checkout_operations if checkout.due_date < current_date]