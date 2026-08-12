# importação do conn vindo do config do diretorio raiz, atribuindo ao conn, basicamente as informações do banco
from config import conn

# TODO: Refatorar depois para a adição de tratamento de erros, é o coração da aplicação

def create_problem(title,description,solution,image_problem,image_solution):
    
    try:
        with conn.cursor() as cursor:
    
            cursor.execute('''
            INSERT INTO problems (title,description,solution, image_problem, image_solution) VALUES(%s,%s,%s,%s,%s) RETURNING id
                        ''',(title,description,solution,image_problem,image_solution))

            result = cursor.fetchone()
            
            conn.commit()
            
            return result["id"] if result else None
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Não foi possível criar um problema novo"}

# Lista os problemas em ordem alfabetica

def listProblemsByTitle(incluir_inativos=False):

    if incluir_inativos:
        query = '''SELECT p.id, p.title, p.ativo, STRING_AGG(c.name, ', ') AS categorias
        FROM problems p
        LEFT JOIN problems_categories pc ON pc.problem_id = p.id
        LEFT JOIN categories c ON c.id = pc.category_id
        GROUP BY p.id, p.title, p.ativo
        ORDER BY p.title ASC'''
        
    else:

        query = '''SELECT p.id, p.title, p.ativo, STRING_AGG(c.name, ', ') AS categorias
        FROM problems p
        LEFT JOIN problems_categories pc ON pc.problem_id = p.id
        LEFT JOIN categories c ON c.id = pc.category_id
        WHERE p.ativo = True
        GROUP BY p.id, p.title, p.ativo
        ORDER BY p.title ASC'''

    try:
        with conn.cursor() as cursor:
    
            cursor.execute(query)
            data = cursor.fetchall()
            
            return {"success": True,
                    "data":data}
    except Exception as error:
        print(error)
        conn.rollback()

        return {"success": False,
                "errorMessage": "Erro ao listar os problemas pelo titulo"}

# Lista de problemas filtrada pela data mais antiga ou mais nova

def listProblemsByDate(ordemEscolhida, incluir_inativo=False):
    
    ordem = None
    filtro = None

    if incluir_inativo:
        filtro = ""

    else:
        filtro = ("WHERE ativo = True")
        
    
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
    
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as error:
        print(error)
        conn.rollback()
        return{"success": False,
               "errorMessage": "Erro ao listar problemas pela data"}


def get_problem(id):
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
            SELECT p.id, p.created_at, p.title, p.description, p.solution,
                   p.image_problem, p.image_solution, p.ativo,
                   STRING_AGG(c.name, ', ') AS categorias
            FROM problems p
            LEFT JOIN problems_categories pc ON pc.problem_id = p.id
            LEFT JOIN categories c ON c.id = pc.category_id
            WHERE p.id = %s
            GROUP BY p.id, p.created_at, p.title, p.description, p.solution,
                     p.image_problem, p.image_solution, p.ativo
            ''', (id,))
            return cursor.fetchone()
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False, "errorMessage": "Erro ao listar problemas"}

# Edição completa dos problemas 

def edit_problems(id,title,description,solution,image_problem,image_solution):
    try:
        with conn.cursor() as cursor:
    
            cursor.execute('''
            UPDATE problems SET 
            title = COALESCE (%s, title),
            description = COALESCE (%s,description),
            solution = COALESCE (%s,solution),
            image_problem = COALESCE (%s,image_problem),
            image_solution = COALESCE (%s, image_solution)
            WHERE id = %s
                            ''',(title,description,solution,image_problem,image_solution,id)
            )

            conn.commit()
            return cursor.rowcount
            
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Erro ao editar problema"}


def search_problems(query):
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
            SELECT p.id, p.title, p.ativo, STRING_AGG(c.name, ', ') AS categorias
            FROM problems p
            LEFT JOIN problems_categories pc ON pc.problem_id = p.id
            LEFT JOIN categories c ON c.id = pc.category_id
            WHERE p.ativo = True AND (p.title ILIKE %s OR p.description ILIKE %s)
            GROUP BY p.id, p.title, p.ativo
            ORDER BY p.title ASC
            ''', (f"%{query}%", f"%{query}%"))

            data = cursor.fetchall()

            return {"success": True, "data": data}
        
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False, "errorMessage": "Erro ao buscar problemas"}
    
def delete_problems(id):
    try:
        with conn.cursor() as cursor:

            cursor.execute('''
            UPDATE PROBLEMS
            SET ativo = FALSE
            WHERE id = %s
            ''',(id,)
            )
            
            conn.commit()
            return cursor.rowcount
        
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Não foi possivel inativar o problema"}