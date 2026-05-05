from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.pantry import Pantry
from app.services.ai_service import suggest_recipes_from_ingredients, remix_recipe_from_ingredients
from app.models.recipe import Recipe
from app.schemas import RecipeRequest
from fastapi import HTTPException

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

    first_match = recipes.get("mealdb_first_match")
    if first_match:
        # Check if the recipe is already in the database
        existing = db.query(Recipe).filter(Recipe.name == first_match).first()
        if not existing:
            new_recipe = Recipe(name=first_match)
            db.add(new_recipe)
            db.commit()
            db.refresh(new_recipe)

    return {
        "ingredients": ingredients,
        "suggested_recipes": recipes
    }

@router.post("/remix")
def get_recipe_for_remix(request: RecipeRequest, db: Session = Depends(get_db)):
    # Look up the recipe by ID
    db_recipe = db.query(Recipe).filter(Recipe.id == request.recipe_id).first()
    
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
        
    remixed_recipe = remix_recipe_from_ingredients(db_recipe.name, db)
    return remixed_recipe


@router.get("/")
def list_recipes(db: Session = Depends(get_db)):
    """List all recipes stored in the database."""
    recipes = db.query(Recipe).all()
    return recipes


@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """Delete a recipe by its ID."""
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
        
    db.delete(db_recipe)
    db.commit()
    return {"detail": f"Recipe {recipe_id} deleted successfully"}
