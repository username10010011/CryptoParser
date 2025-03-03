import sqlite3
from pprint import pprint



def create_users_table():
    connect = sqlite3.connect("data/users/users.db")
    cursor = connect.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS users
        (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            tgid INTEGER NOT NULL UNIQUE, 
            send_news INTEGER DEFAULT 0,
            autoupdate INTEGER DEFAULT 0,
            autoupdate_messages TEXT
        )
        '''
    )
    connect.commit()
    connect.close()

create_users_table()

def get_user(tgid: int) -> dict | bool:
    connect = sqlite3.connect("data/users/users.db")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM users WHERE tgid = ?", (tgid,))
    user = cursor.fetchone()
    if user:
        return {
            "user_id": user[0],
            "tgid": user[1],
            "send_news": user[2],
            "autoupdate": user[3],
            "autoudate_messages": user[4]
        }
    return False


def add_user(tgid: int) -> None:
    if get_user(tgid) is False:
        print(f"user: {tgid} added to db")
        connect = sqlite3.connect("data/users/users.db")
        cursor = connect.cursor()
        cursor.execute("INSERT INTO users (tgid) VALUES (?)", (tgid,))
        connect.commit()
        connect.close()
        return
    raise ValueError(f"ERROR: User with {tgid} is already exist!")


def switch_send_news(tgid: int):
    connect = sqlite3.connect("data/users/users.db")
    cursor = connect.cursor()
    user = get_user(tgid)
    if not user:
        raise ValueError(f"ERROR: User with tgid {tgid} not found!")
    switch = 1 if user["send_news"] == 0 else 0
    cursor.execute("UPDATE users SET send_news = ? WHERE tgid = ?", (switch, user["tgid"],))
    connect.commit()
    connect.close()


def switch_autoupdate(tgid: int):
    connect = sqlite3.connect("data/users/users.db")
    cursor = connect.cursor()
    user = get_user(tgid)
    if not user:
        raise ValueError(f"ERROR: User with tgid {tgid} not found!")
    switch = 1 if user["autoupdate"] == 0 else 0
    cursor.execute("UPDATE users SET autoupdate = ? WHERE tgid = ?", (switch, user["tgid"],))
    connect.commit()
    connect.close()


def display_all_users():
    connect = sqlite3.connect("data/users/users.db")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    pprint(data)


def get_autoupdate_users() -> list[tuple]:
    connect = sqlite3.connect("data/users/users.db")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM users WHERE autoupdate = 1")
    return cursor.fetchall()[:]


def add_arbitrage_message(tgid: int, messages: list[int]) -> None: # type: ignore
    connect = sqlite3.connect("data/users/users.db")
    cursor = connect.cursor()
    messages_ids = ""
    for message_id in messages:
        messages_ids += str(message_id) + "|"
    messages_ids = messages_ids[:-1]
    cursor.execute("UPDATE users SET autoupdate_messages = ? WHERE tgid = ?", (messages_ids, tgid, ))
    connect.commit()
    connect.close()


def clear_arbitrage_message(tgid: int):
    connect = sqlite3.connect("data/users/users.db")
    cursor = connect.cursor()
    cursor.execute("UPDATE users SET autoupdate_messages = ? WHERE tgid = ?", ('', tgid))
    connect.commit()
    connect.close()
