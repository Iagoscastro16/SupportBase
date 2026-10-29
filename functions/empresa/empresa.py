import re

from config import conn

# erros do banco que o usuário consegue corrigir, tratados à parte do except genérico
from psycopg2.errors import UniqueViolation

def create_empresa(razao_social,nome_fantasia,cnpj):

    # Limpa o cnpj antes de medir: tira espaços das pontas e deixa tudo em maiusculo (o cnpj alfanumérico aceita letras)
    # strings são imutáveis, então o resultado precisa voltar para a variável
    cnpj = cnpj.strip().upper()

    # Verifica o formato: exatamente 14 caracteres, só letras maiúsculas (A-Z) e números
    # o fullmatch exige que a string inteira bata com o padrão, e o len sozinho deixava passar algo como "!!!!!!!!!!!!!!"
    if not re.fullmatch(r"[0-9A-Z]{14}", cnpj):
        return {
            "success": False,
            "errorMessage": "O CNPJ deve ter 14 caracteres, só letras e números"
        }

    # Verifica se a razao social veio vazia
    razao_social = razao_social.strip()
    if not razao_social:
        return {
            "success": False,
            "errorMessage": "Campo razão social não pode estar vazio"
        }

    # nome fantasia é opcional: se vier vazio (ou só espaços), vira None para o banco gravar NULL e não uma string vazia
    # o is not None vem antes do strip(), porque None.strip() levanta AttributeError
    if nome_fantasia is not None:
        nome_fantasia = nome_fantasia.strip() or None

    try:
        with conn.cursor() as cursor:

            cursor.execute('''
            INSERT INTO empresa (razao_social, nome_fantasia,cnpj) VALUES (%s,%s,%s) RETURNING id
            ''',(razao_social,nome_fantasia,cnpj))

            result = cursor.fetchone()

            conn.commit()

            return {"success": True,
                    "id": result["id"]}
    # o único UNIQUE que o create pode violar é o do cnpj
    except UniqueViolation as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Já existe uma empresa com esse CNPJ"}
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage":"Não foi possível cadastrar uma nova empresa"}


# edição parcial com COALESCE: o que vier None mantém o valor antigo
# por isso nome_fantasia só pode ser trocado por outro valor, não limpado (None = "não mexe")
# o cnpj não é editável: a empresa é a raiz do tenant e o cnpj quase nunca muda (YAGNI)
def edit_empresa(id,razao_social=None,nome_fantasia=None):

    # sem nenhum campo, o UPDATE rodaria sem mudar nada e devolveria sucesso, o que enganaria quem chamou
    if razao_social is None and nome_fantasia is None:
        return {"success": False,
                "errorMessage": "Nenhum campo para atualizar"}

    # regra "se veio, valida": o is not None vem antes do strip(), porque None é um valor legítimo aqui (não alterar)
    if razao_social is not None:
        razao_social = razao_social.strip()
        if not razao_social:
            return {"success": False,
                    "errorMessage": "Campo razão social não pode estar vazio"}

    if nome_fantasia is not None:
        nome_fantasia = nome_fantasia.strip()
        if not nome_fantasia:
            return {"success": False,
                    "errorMessage": "Nome fantasia não pode ficar vazio, só pode ser trocado por outro valor"}

    try:
        with conn.cursor() as cursor:

            # sem filtro por empresa_id: o próprio id é o tenant
            cursor.execute('''
            UPDATE empresa
            SET razao_social = COALESCE(%s, razao_social),
                nome_fantasia = COALESCE(%s, nome_fantasia)
            WHERE id = %s
                        ''',(razao_social,nome_fantasia,id))

            conn.commit()

            # rowcount 0 = o id não existe
            if cursor.rowcount == 0:
                return {"success": False,
                        "errorMessage": "Empresa não encontrada"}

            return {"success": True}
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Não foi possível editar a empresa"}


# retorna todas as empresas. Aqui não existe filtro por empresa_id: a própria empresa é o tenant
def list_empresas(incluir_inativo=False):

    filtro = ""

    if not incluir_inativo:
        filtro = "WHERE ativo = True"

    query = f"SELECT id, razao_social, nome_fantasia, cnpj, ativo FROM empresa {filtro}"

    try:
        with conn.cursor() as cursor:

            cursor.execute(query)
            data = cursor.fetchall()
            return {"success": True,
                    "data": data}
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Erro ao listar empresas"}


def get_empresa(id):

    try:
        with conn.cursor() as cursor:

            cursor.execute('''
            SELECT id, razao_social, nome_fantasia, cnpj, ativo FROM empresa WHERE id = %s
            ''',(id,))

            data = cursor.fetchone()

            # fetchone devolve None quando não há linha: não é erro do banco, só não existe
            if data is None:
                return {"success": False,
                        "errorMessage": "Empresa não encontrada"}

            return {"success": True,
                    "data": data}
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Erro ao buscar a empresa"}


# soft delete: não apaga a linha, só marca como inativa
# um DELETE de verdade falharia assim que a empresa tivesse dados, porque todas as FKs para ela são ON DELETE RESTRICT
def delete_empresa(id):

    try:
        with conn.cursor() as cursor:

            cursor.execute('''
            UPDATE empresa
            SET ativo = FALSE
            WHERE id = %s
                        ''',(id,))

            conn.commit()

            # rowcount 0 = o id não existe
            if cursor.rowcount == 0:
                return {"success": False,
                        "errorMessage": "Empresa não encontrada"}

            return {"success": True}
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Não foi possível inativar a empresa"}
