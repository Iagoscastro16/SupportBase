from fastapi import APIRouter, HTTPException
from functions.support.problems_categories import create_category_problem, delete_category_problem, list_problems_categories
from pydantic import BaseModel

router = APIRouter(tags=["Problems-Categories"])

# Base Model utilizando o pydantic, essa classe serve para tratar e validar os dados de forma mais simplificada

class CategoryProblemBody(BaseModel):
    category_id: int
    empresa_id: int

# Listar os problemas

@router.get("/problems/{problem_id}/categories")
def listOfCategoryProblems(problem_id:int, empresa_id: int):
    # Assinatura do service: list_problems_categories(problem_id, empresa_id)
    result = list_problems_categories(problem_id, empresa_id)

    return result


@router.delete("/problems/{problem_id}/categories/{category_id}")
def deleteOfProblemCategory(problem_id:int,category_id:int, empresa_id: int):
    # Assinatura do service: delete_category_problem(problem_id, category_id, empresa_id)
    result = delete_category_problem(problem_id,category_id, empresa_id)

    return result

# Utilização do BaseModel para a criação da atribuição na rota de atribuir categories a problems

@router.post("/problems/{problem_id}/categories")
def creationCategoryProblem(problem_id: int, body: CategoryProblemBody):
    # Assinatura do service: create_category_problem(problem_id, category_id, empresa_id)
    result = create_category_problem(problem_id, body.category_id, body.empresa_id)
    if isinstance(result, dict) and not result.get("success", True):
        raise HTTPException(status_code=400, detail=result["errorMessage"])
    return result
