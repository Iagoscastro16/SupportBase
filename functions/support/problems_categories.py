# importação do conn vindo do config do diretorio raiz, atribuindo ao conn, basicamente as informações do banco
from config import conn

#TODO: Refatoração do código com tratamento de erros.


# Fora o list, é um crud basico também
def createCategoryProblem(problem_id,category_id):
    
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO problems_categories (problem_id,category_id) VALUES (%s,%s)
    ''',(problem_id,category_id)
                   )
    
    conn.commit()
    
    return cursor.lastrowid

def deleteCategoryProblem(problem_id,category_id):
    
    cursor = conn.cursor()
    
    cursor.execute('''
    DELETE FROM problems_categories
    where problem_id = %s and category_id = %s
    ''',(problem_id,category_id)              
                   )
    
    conn.commit()
    
    return cursor.rowcount

# Traduzindo esse inner join, ao mesmo tempo, le o id e o nome da categoria, le o id da categoria e verifica qual está batendo com o problem_id.

def listProblemsCategories(problem_id):
    
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT categories.id, categories.name from problems_categories
    INNER JOIN categories on problems_categories.category_id = categories.id
    where problem_id = %s
    ''',(problem_id,))
    
    return cursor.fetchall()