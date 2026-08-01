# 1. banco que será utilizado
import os, psycopg2

# 2. biblioteca para armazenar caminhos
import os
from pathlib import Path

#3. importar variaveis de ambiente
from dotenv import load_dotenv

load_dotenv()

db_name= os.getenv("POSTGRES_DB")
db_user= os.getenv("POSTGRES_USER")
db_password= os.getenv("POSTGRES_PASSWORD")
db_host= os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")

conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)