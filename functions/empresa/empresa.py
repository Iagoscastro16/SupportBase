from config import conn

def create_empresa(razao_social,nome_fantasia,cnpj):

    # Limpa o cnpj antes de medir: tira espaços das pontas e deixa tudo em maiusculo (o cnpj alfanumérico aceita letras)
    # strings são imutáveis, então o resultado precisa voltar para a variável
    cnpj = cnpj.strip().upper()

    # Verifica se está no tamanho certo
    if len(cnpj) != 14:
        return {
            "success": False,
            "errorMessage": "O CNPJ deve ter 14 caracteres"
        }

    # Verifica se a razao social veio vazia
    razao_social = razao_social.strip()
    if not razao_social:
        return {
            "success": False,
            "errorMessage": "Campo razão social não pode estar vazio"
        }


    try:
        with conn.cursor() as cursor:

            cursor.execute('''
            INSERT INTO empresa (razao_social, nome_fantasia,cnpj) VALUES (%s,%s,%s) RETURNING id
            ''',(razao_social,nome_fantasia,cnpj))

            result = cursor.fetchone()

            conn.commit()

            return {"success": True,
                    "id": result["id"]}
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage":"Não foi possível cadastrar uma nova empresa"}


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
