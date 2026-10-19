from fastapi import APIRouter
from functions.support.categories import create_category, edit_categories, list_categories, delete_category
from pydantic import BaseModel

router = APIRouter(tags=["Categories"])

#Base Model utilizando o pydantic, essa classe serve para tratar e validar os dados de forma mais simplificada

class BodyName(BaseModel):
    name: str
    empresa_id: int

# Rota de listar as categorias

@router.get("/categories")
def listOfcategories(empresa_id: int, incluir_inativo: bool = False):
    # Assinatura do service: list_categories(empresa_id, incluir_inativo)
    result = list_categories(empresa_id, incluir_inativo)

    return result

# Rota de criação das categorias

@router.post("/categories")
def creationCategory(body: BodyName):
    # Assinatura do service: create_category(name, empresa_id)
    result = create_category(body.name, body.empresa_id)

    return result

# Rota de atualizar as categorias, utilizei patch por ele deixar escolher o que atualizar, ao inves do post que sempre envia tudo

@router.patch("/categories/{category_id}")
def editingCategories(category_id: int, body: BodyName):
    # Assinatura do service: edit_categories(id, name, empresa_id)
    result = edit_categories(category_id, body.name, body.empresa_id)

    return result

# Rota de deletar a categgoria

@router.delete("/categories/{category_id}")
def deletingCategories(category_id: int, empresa_id: int):
    # Assinatura do service: delete_category(id, empresa_id)
    result = delete_category(category_id, empresa_id)

    return result
