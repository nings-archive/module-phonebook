import os, time
import sqlite3

from datatypes import User, Group

DEFAULT_LIFESPAN = 100 * 24 * 60 * 60  # TODO make env var

def connect(db_action):
    """All the functions in this file require a sqlite3 Connection object as
    their first positional argument. This connect/1 decorator implicitly
    supplies that sqlite3 Connection object so that said functions can be called
    without having to include that first argument."""
    def connected_db_action(*args, **kwargs):
        conn = sqlite3.connect(os.environ['DB_NAME'])
        with conn:
            return db_action(conn, *args, **kwargs)
    return connected_db_action

def record_stat(command_handler_func):
    """Records a row for this command handler function."""
    def recorder(bot, update):
        insert_stat(
            update.message.chat_id,
            round(time.time()),
            update.message.text
        )
        return command_handler_func(bot, update)
    return recorder

@connect
def insert_user(conn, _id, state=0, role=0):
    """INSERT a row into TABLE users"""
    query = "INSERT INTO users (id, state, role) VALUES (?, ?, ?)"
    try:
        conn.execute(query, (_id, state, role))
    except sqlite3.IntegrityError:
        return None
    return True

@connect
def insert_group(conn, code, url, owner, expiry=None):
    """INSERT a row into TABLE groups"""
    query = "INSERT INTO groups VALUES (?, ?, ?, ?)"
    expiry = expiry if expiry else round(time.time() + DEFAULT_LIFESPAN)
    try:
        conn.execute(query, (code, url, owner, expiry))
    except sqlite3.IntegrityError:
        return None
    return True

@connect
def insert_stat(conn, user, time, command):
    """INSERT a row into TABLE stats"""
    query = "INSERT INTO stats (user, time, command) VALUES (?, ?, ?)"
    conn.execute(query, (user, time, command))
    return True

@connect
def get_user(conn, _id):
    """SELECT a row from TABLE users, using id"""
    query = "SELECT * FROM users WHERE id=?"
    row = conn.execute(query, (_id,)).fetchone()
    return User(*row) if row else None

@connect
def get_group(conn, code):
    """SELECT a row from TABLE groups, using code"""
    query = "SELECT * FROM groups where code=?"
    row = conn.execute(query, (code,)).fetchone()
    return Group(*row) if row else None

@connect
def get_group_by_url(conn, url):
    """SELECT a row from TABLE groups, using url; only used to validate"""
    query = "SELECT * FROM groups where url=?"
    row = conn.execute(query, (url,)).fetchone()
    return Group(*row) if row else None

@connect
def get_all_groups(conn):
    """SELECT all rows from TABLE groups"""
    query = "SELECT * FROM groups"
    rows = conn.execute(query).fetchall()
    return tuple(Group(*row) for row in rows) if rows else None  # [] is falsy

@connect
def update_user_state(conn, _id, new_state):
    """UPDATE a row's state value in TABLE users"""
    query = "UPDATE users SET state=? WHERE id=?"
    if get_user(_id) is None:
        return None  # if user does not exist, return None
    else:
        conn.execute(query, (new_state, _id))
        return True

@connect
def update_user_saved_state(conn, _id, new_saved_state):
    """UPDATE a row's saved_state value in TABLE users"""
    query = "UPDATE users SET saved_state=? WHERE id=?"
    if get_user(_id) is None:
        return None  # if user does not exist, return None
    else:
        conn.execute(query, (new_saved_state, _id))
        return True
