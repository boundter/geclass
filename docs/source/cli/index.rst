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
   $ flask change-pwd $email $new_password

Here `$email` has to be replaced by the Email adress of the user and
`$new_password` the new password.

Questionnaire Database
======================

To initialize a new Questionnaire database simply execute
::
  $ flask init-questionnaire-db

**Take Care: This will delete the current database.**

The following command downloads the data from the survey page and saves it to
the /app/instance directory.
::
  $ flask download-data

To then load the data into the datbase just execute
::
  $ flask load-questionnaire-data $data_file

where `$data_file` has to be replaced by the location of the downloaded file.

Reports are generated with the following command. Created reports are saved to
`/app/instance/$course_id`. If, for some reason, no report can be created then
an empty directory will be generated.
::
  $ flask create-reports

It checks for all finished courses. If a directory in `/app/instance` already
has the name of the course identifier nothing will be done.

A convenience function helps to set the time validity of courses, should there
be a delay in the survey. The command
::
  $ flask validate_time $pre_post $course_name

validates all answers for the pre or post survey for a given course. The
possible values for `$pre_post` are `pre` and `post` and `$course_name` has to
be replaced by the course identifier, e.g., `abcde` or `zrwyx`. To validate all post
responses for the course with the identifier `qtycv` the following command would
be used
::
  $ flask validate_time post qtycv

Reminders
=========

The following command sends reminders to all users about the start of their pre
and post questionnaires.
::
  $ flask send_reminder


Analysis
========

First of all, to check the validity of the data, there are some commands to get
all unmatched students and all unknown courses.

The command
::
  $ flask get_unknown_courses

returns all the codes of the known courses, i.e., `abcde` or `zrwyx`, as well as
all codes that could not be matched. The list will be saved to
`/app/instance/unknown.csv` and is in the typical `.csv` format, where columns
are separated by commas. The first column will be the known courses and the
second column the unknown_courses.

A similar command to find the unmatched students is
::
  $ flask get_unmatched

A list of all unmatched students will be saved to `/app/instance/unmatched.csv`.
Only students with valid pre- and post-responses will be considered, to decrease
the noise of unfinished or wrongly finished surveys. The datafile contains three
rows, the first one contains the id of the course, i.e., `1`, `2`, and so on.
The second column contains the unmatched student codes of the pre survey and the
third column the umatched student codes of the post survey. The students are
sorted by courses to help the matching.

The matched data from the surveys can be exported in an anonymized form with
::
  $ flask export_to_csv

All matched responses will be exported to the file `/app/instance/export.csv`.
For each student the following information will be saved (in this order of
columns):

- the course id
- experience_id, i.e., first year or beyond first year
- program_id, the type of course (Mono Bachelor, Lehramt, ...)
- course_type_id, Grundpraktikum or F-Praktikum
- traditional_id, if the course  has a detailed instruction or if it is more
  open
- q_you_pre_{}, these contain all the answers to the pre survey for the
  you-questions
- q_you_post_{}, these contain all the answers to the post survey for the
  you-questions
- q_expert_pre_{}, these contain all the answers to the pre survey for the
  expert-questions
- q_expert_post_{}, these contain all the answers to the post survey for the
  expert-questions
- q_mark_{}, these contain all the answers to the questions about the marks

The values for the first few questions can be found in the geclass database in
`/app/instance/geclass.sqlite` or in the default values in
`/app/geclass/default.sql`. The answers to the survey are already compared to
the expert, where a `1` indicates agreement, a `-1` disagreement, a `0`
undecidedness and a `-998` that the question was not answered. To anonymize the
data, there are no ids for the students and their order has been shuffled.

Cron
****
Cron is a tool to execute commands at specific times, such as daily at a certin
hour, or weekly or such (note that the docker container is in the GMT timezone).
The cronfile which contains these informations is located in the root folder
called `reminder_cron`.

As it stands now the following rules are included:

- Every day at 01:00 the daily logs are moved
- Every day at 03:00 the survey data is downloaded and deleted from the server
- Every day at 04:00 reminders are sent out
- Every day at 05:00 the reports are created

Please note that the cron service has to be started manually when creating a
new docker container. This is done automatically in the `server.sh` script.

Running the Server
******************

Assuming the docker image was build, as explained in the Docker section, the
server can be easily started. In the root directiry there exist two scripts
`server_dev.sh` and `server.sh`.

The `server.sh` script starts a container automatically and starts the cron job.
The environment variables `FLASK_KEY`, `QUAMP_USER`, and `QUAMP_PASSWD` have to
best. The quamp variables are needed to login to the quamp server and the
flask_key is a simple encryption key for the cookies. The key may change between
server start, but this will log out all users. This server is self contained, so
changes in the source files will not be reflected in the container. As an
example:
::
  $ export FLASK_KEY=1234; export QUAMP_USER=test_user; export QUAMP_PASSWD=test_passwd; ./server.sh

The `server_dev.sh` script works similarly, but does not need the key variable.
Here changes in the local files will be reflected so that it can be used for the
development.

All servers are exposed on the port 80, which is also forwarded.
