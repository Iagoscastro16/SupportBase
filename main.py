#Importa a função da criação das tabelas
from database.tables import createTables
#importação do fastAPI
from fastapi import FastAPI
# Importação do staticfiles para o html
from fastapi.staticfiles import StaticFiles
#importação da rota do problems_categories
from routes.problems_categories import router as problems_categories_router
#importação da rota de categories
from routes.categories import router as categories_router
# importação da rota de problems
from routes.problems import router as problems_router
# importação da rota shortcut
from routes.shortcut import router as shortcut_router 

from routes.ui.problems import router as ui_problems_router

from routes.ui.index import router as ui_index


# Criação das tabelas se não existirem
createTables()

app = FastAPI()

app.mount("/static", StaticFiles(directory="./src/static"), name="static")

app.include_router(problems_categories_router)
app.include_router(categories_router)
app.include_router(problems_router)
app.include_router(shortcut_router)
app.include_router(ui_problems_router)
app.include_router(ui_index)