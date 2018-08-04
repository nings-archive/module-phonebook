================
Module Phonebook
================
The official implementation of this project can be found at `@USPhonebook_bot`_.

.. _`@USPhonebook_bot`: https://t.me/USPhonebook_bot

Contributing Guide
==================
To set up a development environment, you will need Pipenv_, and a copy of
python 3.7.

.. code::

    $ pipenv install --dev

Then, ping the `@botfather`_ on telegram and obtain a bot token. Add it to your
``.env`` file.

.. code::

    $ cp .env.example .env
    $ vim .env

.. _Pipenv: https://github.com/pypa/pipenv
.. _`@botfather`: https://t.me/botfather

Pipenv Scripts
--------------
``check``
    Runs the Mypy_ static type checker.
``migrate``
    Creates a database file, including the necessary tables.
``reset``
    Deletes the current database file, then runs ``migrate`` (above).
``start``
    Starts the bot.
``test``
    Runs the pytest_ tests.

For example, ``pipenv run test`` would run the script ``test``, as described
above. The database file is specified by the ``.env`` file. The default name is
``phonebook.db``.

.. _Mypy: http://mypy-lang.org/
.. _pytest: https://docs.pytest.org/
