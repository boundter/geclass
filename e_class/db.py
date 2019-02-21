"""Access to the database for the user data.

This module contains functions to create a database connection,
execute queries and close the connection. Additionally there is a tool
to create the database.

Closing the database is done in the context of the flask app, as well
as the creation. To create a new database there is the following
command:

    $ flask init-db

"""

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


class DBConnection:
    """Connection handler for the EClass website.

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
            g.db = sqlite3.connect(
                database=current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
        self.db = g.db

    def __call__(self):
        """Return the database connection object."""
        return self.db

    def execute(self, sql, parameter=None):
        """Execute a SQL query.

        The SQL statement should have ? placeholders for sanitation.
        This is just a wrapper around the sqlite3 method for
        convenience.

        Args:
            sql (str): The SQL query.

        Kwargs:
            parameter (tuple): Replacements for the placeholders.

        Returns:
            sqlite3.Cursor

        >>> cursor = execute('SELECT * FROM user WHERE id = ?', (3,))
        >>> cursor.fetchone()
        (3, 'test@abc.de', 'password')

        """
        return self.db.execute(sql, parameter)

    def select_user(self, user_id=None, email=None):
        """Get all info about a specific user.

        Query the database using either the user_id or the email.

        Kwargs:
            user_id (int): The user id to search for.
            email (string): The email of the user to search for.

        Returns:
            A tuple of form (user_id, email, password_hash) for the
            given parameters. If there is no match None will be
            returned.

        >>> select_user(user_id=3)
        (3, 'test@abc.de', 'password')
        >>> select_user(email='test@abc.de')
        (3, 'test@abc.de', 'password')

        """
        if user_id is not None:
            return self.db.execute(
                'SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
        if email is not None:
            return self.db.execute(
                'SELECT * FROM user WHERE email = ?', (email,)).fetchone()
        return None

    def add_user(self, email, password):
        """Add a new user to the database.

        There is no check, if the user already exists. Also the
        password will not be hashed, but written as it is given.

        Args:
            email (str): The email of the new user.
            password (str): The hash of the password of the new user.

        >>> select_user(user_id=4)
        None
        >>> add_user(email='hello@abc.de', password='foo')
        >>> select_user(user_id=4)
        (4, 'hello@abc.de', 'foo')

        """
        self.db.execute(
            'INSERT INTO user (email, password) VALUES (?, ?)',
            (email, password))
        self.db.commit()

    def get_courses(self, user_id):
        return self.db.execute(
            'SELECT * FROM course WHERE user_id = ?', (user_id,)).fetchall()


def init_db():
    """Remove old database (if exists) and create new one."""
    db = DBConnection()
    with current_app.open_resource('schema.sql') as f:
        db().executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Remove old database (if exists) and create new one."""
    init_db()
    click.echo('Initialized the database')


def close_db(e=None):
    db = g.pop(name='db', default=None)
    if db is not None:
        db.close()


def init_app(app):
    """Create connection to the factory."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
