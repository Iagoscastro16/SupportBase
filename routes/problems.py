from fastapi import APIRouter
from functions.support.problems import createProblem, listProblemsByTitle, listProblemsByDate, getProblem, editProblems, deleteProblems
from typing import Optional
from pydantic import BaseModel

router = APIRouter()

# Base Model do problems, aqui me utilizei do optional para não obrigar a requisição a mandar solution, image problem e description

class BodyProblem(BaseModel):
    title: str
    description: str
    solution: Optional[str] = None
    image_problem: Optional[str] = None
    image_solution: Optional[str] = None

# Rota criação problems

@router.post("/problems")
def creationProblems(body: BodyProblem):
    creationOfProblems = createProblem(body.title,body.description, body.solution, body.image_problem, body.image_solution)

    return creationOfProblems


