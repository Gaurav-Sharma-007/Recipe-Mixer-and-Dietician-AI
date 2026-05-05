from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def nutrition_status():
    return {"message": "Nutrition router is ready"}
