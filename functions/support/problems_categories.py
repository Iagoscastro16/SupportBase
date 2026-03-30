from config import conn

def createCategoryProblem(problem_id,category_id):
    
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO problems_categories (problem_id,category_id) VALUES (?,?)
    ''',(problem_id,category_id)
                   )
    
    conn.commit()
    
    return cursor.lastrowid

def deleteCategoryProblem(problem_id,category_id):
    
    cursor = conn.cursor()
    
    cursor.execute('''
    DELETE FROM problems_categories
    where problem_id = ? and category_id = ?
    ''',(problem_id,category_id)              
                   )
    
    conn.commit()
    
    return cursor.rowcount

def listProblemsCategories(problem_id):
    
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT categories.id, categories.name from problems_categories
    INNER JOIN categories on problems_categories.category_id = categories.id
    where problem_id = ?
    ''',(problem_id,))
    
    return cursor.fetchall()