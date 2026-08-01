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
    result = listCategories()

    return result

# Rota de criação das categorias

@router.post("/categories")
def creationCategory(body: BodyName):
    result = createCategory(body.name)

    return result

# Rota de atualizar as categorias, utilizei patch por ele deixar escolher o que atualizar, ao inves do post que sempre envia tudo

@router.patch("/categories/{category_id}")
def editingCategories(category_id: int, body: BodyName):
    result = editCategories(category_id, body.name)

    return result

# Rota de deletar a categgoria

@router.delete("/categories/{category_id}")
def deletingCategories(category_id: int):
    result = deleteCategory(category_id)

    return result