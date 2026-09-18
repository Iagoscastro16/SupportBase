# importação do conn vindo do config do diretorio raiz, atribuindo ao conn, basicamente as informações do banco
from config import conn

def create_problem(title,description,solution,image_problem,image_solution,empresa_id):
    
    try:
        with conn.cursor() as cursor:
    
            cursor.execute('''
            INSERT INTO problems (title,description,solution, image_problem, image_solution, empresa_id) VALUES(%s,%s,%s,%s,%s, %s) RETURNING id
                        ''',(title,description,solution,image_problem,image_solution, empresa_id))

            result = cursor.fetchone()
            
            conn.commit()
            
            return result["id"] if result else None
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
            return cursor.fetchall()
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

            return cursor.fetchone()

    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage":"Erro ao listar problemas"}

# Edição completa dos problemas 

def edit_problems(id,title,description,solution,image_problem,image_solution, empresa_id):
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
            return cursor.rowcount
            
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
            return cursor.rowcount
        
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Não foi possivel inativar o problema"}