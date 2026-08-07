# Importa o APIRouter, que serve para agrupar todas essas rotas e depois plugar no main.py
from fastapi import APIRouter, Request
# Importação da lógica do négocio
from functions.support.problems import listProblemsByTitle,get_problem

from src.templates_config import templates

router = APIRouter()

# Rota de listagem dos problemas

@router.get("/ui/problems")
def show_problems_list(request: Request):
    result = listProblemsByTitle()
    return templates.TemplateResponse(
        request=request,
        name="pages/problem_list_by_title.html",
        context={"problemas": result["data"]}
    )

@router.get("/ui/problems/{problem_id}")
def getting_problems(request: Request, problem_id:int):
    result = get_problem(problem_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/problem_detail.html",
        context={"problema":result}
    )