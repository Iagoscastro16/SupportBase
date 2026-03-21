# banco que será utilizado
import sqlite3
# biblioteca para armazenar caminhos
from pathlib import Path


caminhoBanco = Path(__file__).parent /"database"/"supportBase.db"

conn = sqlite3.connect(caminhoBanco)

