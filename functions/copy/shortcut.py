#1.  importando a conexão com o banco
from config import conn

def validatePosition(position):
    if not isinstance(position, int):
        return {
            "success": False,
            "errorMessage": "Valor inválido, digite um número inteiro"
        }

    if position < 1 or position > 9:
        return {
            "success": False,
            "errorMessage": "Posição inválida, digite um número entre 1 e 9"
        }

    cursor = None
    try:
        cursor = conn.cursor()

        query_verification = "SELECT id FROM shortcuts WHERE position = %s LIMIT 1"
        cursor.execute(query_verification, (position,))

        result = cursor.fetchone()

        if result is not None:
            return {
                "success": False,
                "errorMessage": "Posição já ocupada, escolha outra"
            }

        return {"success": True}

    except Exception as error:
        print(error)
        return {
            "success": False,
            "errorMessage": "Erro ao validar posição"
        }

    finally:
        if cursor is not None:
            cursor.close()

#2. criando a função de atribuir tecla a frase
def createshortcut(short_cut_key,phrase,position):
    #anotação pq foi dificil fazer, aqui eu estou aproveitando o que veio da função validatePosition, ele já verifica o número do position e no dicionario eu já chamo o erro
    if position is not None:
        result = validatePosition(position)

        if not result["success"]:
            return result
    cursor = None
    try:
        cursor = conn.cursor()
        
        cursor.execute('''
                    
        INSERT INTO shortcuts (short_cut_key,phrase,position) VALUES (%s,%s,%s) 
        ''', (short_cut_key,phrase,position))
        
        conn.commit()
        return {"success": True}
    except Exception as error:
        print(error)
        conn.rollback() 
        return {"success": False,
                "errorMessage": "Erro ao criar atalho"
                }
    
    finally:
        if cursor is not None:
            cursor.close()

    
#3.  criando a função de listar as frases e teclas
def listshortcutByPosition():
    
    cursor = None
    try:
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT short_cut_key, phrase, position
        FROM shortcuts ORDER BY position ASC NULLS LAST
                    ''')
        
        data = cursor.fetchall()
        return {"success": True,
                "data": data}
    except Exception as error:
        print(error)
        return {"success": False,
                "errorMessage": "Erro ao listar atalhos"
                }
    finally:
        if cursor is not None:
            cursor.close()



def listShortcutByDate(ordensEscolhida):
    
    ordem = None
    if ordensEscolhida == "maisAntiga":
        ordem = "created_at ASC"
    elif ordensEscolhida == "maisRecente":
        ordem = "created_at DESC"
    else:
        return {"success": False, 
                "errorMessage": "Ordem inválida"
                }
    
    query = f"SELECT id, created_at,short_cut_key ,phrase, position FROM shortcuts ORDER BY {ordem}"
    cursor = None
    try:
        cursor = conn.cursor()
    
        cursor.execute(query)

        data = cursor.fetchall()
        return {"success": True,
                "data": data}
    except Exception as error:
        print(error)
        return {"success": False,
                "errorMessage": "Erro ao listar atalhos"
                }
    finally:
        if cursor is not None:
            cursor.close()



def EditShortcut(id,short_cut_key,phrase, position):
    cursor = None
    try:
        cursor = conn.cursor()
        shortcut = getShortcutById(cursor,id)
        
        if shortcut == None:
            return {"success": False
                    "errorMessage": "Não existe um atalho para editar"
                    }
        positionToEdit = validateEditPosition(cursor,id,position)
        
        if not positionToEdit["success"]:
            return positionToEdit
            
        updateValue = updateShortcut(cursor, id,short_cut_key, phrase, position)
            if updateValue == 0:
                return {"success": False,
                        "errorMessage": "Erro ao atualizar atalho"
                        }
            else:
                conn.commit()
                return {"success": True,
                        "message": "Atalho atualizado com sucesso"
                        }
    
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Erro geral ao editar atalho"
                }
        
    finally:
        if cursor is not None:
            cursor.close()
    
    
    
def getShortcutById(cursor, shortcut_id):
    
        
    cursor.execute('''
         SELECT * FROM shortcuts WHERE id = %s
                    ''',(shortcut_id,))
        
    shortcut = cursor.fetchone()
    
    return shortcut



def validateEditPosition(cursor, id, position):
    if position == None:
        return {"success": True}
        
        
    if not isinstance(position, int):
        return {
            "success": False,
            "errorMessage": "Valor inválido, digite um número inteiro"
        }
    
        
    if position <1 or position >9:
        return {"success": False,
                "errorMessage": "Posição inválida, digite um número entre 1 e 9"
                }
        
        
    cursor.execute('''
        SELECT id FROM shortcuts WHERE POSITION = %s and id != %s
                   ''',(position,id))
    
    
    result = cursor.fetchone()
    if result is not None:
        return {
            "success": False,
            "errorMessage": "Posição já ocupada, escolha outra"
            }

    return {"success": True}
    

    
def updateShortcut(cursor, id,short_cut_key, phrase, position):
    cursor.execute('''
        UPDATE shortcut set
        short_cut_key = COALESCE(%s, short_cut_key),
        phrase = COALESCE(%s, phrase),
        position = COALESCE(%s,position)
        WHERE id = %s
                   ''',(short_cut_key,phrase,position,id))
    
    return cursor.rowcount

    
    
#7. apagando as atribuições                   
def deleteshortcut(id):
    cursor = None
    try:
        cursor = conn.cursor()
        
        cursor.execute('''
        DELETE FROM shortcuts
        WHERE id = %s
        ''', (id,)            
           
                           )
        if cursor.rowcount == 0:
            return {"success": False,
                    "errorMessage": "Atalho não encontrado"
                    }
        
        conn.commit()
        return {"success": True,
                "message": "Atalho deletado com sucesso"
                } 
    except Exception as error:
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Erro ao deletar atalho"
                }
    finally:
        if cursor is not None:
            cursor.close()    