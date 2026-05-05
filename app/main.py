from fastapi import FastAPI
from app.config import settings
from app.database import Base, engine
from app.models import pantry as pantry_model
from app.routers import auth, pantry, recipes, nutrition, shopping, meal_plan

app = FastAPI(
    title=settings.app_name,
    description="AI-powered recipe suggestions from your pantry",
    version="1.0.0"
)


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

# Register all routers
app.include_router(auth.router,       prefix="/auth",          tags=["Auth"])
app.include_router(pantry.router,     prefix="/pantry",        tags=["Pantry"])
app.include_router(recipes.router,    prefix="/recipes",       tags=["Recipes"])
app.include_router(nutrition.router,  prefix="/nutrition",     tags=["Nutrition"])
app.include_router(shopping.router,   prefix="/shopping-list", tags=["Shopping"])
app.include_router(meal_plan.router,  prefix="/meal-plan",     tags=["Meal Plan"])

@app.get("/")
def root():
    return {"message": "Welcome to Recipe Remix API - your AI-powered recipe assistant!"}

@app.get("/health")
def health():
    return {"status": "ok"}
