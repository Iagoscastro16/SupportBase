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
def listAssignKeyByPosition():
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT shortCutKey, phrase
    FROM shortcuts ORDER BY position ASC
                ''')
    
    return cursor.fetchall()

def listAssignKeyByDate(ordensEscolhida):
    
    ordem = None

    if ordensEscolhida == "maisAntiga": #trocar quando o front estiver pronto
        ordem = "createdAt ASC"
        
    elif ordensEscolhida == "maisRecente": #trocar quando o front estiver pronto
        ordem = "createdAt DESC"
    
    query = f"SELECT shortCutKey, phrase FROM shortcuts ORDER BY {ordem}"
    
    cursor = conn.cursor()
    
    cursor.execute(query)
    return cursor.fetchall()

def editAssignKey(id,shortCutKey,phrase, position):
    cursor = conn.cursor()
    
    
    cursor.execute('''
    UPDATE shortcuts SET
    shortCutKey = COALESCE (?, shortCutKey),
    phrase = COALESCE (?, phrase),
    position = COALESCE (?, position)
    WHERE id = ?
                   ''',(shortCutKey,phrase,position,id)
    )
                   
    conn.commit()
    
    return cursor.rowcount
                   
#7. apagando as atribuições                   
def deleteShortCutKey(id):
    
    cursor = conn.cursor()
    
    cursor.execute('''
    DELETE FROM shortcuts
    WHERE id = ?
    ''', (id,)               
                   )
    conn.commit()
    
    return cursor.rowcount    

