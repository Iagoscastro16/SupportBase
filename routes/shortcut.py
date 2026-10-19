# Importa o APIRouter, que serve para agrupar todas essas rotas e depois plugar no main.py
from fastapi import APIRouter

# Importa as funções de banco de dados (Services) que contêm a lógica real e o try/except
from functions.copy.shortcut import createshortcut, listshortcutByPosition, listShortcutByDate, EditShortcut, deleteshortcut

# O Optional é usado para dizer que um campo pode ser None (nulo/vazio)
from typing import Optional

# O BaseModel do Pydantic é a ferramenta do FastAPI para validar o corpo da requisição (JSON)
from pydantic import BaseModel

router = APIRouter(tags=["Shortcuts"])

# Modelo para criar: A chave do atalho é obrigatória, mas a frase e a posição são opcionais
class body_create_shortcut(BaseModel):
    short_cut_key: str
    empresa_id: int
    usuario_id: int
    phrase: Optional[str] = None
    position: Optional[int] = None

# Modelo para editar: Tudo é opcional. Por que? 
# Porque num PATCH (atualização parcial), o usuário pode querer mudar só a frase, 
# deixando a chave e a posição intactas (o que vai virar None e o COALESCE no SQL vai ignorar)
class body_edit_shortcut(BaseModel):
    empresa_id: int
    usuario_id: int
    short_cut_key: Optional[str] = None
    phrase: Optional[str] = None
    position: Optional[int] = None

# ---------------------------------------------------------
# ROTAS (CONTROLLERS)
# ---------------------------------------------------------

# Rota para CRIAR um atalho
@router.post("/shortcuts")
def creation_shortcuts(body: body_create_shortcut):
    # Pega os dados já validados pelo Pydantic e repassa para a função do banco de dados
    # Assinatura do service: createshortcut(short_cut_key, phrase, position, empresa_id, usuario_id)
    result = createshortcut(body.short_cut_key, body.phrase, body.position, body.empresa_id, body.usuario_id)
    return result

# Rota para LISTAR atalhos ordenados por POSIÇÃO
@router.get("/shortcuts/by-position")
def shortcut_by_position(empresa_id: int, usuario_id: int):
    # Recebe só a empresa e o usuário dono dos atalhos, a função do banco faz o SELECT com ORDER BY
    # Assinatura do service: listshortcutByPosition(empresa_id, usuario_id)
    result = listshortcutByPosition(empresa_id, usuario_id)
    return result

# Rota para LISTAR atalhos ordenados por DATA
# Repare que 'ordem_escolhida' não está entre chaves {} na URL. 
# Isso significa que o FastAPI vai esperar isso como um Query Parameter (ex: /shortcuts/by-date?ordem_escolhida=maisRecente)
@router.get("/shortcuts/by-date")
def shortcut_by_date(ordem_escolhida: str, empresa_id: int, usuario_id: int):
    # Repassa a string ("maisAntiga" ou "maisRecente") para a função de banco decidir o ORDER BY
    # Assinatura do service: listShortcutByDate(ordem_escolhida, empresa_id, usuario_id)
    result = listShortcutByDate(ordem_escolhida, empresa_id, usuario_id)
    return result

# Rota para EDITAR um atalho (Atualização Parcial)
# O ID vem na URL (Path Parameter) e os dados a serem alterados vêm no corpo (Body)
@router.patch("/shortcuts/{shortcut_id}")
def edition_shortcut(shortcut_id: int, body: body_edit_shortcut):
    # Repassa o ID e os dados opcionais para a função de banco que usa o COALESCE
    # Assinatura do service: EditShortcut(id, short_cut_key, phrase, position, empresa_id, usuario_id)
    result = EditShortcut(shortcut_id, body.short_cut_key, body.phrase, body.position, body.empresa_id, body.usuario_id)
    return result

# Rota para DELETAR um atalho
@router.delete("/shortcuts/{shortcut_id}")
def delete_of_shortcut(shortcut_id: int, empresa_id: int, usuario_id: int):
    # O ID vem na URL, empresa e usuário vêm como query parameter para garantir que só o dono apaga o atalho
    # Assinatura do service: deleteshortcut(id, empresa_id, usuario_id)
    result = deleteshortcut(shortcut_id, empresa_id, usuario_id)
    return result