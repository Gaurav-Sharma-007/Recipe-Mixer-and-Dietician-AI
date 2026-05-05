from fastapi import Depends
from app.config import settings
from app.schemas import pantry
def test1(pantry: list[pantry.PantryRead]):
    pantry_items = [item for item in pantry]
    ingredients = [item.ingredient for item in pantry_items]
    return {
    "recipes": [
        f"Recipe using {', '.join(ingredients)}"
    ]
}