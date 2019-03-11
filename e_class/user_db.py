import logging

from e_class.db import DBConnection

log = logging.getLogger(__name__)

class UserDB(DBConnection):
    table = 'user'

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
            return self.select_one(self.table, 'id', user_id)
        if email is not None:
            return self.select_one(self.table, 'email', email)
        return None

    def add_user(self, email, encrypted_password):
        """Add a new user to the database.

        There is no check, if the user already exists. Also the
        password will not be hashed, but written as it is given.

        Args:
            email (str): The email of the new user.
            encrypted_password (str): The hash of the password of the
                new user.

        >>> select_user(user_id=4)
        None
        >>> add_user(email='hello@abc.de', encrypted_password='foo')
        >>> select_user(user_id=4)
        (4, 'hello@abc.de', 'foo')

        """
        self.add(
            self.table, ('email', 'password'), (email, encrypted_password))

    def change_email(self, user_id, new_email):
        """Change the email adress of a given user.

        Args:
            user_id (int): The id of the user.
            new_email (str): The new email adress.

        >>> select_user(user_id=1)
        ('test1@gmail.com', 'some hash')
        >>> change_email(user_id=1, new_email='ab@cd.ef')
        >>> select_user(user_id=1)
        ('ab@cd.ef', 'some hash')

        """
        log.info('User {} changed email to {}'.format(user_id, new_email))
        self.update_one(
            table=self.table,
            condition=('id', user_id),
            new_value=('email', new_email))

    def change_password(self, user_id, new_password):
        """Change the password of a given user.

        Args:
            user_id (int): The id of the user.
            new_password (str): The new password.

        >>> select_user(user_id=1)
        ('test1@gmail.com', 'some hash')
        >>> change_password(user_id=1, new_password='a different hash')
        >>> select_user(user_id=1)
        ('ab@cd.ef', 'a different hash')

        """
        log.info('User {} changed password'.format(user_id))
        self.update_one(
            table=self.table,
            condition=('id', user_id),
            new_value=('password', new_password))
