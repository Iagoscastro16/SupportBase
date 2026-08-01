from fastapi import APIRouter
from functions.copy.shortcut import createshortcut, listshortcutByPosition, listShortcutByDate, EditShortcut, deleteshortcut
from typing import Optional
from pydantic import BaseModel

router = APIRouter()

class body_create_shortcut(BaseModel):
    short_cut_key: str
    phrase: Optional[str] = None
    position: Optional[int] = None


class body_edit_shortcut(BaseModel):
    short_cut_key: Optional[str] = None
    phrase: Optional[str] = None
    position: Optional[int] = None

@router.post("/shortcuts")
def creation_shortcuts(body: body_create_shortcut):
    result = createshortcut(body.short_cut_key, body.phrase, body.position)

    return result

@router.get("/shortcuts/by-position")
def shortcut_by_position():
    result = listshortcutByPosition()

    return result

@router.get("/shortcuts/by-date")
def shortcut_by_date(ordem_escolhida: str):
    result = listShortcutByDate(ordem_escolhida)

    return result

@router.patch("/shortcuts/{shortcut_id}")
def edition_shortcut(shortcut_id: int, body: body_edit_shortcut):
    result = EditShortcut(shortcut_id, body.short_cut_key, body.phrase, body.position)

    return result


@router.delete("/shortcuts/{shortcut_id}")
def delete_of_shortcut(shortcut_id: int):
    result = deleteshortcut(shortcut_id)

    return result