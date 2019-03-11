"""Access to the database for the user data.

This module contains functions to create a database connection,
execute queries and close the connection. Additionally there is a tool
to create the database.

Closing the database is done in the context of the flask app, as well
as the creation.

"""

import sqlite3
import logging

import click
from flask import current_app, g
from flask.cli import with_appcontext

log = logging.getLogger(__name__)


class DBConnection:
    """Connection handler for the GEclass website.

    This class picks up (or creates, if none is available) a database
    connection from the current user session. The closing of the
    connection is the responsibility of the flask app.

    >>> db = DBConnection()
    >>> db.select_user(email='test@abc.de')
    (3, 'test@abc.de', 'password')

    """

    def __init__(self):
        """Pick up the connection to the database.

        If none exists in the current session it will create a new
        connection.

        """
        if 'db' not in g:
            log.debug('Create new db-connection')
            g.db = sqlite3.connect(
                database=current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
        self.db = g.db

    def __call__(self):
        """Return the database connection object."""
        return self.db

    def execute(self, sql, parameters=None):
        """Execute a SQL query.

        The SQL statement should have ? placeholders for sanitation.
        This is just a wrapper around the sqlite3 method for
        convenience.

        Args:
            sql (str): The SQL query.
            parameter (tuple): Replacements for the placeholders.

        Returns:
            sqlite3.Cursor

        >>> cursor = execute('SELECT * FROM user WHERE id = ?', (3,))
        >>> cursor.fetchone()
        (3, 'test@abc.de', 'password')

        """
        return self.db.execute(sql, parameters)

    def _select(self, table, field, value):
        sql = 'SELECT * FROM {} WHERE {} = ?'.format(table, field)
        return self.execute(sql, (value,))

    def select_one(self, table, field, value):
        return self._select(table, field, value).fetchone()

    def select_all(self, table, field, value):
        return self._select(table, field, value).fetchall()

    def add(self, table, field, values):
        value_string = ', '.join(['?']*len(values))
        field_string = ', '.join(field)
        sql = 'INSERT INTO {} ({}) VALUES ({})'.format(table,
            field_string, value_string)
        self.execute(sql, values)
        self.db.commit()

    def update_one(self, table, condition, new_value):
        sql = 'UPDATE {} SET {} = ? WHERE {} = ?'.format(table, new_value[0],
            condition[0])
        self.execute(sql, (new_value[1], condition[1]))
        self.db.commit()


def init_db():
    """Remove old database (if it exists) and create a new one."""
    log.info('Create a new database')
    db = DBConnection()
    with current_app.open_resource('schema.sql') as f:
        db().executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Create CLI for creating a new database with `flask init-db`.

    **Careful: This will overwite the current one and all data will
    be lost.**

    """
    init_db()
    click.echo('Initialized the database')


def close_db(e=None):
    """Close the database. Needed for the teardown."""
    db = g.pop(name='db', default=None)
    if db is not None:
        db.close()


def init_app(app):
    """Create connection to the factory."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
