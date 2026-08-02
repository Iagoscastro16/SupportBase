from fastapi import APIRouter
from functions.support.categories import create_category, edit_categories, list_categories, delete_category
from pydantic import BaseModel

router = APIRouter()

#Base Model utilizando o pydantic, essa classe serve para tratar e validar os dados de forma mais simplificada

class BodyName(BaseModel):
    name: str

# Rota de listar as categorias

@router.get("/categories")
def listOfcategories():
    result = list_categories()

    return result

# Rota de criação das categorias

@router.post("/categories")
def creationCategory(body: BodyName):
    result = create_category(body.name)

    return result

# Rota de atualizar as categorias, utilizei patch por ele deixar escolher o que atualizar, ao inves do post que sempre envia tudo

@router.patch("/categories/{category_id}")
def editingCategories(category_id: int, body: BodyName):
    result = edit_categories(category_id, body.name)

    return result

# Rota de deletar a categgoria

@router.delete("/categories/{category_id}")
def deletingCategories(category_id: int):
    result = delete_category(category_id)

    return result