from fastapi import APIRouter
from functions.support.categories import createCategory, editCategories, listCategories, deleteCategory
from pydantic import BaseModel

router = APIRouter()

#Base Model utilizando o pydantic, essa classe serve para tratar e validar os dados de forma mais simplificada

class BodyName(BaseModel):
    name: str

# Rota de listar as categorias

@router.get("/categories")
def listOfcategories():
    listingCategories = listCategories()

    return listingCategories

# Rota de criação das categorias

@router.post("/categories")
def creationCategory(body: BodyName):
    creationOfCategory = createCategory(body.name)

    return creationOfCategory

# Rota de atualizar as categorias, utilizei patch por ele deixar escolher o que atualizar, ao inves do post que sempre envia tudo

@router.patch("/categories/{category_id}")
def editingCategories(category_id: int, body: BodyName):
    editOfCategories = editCategories(category_id, body.name)

    return editOfCategories

# Rota de deletar a categgoria

@router.delete("/categories/{category_id}")
def deletingCategories(category_id: int):
    deleteOfCategories = deleteCategory(category_id)

    return deleteOfCategories