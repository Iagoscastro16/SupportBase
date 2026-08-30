# Importa o APIRouter, que serve para agrupar todas essas rotas e depois plugar no main.py
from fastapi import APIRouter, Request, Form
# Importação da lógica do négocio
from functions.support.problems import listProblemsByTitle,get_problem, search_problems, create_problem

from functions.support.problems_categories import create_category_problem,list_problems_categories,delete_category_problem

from functions.support.categories import list_categories

from src.templates_config import templates

router = APIRouter()

# Rota de listagem dos problemas

@router.get("/ui/problems")
def show_problems_list(request: Request):
    result = listProblemsByTitle()
    return templates.TemplateResponse(
        request=request,
        name="pages/problems/problem_list_by_title.html",
        context={"problemas": result["data"], "pagina_ativa":"problems"}
    )


@router.get("/ui/problems/search")
def search_problems_ui (request:Request, query: str = ""):
    result = search_problems(query)

    return templates.TemplateResponse(
        request=request,
        name="partials/problems/search_problem.html",
        context={"problemas":result["data"]}
    )

@router.get("/ui/problems/new")
def show_create_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/problems/create_problem.html",
        context={"pagina_ativa": "problems"}
    )

@router.get("/ui/problems/{problem_id}")
def getting_problems(request: Request, problem_id:int):
    result = get_problem(problem_id)
    categorias_disponiveis = list_categories()
    lista_vinculacao  = list_problems_categories(problem_id)


    return templates.TemplateResponse(
        request=request,
        name="partials/problems/problem_detail.html",
        context={"problema":result,
                 "categorias_disponiveis":categorias_disponiveis["data"],
                 "lista_vinculacao":lista_vinculacao["data"]}
    )


@router.post("/ui/problems/create")
def create_problem_ui(
    request:Request,
    title: str = Form(...),
    description: str = Form(...),
    solution: str = Form("")
):
    create_problem(title, description, solution, None, None)
    list_problems_by_title = listProblemsByTitle()

    return templates.TemplateResponse(
        request=request,
        name="partials/problems/form_com_lista_oob.html",
        context={"problemas": list_problems_by_title["data"]}
    )

@router.post("/ui/problems/{problem_id}/categories")
def add_category_to_problem_ui(
    request: Request,
    problem_id: int,
    category_id: int = Form(...)
):
    create_category_problem(problem_id, category_id)
    result = get_problem(problem_id)                     
    categorias_disponiveis = list_categories()
    lista_vinculacao = list_problems_categories(problem_id)
    list_problems_by_title = listProblemsByTitle()

    return templates.TemplateResponse(
    request=request,
    name="partials/problems/detalhe_com_lista_oob.html",
    context={"problema": result,
            "categorias_disponiveis": categorias_disponiveis["data"],
            "lista_vinculacao": lista_vinculacao["data"],
            "problemas": list_problems_by_title["data"]}
        )

@router.delete("/ui/problems/{problem_id}/categories/{category_id}")
def remove_category_from_problem_ui(request: Request, problem_id: int, category_id: int):
    delete_category_problem(problem_id, category_id)
    result = get_problem(problem_id)
    categorias_disponiveis = list_categories()
    lista_vinculacao = list_problems_categories(problem_id)
    list_problems_by_title = listProblemsByTitle()

    return templates.TemplateResponse(
        request=request,
        name="partials/problems/detalhe_com_lista_oob.html",
        context={"problema": result,
                 "categorias_disponiveis": categorias_disponiveis["data"],
                 "lista_vinculacao": lista_vinculacao["data"],
                 "problemas": list_problems_by_title["data"]}
    )

@router.get("/ui/problems/new/form")
def show_create_form_partial(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="partials/problems/problem_form.html"
    )