from fastapi import APIRouter, Request

from functions.support.categories import list_categories,get_category_id

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

@router.get("/ui/categories/{category_id}")
def getting_category(request: Request, category_id: int):
    result = get_category_id(category_id)

    return templates.TemplateResponse(
        request=request,
        name="partials/get_category_id.html",
        context={"categoria":result}
    )