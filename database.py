import sqlite3
from flask import g

DATABASE = 'taskify.db'

def init_db():
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                progress_update TEXT,  -- Changed from 'update' to 'progress_update'
                date TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS features (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                feature TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS thoughts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                thought TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )
        ''')
        db.commit()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()