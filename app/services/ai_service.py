from groq import Groq
from sqlalchemy.orm import Session
from fastapi import Depends
from app.config import settings
from app.database import SessionLocal
from app.services.meal_db import search_meals
from app.models.recipe import Recipe


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def suggest_recipes_from_ingredients(ingredients: list[str]) -> dict[str, object]:
    """Suggest recipes from pantry ingredients.

    TheMealDB gives us deterministic recipe-name matches. When a Groq API key is
    configured, use those matches as context for a short AI-curated list.
    """
    meal_matches = search_meals(ingredients)
    result = {
        "mealdb_first_match": meal_matches[0] if meal_matches else None,
        "mealdb_matches": meal_matches,
        "groq_note": "The following recipes are generated using Groq AI.",
        "groq_generated_recipes": [],
    }

    if not settings.groq_api_key:
        return result

    ingredient_text = ", ".join(ingredients)
    first_match = meal_matches[0] if meal_matches else "No direct MealDB match found."
    other_matches = ", ".join(meal_matches[1:]) if len(meal_matches) > 1 else "None."

    try:
        client = Groq(api_key=settings.groq_api_key)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Return only a concise newline-separated list of additional recipe names. "
                        "Do not include MealDB matches, headings, bullets, or extra commentary."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Suggest recipes using these ingredients: {ingredient_text}. "
                        f"The first MealDB match is: {first_match}. "
                        f"Other MealDB matches, for context only: {other_matches}"
                    ),
                },
            ],
            model=settings.groq_model,
        )
    except Exception as exc:
        result["groq_error"] = f"Groq suggestions unavailable: {exc}"
        return result

    content = chat_completion.choices[0].message.content
    if not content:
        return result

    mealdb_names = {meal_name.lower() for meal_name in meal_matches}
    result["groq_generated_recipes"] = [
        recipe_name
        for line in content.splitlines()
        if (recipe_name := line.strip("- ").strip())
        and recipe_name.lower() not in mealdb_names
    ]
    return result

def remix_recipe_from_ingredients(recipe_name: str, db: Session) -> dict[str, object]:
    """Remix a recipe using the database to verify it exists and Groq AI to generate variants."""
    recipe_record = db.query(Recipe).filter(Recipe.name.ilike(f"%{recipe_name}%")).first()
    
    result = {
        "db_match": recipe_record.name if recipe_record else None,
        "groq_note": "The following recipes are generated using Groq AI.",
        "groq_generated_recipes": [],
    }

    if not recipe_record:
        result["error"] = f"No recipe found matching '{recipe_name}' in the database."
        return result

    if not settings.groq_api_key:
        result["groq_error"] = "Groq API key not configured."
        return result

    try:
        client = Groq(api_key=settings.groq_api_key)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert chef. Your task is ONLY to return variants of the specific recipe provided. "
                        "Do NOT suggest entirely new recipes. Provide exactly 3 variants: one vegan, one vegetarian, and one spicy. "
                        "Return only a concise newline-separated list of the 3 variant names. "
                        "Do not include headings, bullets, or extra commentary."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Recipe name: {recipe_record.name}",
                },
            ],
            model=settings.groq_model,
        )
    except Exception as exc:
        result["groq_error"] = f"Groq suggestions unavailable: {exc}"
        return result

    content = chat_completion.choices[0].message.content
    if not content:
        return result

    result["groq_generated_recipes"] = [
        line.strip("- ").strip()
        for line in content.splitlines()
        if line.strip("- ").strip()
    ]
    return result
