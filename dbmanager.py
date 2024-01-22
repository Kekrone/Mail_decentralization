import sqlite3
import config


def create_table() -> bool:
    try:
        con = sqlite3.connect(config.path_to_db)
        cursor = con.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER NOT NULL,
        mailaddressfrom TEXT NOT NULL,
        mail TEXT NOT NULL)
        ''')

        con.commit()

        print("DB: commited")

    except sqlite3.Error as er:
        print(f"Error: {er}")

    finally:
        con.close()
        print("Connection close")


def register_user(user_id: int, mailaddressfrom: str, mail: str) -> bool:
    print(f"register_user: {user_id}")

    try:
        con = sqlite3.connect(config.path_to_db)
        cursor = con.cursor()

        cursor.execute('INSERT INTO Users (id, mailaddressfrom, mail) VALUES (?, ?, ?)', (user_id, mailaddressfrom, mail))
        con.commit()

        print("DB: commited")

    except sqlite3.Error as er:
        print(f"Error: {er}")

    finally:
        con.close()
        print("Connection close")

def get_user(user_id: int):
    print(f"get_user: {user_id}")
    try:
        con = sqlite3.connect(config.path_to_db)
        cursor = con.cursor()

        cursor.execute('SELECT * FROM Users WHERE id = ?', (user_id,))

        print("DB: get_user")
        return cursor.fetchall()

    except sqlite3.Error as er:
        print(f"Error: {er}")

    finally:
        con.close()
        print("Connection close")

def delete_user(mailaddressfrom: str):
    print("deletion start")
    try:
        con = sqlite3.connect(config.path_to_db)
        cursor = con.cursor()

        cursor.execute('DELETE FROM Users WHERE mailaddressfrom = ?', (mailaddressfrom,))
        con.commit()

        print("DB: get_user")
    except sqlite3.Error as er:
        print(f"Error: {er}")

    finally:
        con.close()
        print("Connection close")

if __name__ == '__main__':
    user_id = 42342434234
    mail = 'examplemail@yandex.ru'
    mailaddressfrom = 'sdngfdsngsdgn@mail.ru'

    create_table()

    register_user(user_id, mail, mailaddressfrom)

    print(get_user(user_id))
