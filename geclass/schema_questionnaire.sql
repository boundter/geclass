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
  q1 TEXT,
  q2 TEXT,
  q3 TEXT,
  q4 TEXT,
  q5 TEXT,
  q6 TEXT,
  q7 TEXT,
  q8 TEXT,
  q9 TEXT,
  q10 TEXT,
  q11 TEXT,
  q12 TEXT,
  q13 TEXT,
  q14 TEXT,
  q15 TEXT,
  q16 TEXT,
  q17 TEXT,
  q18 TEXT,
  q19 TEXT,
  q20 TEXT,
  q21 TEXT,
  q22 TEXT,
  q23 TEXT,
  q24 TEXT,
  q25 TEXT,
  q26 TEXT,
  q27 TEXT,
  q28 TEXT,
  q29 TEXT,
  q30 TEXT,
  q31 TEXT,
);

CREATE TABLE questionnaire_expert (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  q1 TEXT,
  q2 TEXT,
  q3 TEXT,
  q4 TEXT,
  q5 TEXT,
  q6 TEXT,
  q7 TEXT,
  q8 TEXT,
  q9 TEXT,
  q10 TEXT,
  q11 TEXT,
  q12 TEXT,
  q13 TEXT,
  q14 TEXT,
  q15 TEXT,
  q16 TEXT,
  q17 TEXT,
  q18 TEXT,
  q19 TEXT,
  q20 TEXT,
  q21 TEXT,
  q22 TEXT,
  q23 TEXT,
  q24 TEXT,
  q25 TEXT,
  q26 TEXT,
  q27 TEXT,
  q28 TEXT,
  q29 TEXT,
  q30 TEXT,
  q31 TEXT,
);

CREATE TABLE questionnaire_mark (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  q1 TEXT,
  q2 TEXT,
  q3 TEXT,
  q4 TEXT,
  q5 TEXT,
  q6 TEXT,
  q7 TEXT,
  q8 TEXT,
  q9 TEXT,
  q10 TEXT,
  q11 TEXT,
  q12 TEXT,
  q13 TEXT,
  q14 TEXT,
  q15 TEXT,
  q16 TEXT,
  q17 TEXT,
  q18 TEXT,
  q19 TEXT,
  q20 TEXT,
  q21 TEXT,
  q22 TEXT,
  q23 TEXT,
  q24 TEXT,
  q25 TEXT,
  q26 TEXT,
  q27 TEXT,
  q28 TEXT,
  q29 TEXT,
  q30 TEXT,
  q31 TEXT,
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
  in_time INTEGER NOT NULL,
  FOREIGN KEY (student_id) REFERENCES student (id),
  FOREIGN KEY (questionnaire_post_id) REFERENCES questionnaire_post (id)
);
