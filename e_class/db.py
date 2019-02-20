"""Functions to access the web-database."""
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


class DBConnection:

    def __enter__(self):
        if 'db' not in g:
            g.db = sqlite3.connect(
                database=current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
        self.db = g.db
        return self

    def __exit__(self, exc_type=None, exc_value=None, traceback=None):
        g.pop(name='db', default=None)
        self.db.close()

    def __call__(self):
        return self.db

    def select_user(self, user_id=None, email=None):
        if user_id is not None:
            return self.db.execute(
                'SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
        if email is not None:
            return self.db.execute(
                'SELECT * FROM user WHERE email = ?', (email,)).fetchone()
        return None

    def add_user(self, email, password):
        self.db.execute(
            'INSERT INTO user (email, password) VALUES (?, ?)',
            (email, password))
        self.db.commit()


def init_db():
    """Remove old database (if exists) and create new one."""
    with DBConnection() as db:
        with current_app.open_resource('schema.sql') as f:
            db().executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Remove old database (if exists) and create new one."""
    init_db()
    click.echo('Initialized the database')


def init_app(app):
    """Connection to factory."""
    app.cli.add_command(init_db_command)
