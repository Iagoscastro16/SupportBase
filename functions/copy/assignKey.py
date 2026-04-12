#1.  importando a conexão com o banco
from config import conn

#2. criando a função de atribuir tecla a frase
def createAssignKey(short_cut_key,phrase):
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO shortcuts (short_cut_key,phrase) VALUES (%s,%s) 
    ''', (short_cut_key,phrase))
    
    conn.commit()
    
    return cursor.lastrowid

#3.  criando a função de listar as frases e teclas
def listAssignKeyByPosition():
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT short_cut_key, phrase
    FROM shortcuts ORDER BY position ASC
                ''')
    
    return cursor.fetchall()

def listAssignKeyByDate(ordensEscolhida):
    
    ordem = None

    if ordensEscolhida == "maisAntiga": #trocar quando o front estiver pronto
        ordem = "created_at ASC"
        
    elif ordensEscolhida == "maisRecente": #trocar quando o front estiver pronto
        ordem = "created_at DESC"
    
    query = f"SELECT short_cut_key, phrase FROM shortcuts ORDER BY {ordem}"
    
    cursor = conn.cursor()
    
    cursor.execute(query)
    return cursor.fetchall()

def editAssignKey(id,short_cut_key,phrase, position):
    cursor = conn.cursor()
    
    
    cursor.execute('''
    UPDATE shortcuts SET
    short_cut_key = COALESCE (%s, short_cut_key),
    phrase = COALESCE (%s, phrase),
    position = COALESCE (%s, position)
    WHERE id = %s
                   ''',(short_cut_key,phrase,position,id)
    )
                   
    conn.commit()
    
    return cursor.rowcount
                   
#7. apagando as atribuições                   
def deleteShortCutKey(id):
    
    cursor = conn.cursor()
    
    cursor.execute('''
    DELETE FROM shortcuts
    WHERE id = %s
    ''', (id,)               
                   )
    conn.commit()
    
    return cursor.rowcount    

