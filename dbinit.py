import sqlite3

conn = sqlite3.connect('Geospybot.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS BotUsers (
    userid INTEGER PRIMARY KEY,
    firstname TEXT NOT NULL,
    dc TEXT,
    dateofstart TEXT NOT NULL,
    isbanned BOOLEAN NOT NULL DEFAULT 0
)
''')

conn.commit()
conn.close()
