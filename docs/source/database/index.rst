Database
********

Webpage
=======

The database for the webpage is a simple SQLite relational database. Since there
is not a huge amount of users, this should be enough. If there should be a
time when it will not be enough, then the transition to e.g. MySQL should be
rather painless.

There are two tables:

* user

  * id - the primary key (autoincrements)
  * email - the email of the user, stored as a string
  * password - the password hash as a string

* course

  * id - the primary key (autoincrement)
  * user_id - the id of the user the course belongs to
  * course_identifier - some kind of non-unique identifier string
