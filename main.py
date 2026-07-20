# 1. Importa a função da criação das tabelas
from database.tables import createTables
#2. importação do fastAPI
from fastapi import FastAPI
#3. mportação da rota do problems_categories
from routes.problems_categories import router


# 4. Criação das tabelas se não existirem
createTables()

app = FastAPI()

app.include_router(router)