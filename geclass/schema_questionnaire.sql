DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS student_course;
DROP TABLE IF EXISTS questionnaire_you;
DROP TABLE IF EXISTS questionnaire_expert;
DROP TABLE IF EXISTS questionnaire_mark;
DROP TABLE IF EXISTS questionnaire_pre;
DROP TABLE IF EXISTS questionnaire_post;
DROP TABLE IF EXISTS student_pre;
DROP TABLE IF EXISTS student_post;

PRAGME encoding='UTF-8';

CREATE TABLE student (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code TEXT NOT NULL
);

CREATE TABLE student_course (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  course_id INTEGER NOT NULL,
  FOREIGN KEY (student_id) REFERENCES student (id)
);

CREATE TABLE questionnaire_you (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  q1 INTEGER,
  q2 INTEGER,
  q3 INTEGER,
  q4 INTEGER,
  q5 INTEGER,
  q6 INTEGER,
  q7 INTEGER,
  q8 INTEGER,
  q9 INTEGER,
  q10 INTEGER,
  q11 INTEGER,
  q12 INTEGER,
  q13 INTEGER,
  q14 INTEGER,
  q15 INTEGER,
  q16 INTEGER,
  q17 INTEGER,
  q18 INTEGER,
  q19 INTEGER,
  q20 INTEGER,
  q21 INTEGER,
  q22 INTEGER,
  q23 INTEGER,
  q24 INTEGER,
  q25 INTEGER,
  q26 INTEGER,
  q27 INTEGER,
  q28 INTEGER,
  q29 INTEGER,
  q30 INTEGER
);

CREATE TABLE questionnaire_expert (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  q1 INTEGER,
  q2 INTEGER,
  q3 INTEGER,
  q4 INTEGER,
  q5 INTEGER,
  q6 INTEGER,
  q7 INTEGER,
  q8 INTEGER,
  q9 INTEGER,
  q10 INTEGER,
  q11 INTEGER,
  q12 INTEGER,
  q13 INTEGER,
  q14 INTEGER,
  q15 INTEGER,
  q16 INTEGER,
  q17 INTEGER,
  q18 INTEGER,
  q19 INTEGER,
  q20 INTEGER,
  q21 INTEGER,
  q22 INTEGER,
  q23 INTEGER,
  q24 INTEGER,
  q25 INTEGER,
  q26 INTEGER,
  q27 INTEGER,
  q28 INTEGER,
  q29 INTEGER,
  q30 INTEGER
);

CREATE TABLE questionnaire_mark (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  q1 INTEGER,
  q2 INTEGER,
  q3 INTEGER,
  q4 INTEGER,
  q5 INTEGER,
  q6 INTEGER,
  q7 INTEGER,
  q8 INTEGER,
  q9 INTEGER,
  q10 INTEGER,
  q11 INTEGER,
  q12 INTEGER,
  q13 INTEGER,
  q14 INTEGER,
  q15 INTEGER,
  q16 INTEGER,
  q17 INTEGER,
  q18 INTEGER,
  q19 INTEGER,
  q20 INTEGER,
  q21 INTEGER,
  q22 INTEGER,
  q23 INTEGER
);

CREATE TABLE questionnaire_pre (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  questionnaire_you_id INTEGER NOT NULL,
  questionnaire_expert_id INTEGER NOT NULL,
  FOREIGN KEY (questionnaire_you_id) REFERENCES questionnaire_you (id),
  FOREIGN KEY (questionnaire_expert_id) REFERENCES questionnaire_expert (id)
);

CREATE TABLE questionnaire_post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  questionnaire_you_id INTEGER NOT NULL,
  questionnaire_expert_id INTEGER NOT NULL,
  questionnaire_mark_id INTEGER NOT NULL,
  FOREIGN KEY (questionnaire_you_id) REFERENCES questionnaire_you (id),
  FOREIGN KEY (questionnaire_expert_id) REFERENCES questionnaire_expert (id),
  FOREIGN KEY (questionnaire_mark_id) REFERENCES questionnaire_mark (id)
);

CREATE TABLE student_pre (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  questionnaire_pre_id INTEGER NOT NULL,
  start_time INTEGER,
  end_time INTEGER,
  valid_control INTEGER NOT NULL,
  in_time INTEGER NOT NULL,
  FOREIGN KEY (student_id) REFERENCES student (id),
  FOREIGN KEY (questionnaire_pre_id) REFERENCES questionnaire_pre (id)
);

CREATE TABLE student_post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  questionnaire_post_id INTEGER NOT NULL,
  start_time INTEGER,
  end_time INTEGER,
  valid_control INTEGER NOT NULL,
  in_time INTEGER NOT NULL,
  FOREIGN KEY (student_id) REFERENCES student (id),
  FOREIGN KEY (questionnaire_post_id) REFERENCES questionnaire_post (id)
);
