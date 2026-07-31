#1.  importando a conexão com o banco
from config import conn

# ValidatePosition verifica se o número é inteiro com o isinstance, tanto se é número inteiro quanto se está entre 1 e 9, depois dá select em um dos atalhos e verifica se aquele atalho está disponivel
def validatePosition(position):
    # Primeira barreira: garante que position é um inteiro. O isinstance evita erros silenciosos com strings como "5"
    if not isinstance(position, int):
        return {
            "success": False,
            "errorMessage": "Valor inválido, digite um número inteiro"
        }

    # Segunda barreira: regra de negócio — só existem 9 posições possíveis (1 a 9)
    if position < 1 or position > 9:
        return {
            "success": False,
            "errorMessage": "Posição inválida, digite um número entre 1 e 9"
        }

    cursor = None
    try:
        cursor = conn.cursor()

        # Consulta enxuta: só precisa do id para saber se a posição já existe, não precisa trazer colunas desnecessárias
        query_verification = "SELECT id FROM shortcuts WHERE position = %s LIMIT 1"
        cursor.execute(query_verification, (position,))

        result = cursor.fetchone()

        # Se encontrou algo, a posição já está ocupada por outro atalho
        if result is not None:
            return {
                "success": False,
                "errorMessage": "Posição já ocupada, escolha outra"
            }

        # Se chegou até aqui, passou por todas as validações
        return {"success": True}

    except Exception as error:
        # Loga o erro no console para debug, mas retorna mensagem amigável para o usuário
        print(error)
        return {
            "success": False,
            "errorMessage": "Erro ao validar posição"
        }

    finally:
        # Sempre fecha o cursor, mesmo se deu erro — evita vazamento de recurso
        if cursor is not None:
            cursor.close()

#2. criando a função de atribuir tecla a frase
def createshortcut(short_cut_key,phrase,position):
    #anotação pq foi dificil fazer, aqui eu estou aproveitando o que veio da função validatePosition, ele já verifica o número do position e no dicionario eu já chamo o erro
    # Reprova cedo: se a posição for inválida, nem chega a abrir conexão para o INSERT
    if position is not None:
        result = validatePosition(position)

        # Se validatePosition retornou success False, repassa o erro direto para quem chamou
        if not result["success"]:
            return result
    
    # Observação: aqui não há validação de short_cut_key e phrase — se vierem vazios ou None, vão entrar no banco assim.
    # Vale pensar em adicionar uma validação tipo "if not short_cut_key or not phrase: return erro"
    
    cursor = None
    try:
        cursor = conn.cursor()
        
        # INSERT simples passando os 3 campos. Como position pode ser None, vai gravar NULL na coluna (se ela permitir)
        cursor.execute('''
                    
        INSERT INTO shortcuts (short_cut_key,phrase,position) VALUES (%s,%s,%s) 
        ''', (short_cut_key,phrase,position))
        
        # commit obrigatório aqui porque o INSERT só é efetivado de fato após o commit
        conn.commit()
        return {"success": True}
    except Exception as error:
        # rollback garante que uma falha parcial não deixe a transação "presa"
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
    # Não recebe parâmetros — sempre retorna todos os atalhos ordenados por posição
    
    cursor = None
    try:
        cursor = conn.cursor()
        
        # NULLS LAST é o detalhe legal aqui: joga os atalhos sem posição para o final da lista,
        # mantendo os que têm posição numerada aparecendo primeiro (mais organizado para o usuário)
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
    # Essa função permite listar ordenando por data — mais antiga primeiro ou mais recente primeiro
    
    # Mapeia a escolha do usuário para o trecho SQL correspondente
    # IMPORTANTE: como o controle é feito com if/elif (e não concatenando input direto), não há risco de SQL injection aqui.
    # O f-string só recebe uma das duas strings fixas que nós mesmos definimos.
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
    # Função orquestradora do fluxo de edição: busca o atalho, valida a posição, atualiza e commita
    # Padrão diferente do createshortcut: aqui o cursor é criado uma vez e repassado para as funções auxiliares,
    # evitando abrir e fechar cursor várias vezes dentro da mesma operação
    #TODO: createshortcut, não há validação de short_cut_key e phrase vazios/None, Tratar disso futuramente
    
    cursor = None
    try:
        cursor = conn.cursor()
        # Primeiro verifica se o atalho existe — não faz sentido editar algo que não está lá
        shortcut = getShortcutById(cursor,id)
        
        if shortcut == None:
            return {"success": False,
                    "errorMessage": "Não existe um atalho para editar"
                    }
        # Validação específica para edição: permite manter a posição atual (id != %s na query interna)
        positionToEdit = validateEditPosition(cursor,id,position)
        
        if not positionToEdit["success"]:
            return positionToEdit
            
        # Se passou nas validações, tenta atualizar. updateShortcut retorna rowcount
        updateValue = updateShortcut(cursor, id,short_cut_key, phrase, position)
        if updateValue == 0:
            # rowcount 0 = nenhuma linha afetada, geralmente id inexistente (já checado acima, mas é uma proteção extra)
            return {"success": False,
                    "errorMessage": "Erro ao atualizar atalho"
                    }
        else:
            # Só commita depois que confirmou que o UPDATE afetou alguma linha
            conn.commit()
            return {"success": True,
                    "message": "Atalho atualizado com sucesso"
                    }
    
    except Exception as error:
        # Rollback para desfazer qualquer alteração pendente em caso de erro
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Erro geral ao editar atalho"
                }
        
    finally:
        if cursor is not None:
            cursor.close()
    
    
    
def getShortcutById(cursor, shortcut_id):
    # Função auxiliar que reaproveita o cursor aberto pela função chamadora (não fecha aqui dentro)
    # Retorna a linha completa do atalho — útil tanto para validar existência quanto para leitura de campos
        
    cursor.execute('''
         SELECT * FROM shortcuts WHERE id = %s
                    ''',(shortcut_id,))
        
    shortcut = cursor.fetchone()
    
    return shortcut



def validateEditPosition(cursor, id, position):
    # Versão "edit" da validatePosition: recebe o cursor por parâmetro e exclui o próprio id da busca.
    # Isso permite que o usuário mantenha a mesma posição do atalho que está editando sem disparar "posição ocupada".
    
    # Se position veio None, significa que o usuário não quer alterar a posição — deixa seguir
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
        
        
    # Ponto chave da diferença: "id != %s" garante que a posição só é considerada ocupada se pertencer a OUTRO atalho
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
    # UPDATE parcial usando COALESCE: se algum campo vier None, mantém o valor que já estava no banco.
    # Isso permite editar só alguns campos sem precisar passar todos — bem prático para formulários parciais.
    

    cursor.execute('''
        UPDATE shortcuts set
        short_cut_key = COALESCE(%s, short_cut_key),
        phrase = COALESCE(%s, phrase),
        position = COALESCE(%s,position)
        WHERE id = %s
                   ''',(short_cut_key,phrase,position,id))
    
    # rowcount informa quantas linhas foram afetadas pelo UPDATE — 0 significa que o id não foi encontrado
    return cursor.rowcount

    
    
#7. apagando as atribuições                   
def deleteshortcut(id):
    # Deleta o atalho pelo id. Usa rowcount para distinguir entre "deletou" e "não achou nada para deletar"
    
    cursor = None
    try:
        cursor = conn.cursor()
        
        cursor.execute('''
        DELETE FROM shortcuts
        WHERE id = %s
        ''', (id,)            
           
                           )
        # Se nenhuma linha foi afetada, é porque o id não existia — evita dar "sucesso" em uma exclusão fantasma
        if cursor.rowcount == 0:
            return {"success": False,
                    "errorMessage": "Atalho não encontrado"
                    }
        
        conn.commit()
        return {"success": True,
                "message": "Atalho deletado com sucesso"
                } 
    except Exception as error:
        # Rollback por segurança — se algo quebrou no meio do caminho, nada deve ser persistido
        print(error)
        conn.rollback()
        return {"success": False,
                "errorMessage": "Erro ao deletar atalho"
                }
    finally:
        if cursor is not None:
            cursor.close()    