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

            return result["id"] if result else None
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
    filtro = "" if incluir_inativo else "WHERE c.ativo = True"
    query = f"""
    SELECT c.id, c.name, c.ativo,
           COUNT(p.id) AS total_problemas,
           STRING_AGG(p.title, '||') FILTER (WHERE p.id IS NOT NULL) AS titulos
    FROM categories c
    LEFT JOIN problems_categories pc ON pc.category_id = c.id
    LEFT JOIN problems p ON p.id = pc.problem_id AND p.ativo = True
    {filtro}
    GROUP BY c.id, c.name, c.ativo
    ORDER BY c.name ASC
    """
    try:
        with conn.cursor() as cursor:
    
            cursor.execute(query)
            data = cursor.fetchall()
            return {"success": True,
                    "data": data}
    except Exception as error:
        print(error)
        conn.rollback()

        return{"success": False,
               "errorMessage": "Erro ao listar categorias"}

def get_category_id(id):

    try:
        with conn.cursor() as cursor:
            cursor.execute('''
            SELECT id,name,ativo from categories where id = %s
            ''',(id,)
            )

            return cursor.fetchone()
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
        "errorMessage":"Erro ao listar categoria"}


def delete_category(id):
    try:
        with conn.cursor() as cursor:
            
            cursor.execute('''
            SELECT p.id
            FROM problems_categories pc
            INNER JOIN problems p
                ON pc.problem_id = p.id
            WHERE pc.category_id = %s
            AND p.ativo = TRUE;
                        ''',(id,)
            )

            result = cursor.fetchone()

            if result is not None:
                return {"success": False,
                        "errorMessage": "Existe um problema ativo vinculado"}

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
    
