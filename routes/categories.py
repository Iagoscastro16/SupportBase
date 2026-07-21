from fastapi import APIRouter
from functions.support.categories import createCategory, editCategories, listCategories, deleteCategory
from pydantic import BaseModel

router = APIRouter()

class BodyName(BaseModel):
    name: str

@router.get("/categories")
def listOfcategories():
    listingCategories = listCategories()

    return listingCategories

@router.post("/categories")
def creationCategory(body: BodyName):
    creationOfCategory = createCategory(body.name)

    return creationOfCategory

@router.patch("/categories/{category_id}")
def editingCategories(category_id: int, body: BodyName):
    editOfCategories = editCategories(category_id, body.name)

    return editOfCategories

@router.delete("/categories/{category_id}")
def deletingCategories(category_id: int):
    deleteOfCategories = deleteCategory(category_id)

    return deleteOfCategories