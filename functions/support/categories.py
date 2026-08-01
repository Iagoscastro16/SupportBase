# importação do conn vindo do config do diretorio raiz, atribuindo ao conn, basicamente as informações do banco
from config import conn

# TODO: verificar o motivo dessa parte do código não ter o tratamento de erros com try/except/finally
# no mais, é um CRUD básico

def createCategory(name):
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO categories (name) VALUES (%s) RETURNING id
    ''',(name,))
    
    result = cursor.fetchone()

    conn.commit()

    return result[0] if result else None


def editCategories(id,name):
    
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE categories
    set name = %s
    where id = %s
                ''',(name,id)   )
    
    conn.commit()
    
    return cursor.rowcount

# retorna todas as categorias
# TODO: Verificar se vai ser necessario a implementação de diferentes formas de visualização das categorias

def listCategories():
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, name FROM categories
                   ''')
    
    return cursor.fetchall()


def deleteCategory(id):
    cursor = conn.cursor()
    
    cursor.execute('''
    DELETE FROM categories
    where id = %s
                   ''',(id,)
    )
                   
    conn.commit()
    
    return cursor.rowcount