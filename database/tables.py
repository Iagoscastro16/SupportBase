#1. importando a coneção com o banco
from config import conn

#2.  criação das tabelas
def createTables():
    cursor = conn.cursor()
    
    #3. criação da tabela de problemas, com titulo,descrição, solução(opcional), imagem do problema(opcional) e imagem da solução(opcional)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS problems (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            title VARCHAR(80) NOT NULL,
            description VARCHAR(400) NOT NULL,
            solution VARCHAR(800),
            image_problem VARCHAR(255),
            image_solution VARCHAR(255),
            ativo BOOLEAN NOT NULL DEFAULT TRUE
                            )'''
                )

    #4. criação da tabela de categorias, apenas o nome, existe uma tabela que liga a categoria com o problema, pois a relação direta entre as duas é (n:n)
    cursor.execute('''    
        CREATE TABLE IF NOT EXISTS categories(
            id SERIAL PRIMARY KEY,
            name VARCHAR(80) NOT NULL UNIQUE,
            ativo BOOLEAN NOT NULL DEFAULT TRUE
                                )'''
                )

    #5. criação da tabela que liga o problema com a categoria(primeiro cria o campo, depois a chave estrangeira, no final uma chave primaria composta)
    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS problems_categories(
            problem_id INTEGER NOT NULL REFERENCES problems(id) ON DELETE CASCADE,
            category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
            PRIMARY KEY (problem_id, category_id)
                                        )'''
                )
    #6. criação da tabela de configurações, com chave e valor
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            setting_key TEXT PRIMARY KEY ,
            value TEXT NOT NULL
                                )'''
                )
    #7. criação da tabela de atalhos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shortcuts( 
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            short_cut_key VARCHAR(40) NOT NULL UNIQUE,
            phrase VARCHAR(255) NOT NULL,
            position INTEGER UNIQUE CHECK (position >= 1 and position <= 9)
                                    )'''
    )

    conn.commit()