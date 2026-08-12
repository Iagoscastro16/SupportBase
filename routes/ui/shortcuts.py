from fastapi import APIRouter, Request

from functions.copy.shortcut import listshortcutByPosition, get_shortcut

from src.templates_config import templates

router = APIRouter()

@router.get("/ui/shortcuts")
def list_shortcut_by_position(request:Request):
    result = listshortcutByPosition()
    return templates.TemplateResponse(
        request=request,
        name="pages/shortcut_by_position.html",
        context={"atalhos":result["data"],"pagina_ativa":"shortcuts"}
    )

@router.get("/ui/shortcuts/{shortcut_id}")
def getting_shortcut(request: Request, shortcut_id: int):
    result = get_shortcut(shortcut_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/shortcut_detail.html",
        context={"atalho": result}
    )