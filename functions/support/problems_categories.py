# importação do conn vindo do config do diretorio raiz, atribuindo ao conn, basicamente as informações do banco
from config import conn

# erros do banco que o usuário consegue corrigir, tratados à parte do except genérico
from psycopg2.errors import UniqueViolation, ForeignKeyViolation

#TODO: Refatoração do código com tratamento de erros.


# Fora o list, é um crud basico também
def create_category_problem(problem_id,category_id,empresa_id):
    
    try:
        with conn.cursor() as cursor:
    
            cursor.execute('''
            INSERT INTO problems_categories (problem_id,category_id,empresa_id) VALUES (%s,%s,%s)
            ''',(problem_id,category_id,empresa_id)
                        )

            conn.commit()
            
            return cursor.rowcount
    # a PK (problem_id, category_id) barra o mesmo vínculo duas vezes
    except UniqueViolation as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Essa categoria já está vinculada ao problema"}
    # as FKs compostas barram problema ou categoria que não existe, ou que é de outra empresa
    except ForeignKeyViolation as error:
        print(error)
        conn.rollback()
        if error.diag.constraint_name == "problems_categories_problem_empresa_fkey":
            mensagem = "Problema não encontrado nessa empresa"
        elif error.diag.constraint_name == "problems_categories_category_empresa_fkey":
            mensagem = "Categoria não encontrada nessa empresa"
        elif error.diag.constraint_name == "problems_categories_empresa_id_fkey":
            mensagem = "Empresa não encontrada"
        else:
            mensagem = "Problema, categoria ou empresa inválido"
        return {"success": False,
                "errorMessage": mensagem}
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Erro ao vincular categoria ao problema"}

def delete_category_problem(problem_id,category_id,empresa_id):
    
    try:
        with conn.cursor() as cursor:
    
            cursor.execute('''
            DELETE FROM problems_categories
            where problem_id = %s and category_id = %s and empresa_id = %s
            ''',(problem_id,category_id,empresa_id)              
                        )
            
            conn.commit()
            
            return cursor.rowcount
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Erro ao excluir vinculo"}

    # Traduzindo esse inner join, ao mesmo tempo, le o id e o nome da categoria, le o id da categoria e verifica qual está batendo com o problem_id.

def list_problems_categories(problem_id,empresa_id):
    
    try:
        with conn.cursor() as cursor:
    
            cursor.execute('''
            SELECT categories.id, categories.name from problems_categories
            INNER JOIN categories on problems_categories.category_id = categories.id
            where problem_id = %s and problems_categories.empresa_id = %s
            ''',(problem_id,empresa_id))
            
            data = cursor.fetchall()
            return {"success": True,
                    "data": data}
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success":False,
                "errorMessage": "Erro ao listar a vinculação entre categorias e problemas"}