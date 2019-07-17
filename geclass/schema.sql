DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS program;
DROP TABLE IF EXISTS course_type;
DROP TABLE IF EXISTS focus;
DROP TABLE IF EXISTS traditional;
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS experience;
DROP TABLE IF EXISTS university;
DROP TABLE IF EXISTS notes;

PRAGMA encoding='UTF-8';

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE course (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  program_id INTEGER NOT NULL,
  course_type_id INTEGER NOT NULL,
  focus_id INTEGER NOT NULL,
  traditional_id INTEGER NOT NULL,
  equipment_id INTEGER NOT NULL,
  experience_id INTEGER NOT NULL,
  university_id INTEGER NOT NULL,
  notes_id INTEGER,
  number_students INTEGER NOT NULL,
  students_per_instructor REAL NOT NULL,
  lab_per_lecture REAL NOT NULL,
  number_experiments INTEGER,
  number_projects INTEGER,
  start_date_pre TEXT NOT NULL,
  start_date_post TEXT NOT NULL,
  name TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (program_id) REFERENCES program (id),
  FOREIGN KEY (course_type_id) REFERENCES course_type (id),
  FOREIGN KEY (focus_id) REFERENCES focus (id),
  FOREIGN KEY (traditional_id) REFERENCES traditional (id),
  FOREIGN KEY (equipment_id) REFERENCES equipment (id),
  FOREIGN KEY (experience_id) REFERENCES experience (id),
  FOREIGN KEY (university_id) REFERENCES university (id),
  FOREIGN KEY (notes_id) REFERENCES notes (id)
);

CREATE TABLE program (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  program_name TEXT NOT NULL
);

CREATE TABLE course_type (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  course_type_name TEXT NOT NULL
);

CREATE TABLE focus (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  focus_name TEXT NOT NULL
);

CREATE TABLE traditional (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  traditional_name TEXT NOT NULL
);

CREATE TABLE equipment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  equipment_type TEXT NOT NULL
);

CREATE TABLE experience (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  experience_level TEXT NOT NULL
);

CREATE TABLE university (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  university_name TEXT NOT NULL
);

CREATE TABLE notes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  notes_text TEXT NOT NULL
);

CREATE TABLE university_type (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  university_type_name TEXT NOT NULL
);

