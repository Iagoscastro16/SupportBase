from config import conn

def createProblem(title,description,solution,imageProblem,imageSolution):
    
    cursor = conn.cursor()
    
    
    cursor.execute('''
    INSERT INTO problems (title,description,solution, imageProblem, imageSolution) VALUES(?,?,?,?,?)
                   ''',(title,description,solution,imageProblem,imageSolution))
    
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
        
        ordem = "createdAt ASC"
        
    elif ordensEscolhida == "maisRecente": #Trocar quanto o front estiver pronto
        
        ordem = "createdAt DESC"
        
    query = f"SELECT id, title FROM problems ORDER BY {ordem}"
    
    cursor = conn.cursor()
    
    cursor.execute(query)
    return cursor.fetchall()


def getProblem(id):
    
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * from problems where id = ?
                   ''',(id,)
                   )
                   
    return cursor.fetchonne()


def editProblems(id,title,description,solution,imageProblem,imageSolution):
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE problems SET 
    title = COALESCE (?, title),
    description = COALESCE (?,description),
    solution = COALESCE (?,solution),
    imageProblem = COALESCE (?,imageProblem),
    imageSolution = COALESCE (?, imageSolution)
    WHERE id = ?
                    ''',(title,description,solution,imageProblem,imageSolution,id)
    
    conn.commit()
    
    return cursor.rowcount
    
def deleteProblems(id):
    cursor = conn.cursor()
    
    
    cursor.execute('''
    DELETE FROM problems
    WHERE id = ?
    ''',(id,)
    )
    
    conn.commit()
    
    
    return cursor.rowcount