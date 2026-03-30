#1. importando a coneção com o banco
from config import conn

#2.  criação das tabelas
def createTables():
    cursor = conn.cursor()
    
    #3. criação da tabela de problemas, com titulo,descrição, solução(opcional), imagem do problema(opcional) e imagem da solução(opcional)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
            title TEXT NOT NULL,
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
            name TEXT NOT NULL UNIQUE
                                )'''
                )

    #5. criação da tabela que liga o problema com a categoria(primeiro cria o campo, depois a chave estrangeira, no final uma chave primaria composta)
    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS problems_categories(
            problem_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY(problem_id) REFERENCES problems(id) ON DELETE CASCADE,
            FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE CASCADE,
            PRIMARY KEY (problem_id, category_id)
                                        )'''
                )
    #6. criação da tabela de configurações, com chave e valor
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            settingKey TEXT NOT NULL UNIQUE,
            value TEXT NOT NULL
                                )'''
                )
    #7. criação da tabela de atalhos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shortcuts( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
            shortCutKey TEXT NOT NULL UNIQUE,
            phrase TEXT,
            position INTEGER
                                    )'''
    )

    conn.commit()