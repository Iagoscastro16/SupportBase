from config import conn

def createCategory(name):
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO categories (name) VALUES (?)
    ''',(name,))
    
    conn.commit()
    
    return cursor.lastrowid


def editCategories(id,name):
    
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE categories
    set name = ?
    where id = ?
                ''',(name,id)   )
    
    conn.commit()
    
    return cursor.rowcount


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
    where id = ?
                   ''',(id,)
    )
                   
    conn.commit()
    
    return cursor.rowcount