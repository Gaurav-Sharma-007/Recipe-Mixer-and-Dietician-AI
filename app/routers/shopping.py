from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def get_shopping_list():
    return {"items": []}
