# 1. banco que será utilizado
import sqlite3
# 2. biblioteca para armazenar caminhos
from pathlib import Path



# 3. Indica que o caminho do banco é o supportBase.db
caminhoBanco = Path(__file__).parent /"database"/"supportBase.db"

# 4. Conecta ao banco
conn = sqlite3.connect(caminhoBanco)
# 5. Ativação da chave estrangeira por conta do sqlite não vir ativado por padrão
conn.execute("PRAGMA foreign_keys = ON")
