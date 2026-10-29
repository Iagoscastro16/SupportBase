# importação do conn vindo do config do diretorio raiz, atribuindo ao conn, basicamente as informações do banco
from config import conn

# erros do banco que o usuário consegue corrigir, tratados à parte do except genérico
from psycopg2.errors import ForeignKeyViolation

def create_problem(title,description,solution,image_problem,image_solution,empresa_id):

    # title e description são NOT NULL no banco: limpa e rejeita vazio antes de abrir o cursor
    title = title.strip()
    if not title:
        return {"success": False,
                "errorMessage": "O título do problema não pode ser vazio"}

    description = description.strip()
    if not description:
        return {"success": False,
                "errorMessage": "A descrição do problema não pode ser vazia"}

    # solution e as imagens são opcionais: se vierem vazias (ou só espaços) viram None, para o banco gravar NULL e não uma string vazia
    # o is not None vem antes do strip(), porque None.strip() levanta AttributeError
    if solution is not None:
        solution = solution.strip() or None
    if image_problem is not None:
        image_problem = image_problem.strip() or None
    if image_solution is not None:
        image_solution = image_solution.strip() or None

    try:
        with conn.cursor() as cursor:

            cursor.execute('''
            INSERT INTO problems (title,description,solution, image_problem, image_solution, empresa_id) VALUES(%s,%s,%s,%s,%s, %s) RETURNING id
                        ''',(title,description,solution,image_problem,image_solution, empresa_id))

            result = cursor.fetchone()

            conn.commit()

            return {"success": True,
                    "id": result["id"]}
    # empresa_id que não existe na tabela empresa
    except ForeignKeyViolation as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Empresa não encontrada"}
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Não foi possível criar um problema novo"}

# Lista os problemas em ordem alfabetica

def listProblemsByTitle(empresa_id,incluir_inativos=False):
    filtro = "WHERE empresa_id = %s"

    if not incluir_inativos:
        filtro += " AND ativo = True"
    query = f"SELECT id,title, ativo FROM problems {filtro} order by title ASC"
    try:
        with conn.cursor() as cursor:

            cursor.execute(query,(empresa_id,))
            data = cursor.fetchall()

            return {"success": True,
                    "data":data}
    except Exception as error:
        print(error)
        conn.rollback()

        return {"success": False,
                "errorMessage": "Erro ao listar os problemas pelo titulo"}

# Lista de problemas filtrada pela data mais antiga ou mais nova

def listProblemsByDate(ordemEscolhida,empresa_id, incluir_inativo=False):

    ordem = None
    filtro = "WHERE empresa_id = %s"

    if not incluir_inativo:
        filtro += (" AND ativo = True")


    if ordemEscolhida == "maisAntiga": #Trocar quanto o front estiver pronto

        ordem = "created_at ASC"

    elif ordemEscolhida == "maisRecente": #Trocar quanto o front estiver pronto

        ordem = "created_at DESC"

    else:
        return {"success": False,
                "errorMessage":"Ordem escolhida inválida"}

    query = f"SELECT id, title, ativo FROM problems {filtro} ORDER BY {ordem}"

    try:
        with conn.cursor() as cursor:

            cursor.execute(query,(empresa_id,))
            data = cursor.fetchall()

            # antes devolvia a lista solta: agora segue o mesmo formato do listProblemsByTitle
            return {"success": True,
                    "data": data}
    except Exception as error:
        print(error)
        conn.rollback()
        return{"success": False,
               "errorMessage": "Erro ao listar problemas pela data"}


def get_problem(id,empresa_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
            SELECT id,created_at,title,description,solution,image_problem,image_solution, ativo from problems where id = %s and empresa_id = %s
                        ''',(id,empresa_id)
                        )

            data = cursor.fetchone()

            # fetchone devolve None quando não há linha: não é erro do banco, só não existe (ou é de outra empresa)
            if data is None:
                return {"success": False,
                        "errorMessage": "Problema não encontrado"}

            return {"success": True,
                    "data": data}

    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage":"Erro ao listar problemas"}

# Edição completa dos problemas
# edição parcial com COALESCE: o que vier None mantém o valor antigo
# por isso nenhum campo pode ser limpado, só trocado por outro valor (None = "não mexe")

def edit_problems(id,title,description,solution,image_problem,image_solution, empresa_id):

    # sem nenhum campo, o UPDATE rodaria sem mudar nada e devolveria sucesso, o que enganaria quem chamou
    if all(campo is None for campo in (title,description,solution,image_problem,image_solution)):
        return {"success": False,
                "errorMessage": "Nenhum campo para atualizar"}

    # regra "se veio, valida": o is not None vem antes do strip(), porque None é um valor legítimo aqui (não alterar)
    # uma string vazia não é None: o COALESCE gravaria "" por cima do valor antigo, então vazio é erro
    if title is not None:
        title = title.strip()
        if not title:
            return {"success": False,
                    "errorMessage": "O título do problema não pode ser vazio"}

    if description is not None:
        description = description.strip()
        if not description:
            return {"success": False,
                    "errorMessage": "A descrição do problema não pode ser vazia"}

    if solution is not None:
        solution = solution.strip()
        if not solution:
            return {"success": False,
                    "errorMessage": "A solução não pode ficar vazia, só pode ser trocada por outro valor"}

    if image_problem is not None:
        image_problem = image_problem.strip()
        if not image_problem:
            return {"success": False,
                    "errorMessage": "A imagem do problema não pode ficar vazia, só pode ser trocada por outro valor"}

    if image_solution is not None:
        image_solution = image_solution.strip()
        if not image_solution:
            return {"success": False,
                    "errorMessage": "A imagem da solução não pode ficar vazia, só pode ser trocada por outro valor"}

    try:
        with conn.cursor() as cursor:

            cursor.execute('''
            UPDATE problems SET
            title = COALESCE (%s, title),
            description = COALESCE (%s,description),
            solution = COALESCE (%s,solution),
            image_problem = COALESCE (%s,image_problem),
            image_solution = COALESCE (%s, image_solution)
            WHERE id = %s and empresa_id = %s
                            ''',(title,description,solution,image_problem,image_solution,id,empresa_id)
            )

            conn.commit()

            # rowcount 0 = o id não existe, ou pertence a outra empresa
            if cursor.rowcount == 0:
                return {"success": False,
                        "errorMessage": "Problema não encontrado"}

            return {"success": True}

    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Erro ao editar problema"}


def delete_problems(id,empresa_id):
    try:
        with conn.cursor() as cursor:

            cursor.execute('''
            UPDATE PROBLEMS
            SET ativo = FALSE
            WHERE id = %s and empresa_id = %s
            ''',(id,empresa_id)
            )

            conn.commit()

            # rowcount 0 = o id não existe, ou pertence a outra empresa
            if cursor.rowcount == 0:
                return {"success": False,
                        "errorMessage": "Problema não encontrado"}

            return {"success": True}

    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Não foi possivel inativar o problema"}
