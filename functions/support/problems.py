from config import conn

def createProblem(title,description,solution,image_problem,image_solution):
    
    cursor = conn.cursor()
    
    
    cursor.execute('''
    INSERT INTO problems (title,description,solution, image_problem, image_solution) VALUES(%s,%s,%s,%s,%s)
                   ''',(title,description,solution,image_problem,image_solution))
    
    conn.commit()
    
    return cursor.lastrowid

def listProblemsByTitle():
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, title 
    FROM problems order by title ASC
                   ''')
    
    return cursor.fetchall()

def listProblemsByDate(ordensEscolhida):
    
    ordem = None
    
    if ordensEscolhida == "maisAntiga": #Trocar quanto o front estiver pronto
        
        ordem = "created_at ASC"
        
    elif ordensEscolhida == "maisRecente": #Trocar quanto o front estiver pronto
        
        ordem = "created_at DESC"
        
    query = f"SELECT id, title FROM problems ORDER BY {ordem}"
    
    cursor = conn.cursor()
    
    cursor.execute(query)
    return cursor.fetchall()


def getProblem(id):
    
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * from problems where id = %s
                   ''',(id,)
                   )
                   
    return cursor.fetchone()


def editProblems(id,title,description,solution,image_problem,image_solution):
    cursor = conn.cursor()
    
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
    
def deleteProblems(id):
    cursor = conn.cursor()
    
    
    cursor.execute('''
    DELETE FROM problems
    WHERE id = %s
    ''',(id,)
    )
    
    conn.commit()
    
    
    return cursor.rowcount