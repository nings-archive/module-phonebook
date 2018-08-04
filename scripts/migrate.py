#! /usr/bin/env python3

import os
import sqlite3

def main() -> None:
    print('Running migrations...')
    conn = sqlite3.connect(os.environ['DB_NAME'])

    try:
        conn.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            state INTEGER NOT NULL,
            role INTEGER NOT NULL,
            saved_state STRING
        )''')
        conn.commit()
        print('  {}'.format('table users created'))
    except sqlite3.OperationalError as error:
        print('  {}'.format(error))

    try:
        conn.execute('''CREATE TABLE groups (
            code STRING PRIMARY KEY,
            url STRING NOT NULL UNIQUE,
            owner INTEGER NOT NULL,
            expiry INTEGER NOT NULL
        )''')
        conn.commit()
        print('  {}'.format('table groups created'))
    except sqlite3.OperationalError as error:
        print('  {}'.format(error))

    try:
        conn.execute('''CREATE TABLE stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user INTEGER NOT NULL,
            time INTEGER NOT NULL,
            command string NOT NULL
        )''')
        print('  {}'.format('table stats created'))
    except sqlite3.OperationalError as error:
        print('  {}'.format(error))

if __name__ == '__main__':
    main()
