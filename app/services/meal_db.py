import json
import urllib.parse
import urllib.request


def search_meals(ingredients: list[str]) -> list[str]:
    cleaned_ingredients = [
        ingredient.strip().lower().replace(" ", "_")
        for ingredient in ingredients
        if ingredient and ingredient.strip()
    ]

    if not cleaned_ingredients:
        return []

    ingredient_text = ",".join(cleaned_ingredients)
    print(f"Searching meals with ingredients: {ingredient_text}")

    url = f"https://www.themealdb.com/api/json/v2/1/filter.php?i={urllib.parse.quote(ingredient_text)}"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)

        meals = data.get("meals")

        if not meals:
            return []  # No results found

        # Extract only strMeal
        meal_name = [meal.get("strMeal") for meal in meals if meal.get("strMeal")]

        return meal_name

    except Exception as e:
        print("Error:", e)
        return []
    