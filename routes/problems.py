from fastapi import APIRouter
from functions.support.problems import createProblem, listProblemsByTitle, listProblemsByDate, getProblem, editProblems, deleteProblems
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

# Rota criação problems

@router.post("/problems")
def creationProblems(body: Body_problem):
    creationOfProblems = createProblem(body.title,body.description, body.solution, body.image_problem, body.image_solution)

    return creationOfProblems

@router.get("/problems/{problem_id}")
def get_problem(problem_id: int):
    result = get_problem(problem_id)

    return result

@router.get("/problems")
def list_problem_by_title():
    result = listProblemsByTitle()

    return result