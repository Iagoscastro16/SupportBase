# Importa o APIRouter, que serve para agrupar todas essas rotas e depois plugar no main.py
from fastapi import APIRouter
# Importação da lógica do négocio
from functions.support.problems import create_problem, listProblemsByTitle, listProblemsByDate, getProblem, edit_problems, delete_problems
# Optional é usado para dizer que um campo pode ser None (nulo/vazio)
from typing import Optional
#  BaseModel do Pydantic é a ferramenta do FastAPI para validar o corpo da requisição (JSON)
from pydantic import BaseModel

router = APIRouter()

# Base Model do problems, aqui me utilizei do optional para não obrigar a requisição a mandar solution, image problem e description

class Body_problem(BaseModel):
    title: str
    description: str
    solution: Optional[str] = None
    image_problem: Optional[str] = None
    image_solution: Optional[str] = None

# O editproblems necessita de todos os campos serem opcionais, pois nem sempre o usuario vai mudar tudo obviamente

class Body_edit_problem(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    solution : Optional[str] = None
    image_problem: Optional[str] = None
    image_solution: Optional[str] = None

# Rota criação problems

@router.post("/problems")
def creationProblems(body: Body_problem):
    result = create_problem(body.title,body.description, body.solution, body.image_problem, body.image_solution)

    return result

@router.get("/problems/{problem_id}")
def get_problem(problem_id: int,):
    result = get_problem(problem_id)

    return result

@router.get("/problems")
def list_problem_by_title(incluir_inativo: bool = False):
    result = listProblemsByTitle(incluir_inativo)

    return result

@router.get("/problems/by-date")
def list_problem_by_date(ordemEscolhida: str, incluir_inativo: bool = False):
    result = listProblemsByDate(ordemEscolhida, incluir_inativo)

    return result

@router.patch("/problems/{problem_id}")
def edit_problem(problem_id: int, body: Body_edit_problem):
    result = edit_problems(problem_id, body.title, body.description, body.solution, body.image_problem, body.image_solution)

    return result

@router.delete("/problems/{problem_id}")
def delete_problem(problem_id: int):
    result = delete_problems(problem_id)

    return result