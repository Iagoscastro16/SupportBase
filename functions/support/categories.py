# importação do conn vindo do config do diretorio raiz, atribuindo ao conn, basicamente as informações do banco
from config import conn

# no mais, é um CRUD básico

def create_category(name,empresa_id):
    try:
        with conn.cursor() as cursor:
        
            cursor.execute('''
            INSERT INTO categories (name,empresa_id) VALUES (%s,%s) RETURNING id
            ''',(name,empresa_id))
            
            result = cursor.fetchone()

            conn.commit()

            return result["id"] if result else None
    except Exception as error:
        print(error)
        conn.rollback()

        return {"success": False,
                "errorMessage": "Ocorreu um erro na criação da categoria"}


def edit_categories(id,name,empresa_id):
    
    try:
        with conn.cursor() as cursor:
    
            cursor.execute('''
            UPDATE categories
            SET name = %s
            WHERE id = %s AND empresa_id = %s
                        ''',(name,id,empresa_id)   )
            
            conn.commit()

            return cursor.rowcount

    except Exception as error:
        print(error)
        conn.rollback()

        return {"success": False,
                "errorMessage":"Ocorreu um erro na edição da categoria"}
    


# retorna todas as categorias
# TODO: Verificar se vai ser necessario a implementação de diferentes formas de visualização das categorias

def list_categories(empresa_id,incluir_inativo=False):

    filtro = "WHERE empresa_id = %s"

    if not incluir_inativo:
        filtro += " AND ativo = True"

    query = f"SELECT id, name, ativo FROM categories {filtro} "


    try:
        with conn.cursor() as cursor:

            cursor.execute(query,(empresa_id,))
            data=cursor.fetchall()
            return {"success": True,
                    "data": data}
    except Exception as error:
        print(error)
        conn.rollback()

        return{"success": False,
               "errorMessage": "Erro ao listar categorias"}

def get_category_id(id,empresa_id):

    try:
        with conn.cursor() as cursor:
            cursor.execute('''
            SELECT id,name,ativo from categories where id = %s and empresa_id = %s
            ''',(id,empresa_id)
            )

            return cursor.fetchone()
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
        "errorMessage":"Erro ao listar categoria"}


def delete_category(id,empresa_id):
    try:
        with conn.cursor() as cursor:
            
            cursor.execute('''
            UPDATE categories 
            SET ativo = FALSE
            where id = %s and empresa_id = %s
                        ''',(id,empresa_id)
            )
                        
            conn.commit()

            return cursor.rowcount
        
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Não foi possível inativar a categoria"}
    
