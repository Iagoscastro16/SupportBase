from fastapi import APIRouter
from functions.support.problems import create_problem, listProblemsByTitle, listProblemsByDate, getProblem, edit_problems, delete_problems
from typing import Optional
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
    creationOfProblems = create_problem(body.title,body.description, body.solution, body.image_problem, body.image_solution)

    return creationOfProblems

@router.get("/problems/{problem_id}")
def get_problem(problem_id: int):
    result = get_problem(problem_id)

    return result

@router.get("/problems")
def list_problem_by_title():
    result = listProblemsByTitle()

    return result

@router.get("/problems/by-date")
def list_problem_by_date(ordemEscolhida: str):
    result = listProblemsByDate(ordemEscolhida)

    return result

@router.patch("/problems/{problem_id}")
def edit_problem(problem_id: int, body: Body_edit_problem):
    result = edit_problems(problem_id, body.title, body.description, body.solution, body.image_problem, body.image_solution)

    return result

@router.delete("/problems/{problem_id}")
def delete_problem(problem_id: int):
    result = delete_problems(problem_id)

    return result