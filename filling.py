import os
import sqlite3
import shutil

conn = sqlite3.connect('Color_Study(UpdateV2.4).db')
cur = conn.cursor()


def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def Pictures(Author, year, name, image):
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
    cur.execute("""INSERT INTO Pictures (IDAuthor, Name, IDDate, Ratio, ImageSource) VALUES (?,?,?,?,?);""", (aut, name, dat, 1, image))
    conn.commit()
    return "done"


def insert_blob(image, author, name, year):
    try:
        sqlite_insert_blob_query = """INSERT INTO Au
                                  (image, author, name, year) VALUES (?, ?, ?, ?)"""
        data_tuple = (image, author, name, year)
        cur.execute(sqlite_insert_blob_query, data_tuple)
        conn.commit()
        print("Изображение и файл успешно вставлены как BLOB в таблиу")

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


directory = 'Архив Картин'

for dirname in os.listdir(directory):
    f = os.path.join(directory, dirname)
    if os.path.isdir(f):
        print(f)
        try:
            for filename in os.listdir(f):
                fp = os.path.join(f, filename)
                blob = convert_to_binary_data(fp)
                author = dirname
                spis = ".".join(filename.split(".")[:-1]).split("_")
                if spis[-1] == "thumb310":
                    spis = spis[:-1]
                if spis[-1] == "250":
                    spis = spis[:-2]
                name = spis[0] + "\\" + spis[1]
                try:
                    year = int(spis[2])
                except:
                    year = 1900
                Pictures(author, year, name, blob)
        except:
            pass

conn.close()
