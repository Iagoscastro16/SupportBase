#1. importando a coneção com o banco
from config import conn

#2.  criação das tabelas
def createTables():
    cursor = conn.cursor()
    
    #3. criação da tabela de problemas, com titulo,descrição, solução(opcional), imagem do problema(opcional) e imagem da solução(opcional)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(50) NOT NULL,
            description TEXT NOT NULL,
            solution TEXT,
            imageProblem TEXT,
            imageSolution TEXT
                            )'''
                )

    #4. criação da tabela de categorias, apenas o nome, existe uma tabela que liga a categoria com o problema, pois a relação direta entre as duas é (n:n)
    cursor.execute('''    
        CREATE TABLE IF NOT EXISTS categories(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
                                )'''
                )

    #5. criação da tabela que liga o problema com a categoria
    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS problems_categories(
            problem_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            PRIMARY KEY (problem_id, category_id)
                                        )'''
                )
    #6. criação da tabela de configurações, com chave e valor
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL,
            value TEXT NOT NULL
                                )'''
                )
    #7. criação da tabela de atalhos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shortcuts( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shortCutKey TEXT NOT NULL,
            phrase TEXT,
            position INTEGER
                                    )'''
    )

    conn.commit()