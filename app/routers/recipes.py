from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.pantry import Pantry
from app.services.ai_service import suggest_recipes_from_ingredients

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/suggest")
def suggest_recipes(db: Session = Depends(get_db)):
    pantry_items = db.query(Pantry).all()
    
    ingredients = [item.ingredient for item in pantry_items]

    recipes = suggest_recipes_from_ingredients(ingredients)

    return {
        "ingredients": ingredients,
        "suggested_recipes": recipes
    }
