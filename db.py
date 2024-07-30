import sqlite3
from datetime import datetime
from misc import append_to_file

logfile = "log.txt"


def adduser(userid,firstname,dc,dateofstart):
    with sqlite3.connect("Geospybot.db") as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO BotUsers (userid, firstname, dc, dateofstart) VALUES (?, ?, ?, ?)", (userid, firstname, dc, dateofstart))
        conn.commit()
        append_to_file(logfile, f"User {userid} added to database")


def userexists(userid):
    with sqlite3.connect("Geospybot.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT userid FROM BotUsers WHERE userid = ?", (userid,))
        result = cur.fetchone()
        if result:
            return True
        else:
            return False
        conn.commit()

        
def banuser(userid):
    with sqlite3.connect("Geospybot.db") as conn:
        cur = conn.cursor()
        cur.execute("UPDATE BotUsers SET isbanned = 1 WHERE userid = ?", (userid,))
        conn.commit()
        append_to_file(logfile, f"User {userid} banned")

def unbanuser(userid):
    with sqlite3.connect("Geospybot.db") as conn:
        cur = conn.cursor()
        cur.execute("UPDATE BotUsers SET isbanned = 0 WHERE userid = ?", (userid, ))
        conn.commit()
        append_to_file(logfile, f"User {userid} unbanned")

def isbanned(userid):
    with sqlite3.connect("Geospybot.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT isbanned FROM BotUsers WHERE userid = ?", (userid,))
        result = cur.fetchone()
        if result is None:  # User not found in the database
            return False
        if result[0] == 1:
            return True
        else:
            return False

