from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

router = APIRouter()

class Patron(BaseModel):
    id: int
    name: str
    email: EmailStr
    member_since: str

patrons = []

# Yeni bir kullanıcı ekleme API ucu
@router.post("/patrons/", response_model=Patron)
async def create_patron(patron: Patron):
    patrons.append(patron)
    return patron

# Tüm kullanıcıları listeleme API ucu
@router.get("/patrons/", response_model=list[Patron])
async def read_patrons():
    return patrons

# Belirli bir kimliğe sahip kullanıcıyı getirme API ucu
@router.get("/patrons/{patron_id}", response_model=Patron)
async def read_patron(patron_id: int):
    for patron in patrons:
        if patron.id == patron_id:
            return patron
    raise HTTPException(status_code=404, detail="Patron not found")

# Belirli bir kimliğe sahip kullanıcıyı güncelleme API ucu
@router.put("/patrons/{patron_id}", response_model=Patron)
async def update_patron(patron_id: int, updated_patron: Patron):
    for i, patron in enumerate(patrons):
        if patron.id == patron_id:
            patrons[i] = updated_patron
            return updated_patron
    raise HTTPException(status_code=404, detail="Patron not found")

# Belirli bir kimliğe sahip kullanıcıyı silme API ucu
@router.delete("/patrons/{patron_id}")
async def delete_patron(patron_id: int):
    for i, patron in enumerate(patrons):
        if patron.id == patron_id:
            del patrons[i]
            return {"message": "Patron deleted successfully"}
    raise HTTPException(status_code=404, detail="Patron not found")