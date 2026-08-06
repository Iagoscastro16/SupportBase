from fastapi import APIRouter, Request

from functions.support.categories import list_categories

from src.templates_config import templates

router = APIRouter()

@router.get("/ui/categories")
def show_categories_list(request: Request):
    result = list_categories()
    return templates.TemplateResponse(
        request=request,
        name="listing_categories.html",
        context={"categorias":result["data"]}
    )