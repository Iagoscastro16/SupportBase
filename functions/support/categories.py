# importação do conn vindo do config do diretorio raiz, atribuindo ao conn, basicamente as informações do banco
from config import conn

# TODO: verificar o motivo dessa parte do código não ter o tratamento de erros com try/except/finally
# no mais, é um CRUD básico

def create_category(name):
    try:
        with conn.cursor() as cursor:
        
            cursor.execute('''
            INSERT INTO categories (name) VALUES (%s) RETURNING id
            ''',(name,))
            
            result = cursor.fetchone()

            conn.commit()

            return result[0] if result else None
    except Exception as error:
        print(error)
        conn.rollback()

    return {"success": False,
            "errorMessage": "Ocorreu um erro na criação da categoria"}


def edit_categories(id,name):
    
    try:
        with conn.cursor() as cursor:
    
            cursor.execute('''
            UPDATE categories
            set name = %s
            where id = %s
                        ''',(name,id)   )
            
            conn.commit()

            return cursor.rowcount

    except Exception as error:
            print(error)
            conn.rollback()
    


# retorna todas as categorias
# TODO: Verificar se vai ser necessario a implementação de diferentes formas de visualização das categorias

def list_categories(incluir_inativo=False):

    if incluir_inativo:
        query = "SELECT id, ativo ,name FROM categories"

    else:
        query = "SELECT id, name, ativo FROM categories WHERE ativo = True"


    try:
        with conn.cursor() as cursor:
    
            cursor.execute(query)
            data=cursor.fetchall()
            return {"success": True,
                    "data": data}
    except Exception as error:
        print(error)
        conn.rollback()

        return{"success": False,
               "errorMessage": "Erro ao listar categorias"}

def delete_category(id):
    try:
        with conn.cursor() as cursor:
            
            cursor.execute('''
            UPDATE categories 
            SET ativo = FALSE
            where id = %s
                        ''',(id,)
            )
                        
            conn.commit()

            return cursor.rowcount
        
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Não foi possível inativar a categoria"}
    
