from fastapi import APIRouter
from functions.support.problems_categories import createCategoryProblem, deleteCategoryProblem, listProblemsCategories
from pydantic import BaseModel

router = APIRouter()

# Base Model utilizando o pydantic, essa classe serve para tratar e validar os dados de forma mais simplificada

class CategoryProblemBody(BaseModel):
    category_id: int

# Listar os problemas

@router.get("/problems/{problem_id}/categories")
def listOfCategoryProblems(problem_id:int):
    listResult = listProblemsCategories(problem_id)

    return listResult


@router.delete("/problems/{problem_id}/categories/{category_id}")
def deleteOfProblemCategory(problem_id:int,category_id:int):
    eraseResult = deleteCategoryProblem(problem_id,category_id)

    return eraseResult

# Utilização do BaseModel para a criação da atribuição na rota de atribuir categories a problems

@router.post("/problems/{problem_id}/categories")
def creationCategoryProblem(problem_id:int,body: CategoryProblemBody):
    creationOfCategoryProblem = createCategoryProblem(problem_id,body.category_id)

    return creationOfCategoryProblem 