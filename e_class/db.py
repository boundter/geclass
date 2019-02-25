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

    def execute(self, sql, parameter=None):
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
        log.info(
            'Execute query {} with parameters {}'.format(sql, parameter))
        return self.db.execute(sql, parameter)

    def select_user(self, user_id=None, email=None):
        """Get all info about a specific user.

        Query the database using either the user_id or the email.

        Args:
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
        logging.info('Added new user with email {}'.format(email))
        self.db.execute(
            'INSERT INTO user (email, password) VALUES (?, ?)',
            (email, password))
        self.db.commit()

    def get_courses(self, user_id):
        """Fetch all coursed from user with given id.

        Args:
            user_id (int): The id of the owner of the courses.

        Returns:
            A list of all the sqlite3 rows of the courses.

        >>> courses = get_courses(user_id=1)
        >>> for course in courses:
        ...     print(course['course_identifier'])
        'uni_potsdam_biochem_2018'
        'uni_potsdam_phys_2018'

        """
        return self.db.execute(
            'SELECT * FROM course WHERE user_id = ?', (user_id,)).fetchall()

    def add_course(self, user_id, course_identifier):
        """Add a new course to the database.

        Args:
            user_id (int): The id of the owner of the course.
            course_identifier (str): Some identifier for the course. It
                                     does not need to be unique.

        >>> get_courses(user_id=1)
        >>> for course in courses:
        ...     print(course['course_identifier'])
        'uni_potsdam_biochem_2018'
        'uni_potsdam_phys_2018'
        >>> add_course(user_id=1, course_identifier='a_new_course')
        >>> get_courses(user_id=1)
        >>> for course in courses:
        ...     print(course['course_identifier'])
        'uni_potsdam_biochem_2018'
        'uni_potsdam_phys_2018'
        'a_new_course'

        """
        log.info(
            'Added new course {} for user {}'
            ''.format(course_identifier, user_id))
        self.db.execute(
            'INSERT INTO course (user_id, course_identifier) VALUES (?, ?)',
            (user_id, course_identifier))
        self.db.commit()

    def change_email(self, user_id, email):
        """Change the email adress of a given user.

        Args:
            user_id (int): The id of the user.
            email (str): The new email adress.

        >>> select_user(user_id=1)
        ('test1@gmail.com', 'some hash')
        >>> change_email(user_id=1, email='ab@cd.ef')
        >>> select_user(user_id=1)
        ('ab@cd.ef', 'some hash')

        """
        log.info('User {} changed email to {}'.format(user_id, email))
        self.db.execute(
            'UPDATE user SET email = ? WHERE id = ?', (email, user_id))
        self.db.commit()

    def change_password(self, user_id, password):
        """Change the password of a given user.

        Args:
            user_id (int): The id of the user.
            password (str): The new password.

        >>> select_user(user_id=1)
        ('test1@gmail.com', 'some hash')
        >>> change_email(user_id=1, password='new_password')
        >>> select_user(user_id=1)
        ('ab@cd.ef', 'a different hash')

        """
        log.info('User {} changed password'.format(user_id))
        self.db.execute(
            'UPDATE user SET password = ? WHERE id = ?', (password, user_id))
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
