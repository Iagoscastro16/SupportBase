import sqlite3

from config import conn

def createTables():
    cursor = conn.cursor()

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

    cursor.execute('''    
        CREATE TABLE IF NOT EXISTS categories(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(40) NOT NULL
                                )'''
                )


    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS problems_categories(
            problem_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            PRIMARY KEY (problem_id, category_id)
                                        )'''
                )

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL,
            value TEXT NOT NULL
                                )'''
                )

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shortcuts( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tecla TEXT NOT NULL,
            phrase TEXT 
                                    )'''
                )

    conn.commit()