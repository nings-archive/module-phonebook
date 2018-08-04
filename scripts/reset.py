#! /usr/bin/env python3

import os
from migrate import main as migrate

is_confirmed = input(
    "This will wipe the database. Enter 'Yes' (case sensitive) to confirm. > "
)

if is_confirmed == 'Yes':
    db_name = os.environ['DB_NAME']
    print('  Removing {}...'.format(db_name))
    os.remove(db_name)
    migrate()
else:
    print('  Aborted.')
