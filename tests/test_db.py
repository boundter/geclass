"""Test the db functionality for the EClass."""
import sqlite3

import pytest
from flask import g

from e_class.db import DBConnection


def test_get_close_db(app):
    with app.app_context():
        with DBConnection() as db:
            assert db() is g.db

        # after the context the db connection gets teared down
        with pytest.raises(AttributeError) as e:
            g.db.execute('SELECT 1')


def test_init_db_command(runner, monkeypatch):
    init = {'called': False}

    def fake_init_db():
        init['called'] = True

    monkeypatch.setattr('e_class.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert init['called']
