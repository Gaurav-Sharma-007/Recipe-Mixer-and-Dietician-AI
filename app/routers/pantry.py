from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.pantry import Pantry
from app.schemas.pantry import PantryCreate, PantryRead

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PantryRead)
def add_item(item: PantryCreate, db: Session = Depends(get_db)):
    db_item = Pantry(ingredient=item.ingredient, user_id=1)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/", response_model=list[PantryRead])
def list_items(db: Session = Depends(get_db)):
    return db.query(Pantry).all()

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Pantry).filter(Pantry.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
        return {"message": "Item deleted"}
    return {"message": "Item not found"}

