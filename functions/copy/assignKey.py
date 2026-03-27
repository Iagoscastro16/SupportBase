#1.  importando a conexão com o banco
from config import conn
#2. criando a função de atribuir tecla a frase
def createAssignKey(shortCutKey,phrase):
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO shortcuts (shortCutKey,phrase) VALUES (?,?) 
    ''', (shortCutKey,phrase))
    
    conn.commit()
    
    return cursor.lastrowid

#3.  criando a função de listar as frases e teclas
def listAssignKey():
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT shortCutKey, phrase
    FROM shortcuts ORDER BY position ASC
                ''')
    
return cursor.fetchall()

#4. Edita a tecla de um atalho
def editShortCutKey(id, shortCutKey):
    cursor = conn.cursor()
    
    
    cursor.execute('''
    UPDATE shortcuts
    SET shortCutKey = ?
    where id = ?
    ''', (id,shortCutKey ))
    
    conn.commit()
    
    return cursor.lastrowid

#5. Edita a frase de um atalho
def editPhrase(id, phrase):
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE shortcuts
    SET phrase = ?
    where id = ?
    ''', (id,phrase))
    
    conn.commit()
    
    return cursor.lastrowid

#6. Edita a posição de um atalho             
def editPosition(id, position):
    
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE shortcuts
    set position = ?
    where id = ?
    ''', (id, position)
    )
    conn.commit()
    
     return cursor.lastrowid
                   
#7. apagando as atribuições                   
def deleteShortCutKey(id):
    
    cursor = conn.cursor()
    
    cursor.execute('''
    DELETE FROM shortcuts
    where id = ?
    ''', (id,)               
                   )
    conn.commit()
    
    return cursor.lastrowid     

