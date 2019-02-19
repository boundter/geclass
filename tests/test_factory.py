"""Test factory."""
from e_class import create_app


def test_config():
    """Check handling of test configuration in factory."""
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
