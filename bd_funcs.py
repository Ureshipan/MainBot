import sqlite3


bd_name = "Color_Study.db"


def new_user(user_id, qualification, skip):
    conn = sqlite3.connect(bd_name)
    cur = conn.cursor()
    user = (user_id, qualification, skip, -2, 0)
    cur.execute("""INSERT INTO Users (UserNameId, Qualification, Ignore, Position, Social_rate) VALUES (?, ?, ?, ?, ?);""", user)
    conn.commit()
    conn.close()
    return "done"


def update_pos(user_id, pos):
    conn = sqlite3.connect(bd_name)
    cur = conn.cursor()
    cur.execute("""UPDATE Users SET Position=? WHERE UserNameId=?;""", (pos, user_id))
    conn.commit()
    conn.close()
    return "done"


def get_user(user_id):
    try:
        conn = sqlite3.connect(bd_name)
        cur = conn.cursor()
        cur.execute("""SELECT * FROM Users WHERE UserNameId = ?;""", (user_id, ))
        answer = cur.fetchone()
        cur.execute("""SELECT IDPictures FROM MainTable WHERE IDResult = (SELECT ID FROM Users_Result WHERE IDUsers=? ORDER BY ID DESC)""", (user_id, ))
        answer += cur.fetchone()
        conn.close()
    except:
        answer = "No"
    return answer


def new_answer(user_id, pic_id):
    pass


def add_answer(user_id, param, mean):
    pass

