#1. importando a coneção com o banco
from config import conn

#2.  criação das tabelas
def createTables():
    cursor = conn.cursor()
    
    # empresa e usuario vêm primeiro: as outras tabelas têm FK para elas, e o REFERENCES exige que a tabela referenciada já exista
    # criação da tabela de empresas (tenant)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empresa (
        id SERIAL PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        razao_social VARCHAR(150) NOT NULL,
        nome_fantasia VARCHAR(60),
        cnpj VARCHAR(14) NOT NULL UNIQUE,
        ativo BOOLEAN NOT NULL DEFAULT TRUE
                )'''
    )

    # criação da tabela de usuários, cada usuário pertence a uma empresa
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(150) NOT NULL,
        email VARCHAR(256) NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ativo BOOLEAN NOT NULL DEFAULT TRUE,
        empresa_id INTEGER NOT NULL REFERENCES empresa(id) ON DELETE RESTRICT,
        CONSTRAINT usuario_id_empresa_uniq UNIQUE (id, empresa_id)
            )'''
    )

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
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            empresa_id INTEGER NOT NULL REFERENCES empresa(id) ON DELETE RESTRICT,
            CONSTRAINT problems_id_empresa_uniq UNIQUE (id, empresa_id)
                            )'''
                )

    #4. criação da tabela de categorias, apenas o nome, existe uma tabela que liga a categoria com o problema, pois a relação direta entre as duas é (n:n)
    # name não é UNIQUE sozinho: duas empresas podem ter uma categoria com o mesmo nome, só não a mesma empresa duas vezes
    # o CHECK impede nome vazio (ou só espaços) direto no banco, último nível de defesa depois do Pydantic e do service
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories(
            id SERIAL PRIMARY KEY,
            name VARCHAR(80) NOT NULL,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            empresa_id INTEGER NOT NULL REFERENCES empresa(id) ON DELETE RESTRICT,
            CONSTRAINT categories_name_not_blank CHECK (btrim(name) <> ''),
            CONSTRAINT categories_id_empresa_uniq UNIQUE (id, empresa_id)
                                )'''
                )

    # a unicidade ignora caixa e espaços nas pontas: "Rede", "rede" e " rede " são o mesmo nome na mesma empresa
    # UNIQUE inline não aceita expressão, por isso é um índice único separado
    cursor.execute('''
        CREATE UNIQUE INDEX IF NOT EXISTS categories_name_empresa_uniq
        ON categories (lower(btrim(name)), empresa_id)
                    ''')

    #5. criação da tabela que liga o problema com a categoria(primeiro cria o campo, depois a chave estrangeira, no final uma chave primaria composta)
    # as FKs são compostas com empresa_id: o banco recusa vincular um problema de uma empresa a uma categoria de outra
    # por isso problems e categories têm UNIQUE (id, empresa_id), que é o alvo dessas FKs (o id já é único, o par só serve de referência)
    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS problems_categories(
            problem_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            empresa_id INTEGER NOT NULL REFERENCES empresa(id) ON DELETE RESTRICT,
            PRIMARY KEY (problem_id, category_id),
            CONSTRAINT problems_categories_problem_empresa_fkey FOREIGN KEY (problem_id, empresa_id)
                REFERENCES problems(id, empresa_id) ON DELETE CASCADE,
            CONSTRAINT problems_categories_category_empresa_fkey FOREIGN KEY (category_id, empresa_id)
                REFERENCES categories(id, empresa_id) ON DELETE CASCADE
                                        )'''
                )
    #6. criação da tabela de configurações, com chave e valor. Settings é por empresa, por isso a PK é composta
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            setting_key TEXT NOT NULL,
            value TEXT NOT NULL,
            empresa_id INTEGER NOT NULL REFERENCES empresa(id) ON DELETE RESTRICT,
            PRIMARY KEY (empresa_id, setting_key)
                                )'''
                )
    #7. criação da tabela de atalhos, os atalhos são pessoais (escopo por usuário), por isso os UNIQUE usam usuario_id
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shortcuts( 
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            short_cut_key VARCHAR(40) NOT NULL,
            phrase VARCHAR(255) NOT NULL,
            position INTEGER CHECK (position >= 1 and position <= 9),
            empresa_id INTEGER NOT NULL REFERENCES empresa(id) ON DELETE RESTRICT,
            usuario_id INTEGER NOT NULL,
            CONSTRAINT shortcuts_usuario_empresa_fkey FOREIGN KEY (usuario_id, empresa_id)
                REFERENCES usuario(id, empresa_id) ON DELETE RESTRICT,
            UNIQUE (short_cut_key, usuario_id),
            UNIQUE (position, usuario_id)
                                    )'''
    )

    conn.commit()