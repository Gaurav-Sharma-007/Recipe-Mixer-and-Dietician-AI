from pydantic import BaseModel
from typing import Optional


class RecipeRequest(BaseModel):
    recipe_id: int
    recipe_name: Optional[str] = None


class RecipeResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    user_id: Optional[int] = None

    class Config:
        from_attributes = True
