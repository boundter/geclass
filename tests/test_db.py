"""Test the db functionality for the EClass."""
import sqlite3

import pytest

from e_class.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    # after the context the db connection gets teared down
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e)


def test_init_db_command(runner, monkeypatch):
    init = {'called': False}

    def fake_init_db():
        init['called'] = True

    monkeypatch.setattr('e_class.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert init['called']
