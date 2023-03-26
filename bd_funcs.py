import sqlite3


def new_user(user_id, qualification, skip):
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    user = (user_id, qualification, skip, 0)
    cur.execute("""INSERT INTO Users (ID, qualification, skip, position) VALUES (?, ?, ?, ?);""".format(user))
    conn.commit()
    conn.close()
    return "done"


def get_user(user_id):
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM Users WHERE ID = ?""".format(user_id))
    answer = cur.fetchone()
    conn.close()
    return answer
