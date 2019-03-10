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
  * program_id - the id of the program the students belong to
  * course_type_id
  * focus_id
  * traditional_id
  * equipment_id
  * experience_id
  * university_id
  * notes_id
  * number_students - expected total number of students
  * students_per_instructor - average of students per instructor
  * lab_per_lecture - ratio of lab time to lecture time
  * number_experiments - number of experiments
  * number_projects - number of projects
  * start_date_pre - start date of pre questionaire
  * start_date_post - start date of post questionaire
  * name - name of the course

* program

  * id - the primary key (autoincrement)
  * program_name - name of the program

* course_type

  * id - the primary key (autoincrement)
  * course_type_name - name of the type of course (GP/FP)

* focus

  * id - the primary key (autoincrement)
  * focus_name - what the course focuses on

* traditional

  * id - the primary key (autoincrement)
  * traditional_name - if the course is traditional, nontraditional

* equipment

  * id - the primary key (autoincrement)
  * equipment_type - typical type of equipment in lab

* experience

  * id - the primary key (autoincrement)
  * experience_level - level of experience (first-year/second-year)

* university

  * id - the primary key (autoincrement)
  * university_name - name of the university

* notes

  * id - the primary key (autoincrement)
  * notes_text - notes about the course
