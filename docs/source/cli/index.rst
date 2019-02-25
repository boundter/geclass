Command Line Interface
**********************

There are some commands available on the command line

Database
========

The following command initializes the databse.
**Take Care: This will delete the current database.** ::

  $ flask init-db

Sometimes a user may forget his password. A new password can be set by calling
::

   $ flask change-pwd email new_password
