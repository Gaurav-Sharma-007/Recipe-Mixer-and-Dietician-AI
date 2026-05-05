from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.pantry import Pantry
from app.services.ai_service import suggest_recipes_from_ingredients, remix_recipe_from_ingredients

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

@router.post("/remix")
def remix_recipe(recipe_name: str, db: Session = Depends(get_db)):
    remixed_recipe = remix_recipe_from_ingredients(recipe_name, db)
    return {
        "recipe_query": recipe_name,
        "remixed_recipe": remixed_recipe
    }