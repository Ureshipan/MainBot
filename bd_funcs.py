import sqlite3


bd_name = "Color_Study(UpdateV2.4)fill.db"


def get_next_pic(userid):
    conn = sqlite3.connect(bd_name)
    cur = conn.cursor()
    cur.execute("""SELECT ID, IDUsers FROM Users_Result WHERE IDUsers = ?;""", [userid])
    ids = cur.fetchall()
    for i in range(len(ids)):
        ids[i] = (ids[i][0])
    picids = []
    for id in ids:
        cur.execute("""SELECT IDPictures, IDResult FROM MainTable WHERE IDResult = ?;""", [id])
        picids.append(cur.fetchone()[0])
    cur.execute("""SELECT ID, IDAuthor, Name, IDDate, ImageSource FROM Pictures WHERE ID NOT IN (SELECT IDPictures FROM MainTable WHERE IDResult IN (SELECT ID FROM Users_Result WHERE IDUsers = ?));""", [userid])
    pic = list(cur.fetchone())
    #print(pic)
    cur.execute("""SELECT Author FROM Authors WHERE ID = ?""", [pic[1]])
    pic[1] = cur.fetchone()[0]
    cur.execute("""SELECT Date FROM Date WHERE ID = ?""", [pic[3]])
    pic[3] = cur.fetchone()[0]
    conn.close()
    return pic

def ResultUserOpros(IDUser, imid, answers): #Composition, Status,Simmetria, Geometry, Photo_Montage, direction, size, color, form, Pallette):
    conn = sqlite3.connect(bd_name)
    cur = conn.cursor()
    cur.execute("""INSERT INTO Contrast (Direction, Size, Color, Form) VALUES (?,?,?,?);""",
                [answers["Контраст Направлений"], answers["Контраст Размеров"],
                 answers["Контраст Цветов"], answers["Контраст Форм"]])
    cur.execute("""SELECT * FROM Users WHERE UserNameId = ?;""", [IDUser])
    User = cur.fetchone()[0]
    cur.execute("""SELECT * FROM Contrast""")
    count = cur.rowcount
    IDContrast = cur.fetchall()[count][0]
    cur.execute("""INSERT INTO Users_Result (IDUsers, Composition, Status, Simmetria, Geometry, Photo_Montage, IDContrast, Palette) VALUES (?,?,?,?,?,?,?,?);""",
                [User, answers["Композиция"], answers["Динамика"], answers["Симметрия"], answers["Метафора"], answers["Фотомонтаж"], IDContrast, answers["Палитра"]])
    id = cur.execute("""SELECT ID FROM Users_Result WHERE IDUsers = ? ORDER BY ID DESC""", [User]).fetchone()
    cur.execute("""INSERT INTO MainTable (IDPictures, IDResult) VALUES (?, ?);""", (imid, id[0]))
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
        cur.execute("""SELECT * FROM Users WHERE UserNameId = ?;""", [user_id])
        answer = cur.fetchone()
        cur.execute("""SELECT * FROM Users_Result WHERE IDUsers = ?;""", [user_id])
        id = cur.fetchone()[0]
        cur.execute("""SELECT IDPictures FROM MainTable WHERE IDResult = ?""", [id])
        answer += cur.fetchone()
        conn.close()
    except Exception as e:
        print(e)
        answer = "No"
    return answer


def get_user_exist(user_id):
    try:
        conn = sqlite3.connect(bd_name)
        cur = conn.cursor()
        cur.execute("""SELECT * FROM Users WHERE UserNameId = ?;""", [user_id])
        answer = cur.fetchone()
        conn.close()
    except:
        answer = "No"
    return answer


def get_new_pic(userid):
    pass

