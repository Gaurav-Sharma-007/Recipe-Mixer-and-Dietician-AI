from pydantic import BaseModel, ConfigDict


class PantryBase(BaseModel):
    ingredient: str


class PantryCreate(PantryBase):
    pass


class PantryRead(PantryBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
