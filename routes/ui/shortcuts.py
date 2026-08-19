from fastapi import APIRouter, Request, Form

from functions.copy.shortcut import listshortcutByPosition, get_shortcut, createshortcut

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

@router.get("/ui/shortcuts/new")
def show_create_form_shortcut(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/create_shortcut.html",
        context={"pagina_ativa":"shortcuts"}
    )

@router.get("/ui/shortcuts/{shortcut_id}")
def getting_shortcut(request: Request, shortcut_id: int):
    result = get_shortcut(shortcut_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/shortcut_detail.html",
        context={"atalho": result}
    )

@router.post("/ui/shortcuts/create")
def create_shortcut_ui(
    request: Request,
    short_cut_key: str = Form(...),
    phrase: str = Form(...),
    position: int = Form(None)):
    createshortcut(short_cut_key, phrase, position)
    return templates.TemplateResponse(
        request=request,
        name="partials/shortcut_form.html"
    )