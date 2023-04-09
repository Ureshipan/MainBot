import sqlite3


bd_name = "Color_Study(UpdateV2.3).db"

#cur.execute("""SELECT ID FROM Date WHERE Date=?""",(year, ).
def Pictures(Author, year, name):
    conn = sqlite3.connect(bd_name)
    cur = conn.cursor()
    try:
        cur.execute("""INSERT INTO Authors (Autor) VALUES (?);""", (Author, ))
    except sqlite3.Error as e:
        print("Ошибка при записи в SQLite", e)
    try:
        cur.execute("""INSERT INTO Date (Date) VALUES (?);""", (year, ))
    except sqlite3.Error as e:
        print("Ошибка при записи в SQLite", e)
    cur.execute("""SELECT * FROM Authors WHERE Autor = ?;""", [Author])
    aut = cur.fetchone()[0]
    cur.execute("""SELECT * FROM Date WHERE Date = ?;""", [year])
    dat = cur.fetchone()[0]
    cur.execute("""INSERT INTO Pictures (IDAuthor, Name, IDDate, Ratio, ImageSource) VALUES (?,?,?,?,?);""", (aut,name, dat, 1,name ))
    conn.commit()
    conn.close()
    return "done"

def ResultUserOpros(IDUser, Composition, Status,Simmetria, Geometry, Photo_Montage, direction, size, color, form, Pallette):
    conn = sqlite3.connect(bd_name)
    cur = conn.cursor()
    cur.execute("""INSERT INTO Contrast (Direction, Size, Color, Form) VALUES (?,?,?,?);""", [direction, size, color, form])
    cur.execute("""SELECT * FROM Users WHERE UserNameId = ?;""", [IDUser])
    User = cur.fetchone()[0]
    cur.execute("""SELECT * FROM Contrast""")
    count = cur.rowcount
    IDContrast = cur.fetchall()[count][0]
    cur.execute("""INSERT INTO Users_Result (IDUsers, Composition, Status, Simmetria, Geometry, Photo_Montage, IDContrast, Palette) VALUES (?,?,?,?,?,?,?,?);""", [User, Composition, Status,Simmetria, Geometry, Photo_Montage,IDContrast, Pallette])
    conn.commit()
    conn.close()
    return "done"

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

