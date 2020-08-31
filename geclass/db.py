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
        log.debug('query "%s" with parameters %s', sql, parameters)
        return self.db.execute(sql, parameters)

    def _select(self, table, column, value):
        """Select entries from a table.

        Careful: The inputs `table` and `column` are not sanitized.
        The selected entries are not fetched yet, so a .fetchone()
        or .fetchall() is needed.

        Args:
            table (str): The table to fetch from.
            column (str): The column to search.
            value (str or int or float): The value to search for.

        Returns:
            The query result.

        >>> query = _select('user', 'email', 'test1@gmail.com')
        >>> query.fetchone()
        (1, 'test1@gmail.com', 'some_password_hash')

        """
        sql = 'SELECT * FROM {} WHERE {} = ?'.format(table, column)
        return self.execute(sql, (value,))

    def select_one(self, table, column, value):
        """Select the first entry of a query.

        Careful: The inputs `table` and `column` are not sanitized.

        Args:
            table (str): The table to fetch from.
            column (str): The column to search.
            value (str or int or float): The value to search for.

        Returns:
            The first result of the query.


        >>> select_one('user', 'email', 'test1@gmail.com')
        (1, 'test1@gmail.com', 'some_password_hash')

        """
        return self._select(table, column, value).fetchone()

    def select_all(self, table, column, value):
        """Select the all entries of a query.

        Careful: The inputs `table` and `column` are not sanitized.

        Args:
            table (str): The table to fetch from.
            column (str): The column to search.
            value (str or int or float): The value to search for.

        Returns:
            The all results of the query.


        >>> select_all('course', 'user_id', '1')
        (1, ...)
        (2, ...)

        """
        return self._select(table, column, value).fetchall()

    def select_all_entries(self, table):
        """Get all entries from a specific table.

        Careful: `table` is not sanitized.

        Agrs:
            table (str): The table to get the entries from.

        Returns:
            A list with all the rows in the table.

        >>> select_all_entries('user')
        ((1, 'test1@gmail.com', 'some hash'),
         (2, 'test2@web.de', 'a different hash'))

        """
        sql = 'SELECT * FROM {}'.format(table)
        return self.db.execute(sql).fetchall()

    def add(self, table, columns, values):
        """Add a new row to the database.

        Careful: The inputs `table` and `columns` are not sanitized.

        Args:
            table (str): The table to add the row to.
            columns (list(str)): The columns in which to add data.
            values (list(str or int or float)): The values to add in the
                                            fields.

        >>> select_one('user', 'email', 'gp@uni-potsdam.de')
        None
        >>> add('user', ('email', 'password'), ('gp@uni-potsdam.de', 'a'))
        >>> select_one('user', 'email', 'gp@uni-potsdam.de')
        (3, 'gp@uni-potsdam.de', 'a')

        """
        value_string = ', '.join(['?'] * len(values))
        column_string = ', '.join(columns)
        sql = 'INSERT INTO {} ({}) VALUES ({})'\
            ''.format(table, column_string, value_string)
        self.execute(sql, values)
        self.db.commit()


    def add_and_get_id(self, table, columns, values):
        """Add a new row to the database.

        Careful: The inputs `table` and `columns` are not sanitized.

        Args:
            table (str): The table to add the row to.
            columns (list(str)): The columns in which to add data.
            values (list(str or int or float)): The values to add in the
                                            fields.

        >>> select_one('user', 'email', 'gp@uni-potsdam.de')
        None
        >>> add('user', ('email', 'password'), ('gp@uni-potsdam.de', 'a'))
        >>> select_one('user', 'email', 'gp@uni-potsdam.de')
        (3, 'gp@uni-potsdam.de', 'a')

        """
        value_string = ', '.join(['?'] * len(values))
        column_string = ', '.join(columns)
        sql = 'INSERT INTO {} ({}) VALUES ({})'\
            ''.format(table, column_string, value_string)
        last_id = self.execute(sql, values).lastrowid
        self.db.commit()
        return last_id

    def update_one(self, table, condition, new_value):
        """Update fields in the database.

        Careful: The inputs `table` and `condition[0]` and
        `new_value[0]` are not sanitized.

        The condition and new values are in the form
        condition=(column_name, value) and new_value
        equivalently.

        Args:
            table (str): The table to change the values in.
            condition (list(str, (str, or int or float))): The equality
                                                      to fulfill.
            new_value (list(str, (str or int or float))): The new value
                                                      to set.

        >>> select_one('user', 'id', '1')
        (1, 'test1@gmail.com', 'some_password_hash')
        >>> update_one('user', ('id', 1), ('email', 'new@web.de'))
        >>> select_one('user', 'id', '1')
        (1, 'new@web.de', 'some_password_hash')

        """
        sql = 'UPDATE {} SET {} = ? WHERE {} = ?'\
            ''.format(table, new_value[0], condition[0])
        self.execute(sql, (new_value[1], condition[1]))
        self.db.commit()


def init_db():
    """Remove old database (if it exists) and create a new one."""
    log.info('Create a new database')
    db = DBConnection()
    with current_app.open_resource('schema.sql') as f:
        db().executescript(f.read().decode('utf8'))
    with current_app.open_resource('default.sql') as f:
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
