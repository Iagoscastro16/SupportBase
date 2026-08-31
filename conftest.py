from dotenv import load_dotenv

load_dotenv(".env.test", override=True)

from database.tables import createTables

createTables()