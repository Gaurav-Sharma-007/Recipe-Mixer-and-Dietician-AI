from groq import Groq
from app.config import settings
from app.services.meal_db import search_meals


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
