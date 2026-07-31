from fastapi import APIRouter
from functions.copy.shortcut import validateEditPosition, createshortcut, listshortcutByPosition, listShortcutByDate, EditShortcut, deleteshortcut
from typing import Optional
from pydantic import BaseModel

class body_create_shortcut(BaseModel):
    short_cut_key: str
    phrase: Optional[str] = None
    position: Optional[int] = None


class body_edit_shortcut(BaseModel):
    short_cut_key: Optional[str] = None
    phrase: Optional[str] = None
    position: Optional[int] = None