from fastapi import APIRouter, Request, Form

from functions.support.categories import list_categories,get_category_id, create_category

from src.templates_config import templates

router = APIRouter()

@router.get("/ui/categories")
def list_categories_with_problems(request: Request):
    result = list_categories()
    return templates.TemplateResponse(
        request=request,
        name="pages/listing_categories.html",
        context={"categorias":result["data"],"pagina_ativa":"categories"}
    )

@router.get("/ui/categories/new")
def show_create_form_ui(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/create_category.html",
        context={"pagina_ativa": "categories"}
    )

@router.get("/ui/categories/{category_id}")
def getting_category(request: Request, category_id: int):
    result = get_category_id(category_id)

    return templates.TemplateResponse(
        request=request,
        name="partials/get_category_id.html",
        context={"categoria":result}
    )

@router.post("/ui/categories/create")
def create_category_ui(
    request:Request,
    name: str  = Form(...)
):
    create_category(name)

    return templates.TemplateResponse(
        request=request,
        name="partials/category_form.html"
    )