import sqlite3
import config
import terminal


def create_table():
    try:
        con = sqlite3.connect(config.path_to_db)
        cursor = con.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS virtual_aliases (
        id INTEGER NOT NULL,
        source TEXT NOT NULL,
        destination TEXT NOT NULL)
        ''')

        con.commit()

        print("DB: commited")

    except sqlite3.Error as er:
        print(f"Error: {er}")

    finally:
        con.close()
        print("Connection close")


def register_user(user_id: int, source: str, destination: str):
    print(f"register_user: {user_id}")

    try:
        con = sqlite3.connect(config.path_to_db)
        cursor = con.cursor()

        cursor.execute('INSERT INTO virtual_aliases (id, source, destination) VALUES (?, ?, ?)',
                       (user_id, source, destination))
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

        cursor.execute('SELECT * FROM virtual_aliases WHERE id = ?', (user_id,))

        print("DB: get_user")
        return cursor.fetchall()

    except sqlite3.Error as er:
        print(f"Error: {er}")

    finally:
        con.close()
        print("Connection close")


def delete_user(source: str):
    print("deletion start")
    try:
        con = sqlite3.connect(config.path_to_db)
        cursor = con.cursor()

        cursor.execute('DELETE FROM virtual_aliases WHERE source = ?', (source,))
        con.commit()

        print("DB: get_user")
    except sqlite3.Error as er:
        print(f"Error: {er}")

    finally:
        con.close()
        print("Connection close")


if __name__ == '__main__':
    user_id = 42342434234
    destination = 'examplemail@yandex.ru'
    source = 'sdngfdsngsdgn@mail.ru'

    create_table()

    register_user(user_id, destination, source)

    print(get_user(user_id))
