-- Generate two users test1 with password test and test2 with password foo
INSERT INTO user (email, password)
VALUES
  ('test1@gmail.com', 'pbkdf2:sha256:50000$b3I4RIgB$1db4c82583dd102b5141b2d7eb1777d034bf315dabafa19a987c203fc0e2ec3d'),
  ('test2@web.de', 'pbkdf2:sha256:50000$ZpAT7tJG$bee562ed5dfeee0ee6784b841e73024620d667c350597272e99bcd608d593b19');

INSERT INTO program (program_name)
VALUES
  ('Bachelor Physik'),
  ('Master Physik'),
  ('Bachelor Nebenfach');

INSERT INTO course_type (course_type_name)
VALUES
  ('Grundpraktikum'),
  ('Fortgeschritenen Praktikum');

INSERT INTO focus (focus_name)
VALUES
  ('Konzepte'),
  ('Fähigkeiten'),
  ('Konzepte & Fähigkeiten');

INSERT INTO traditional (traditional_name)
VALUES
  ('Traditionelles Praktikum'),
  ('Nicht-Traditionelles Praktikum');


INSERT INTO equipment (equipment_type)
VALUES
  ('Generisch'),
  ('PHYWE');

INSERT INTO experience (experience_level)
VALUES
  ('1./2. Semester'),
  ('3. Semester & später');

INSERT INTO university (university_name)
VALUES
  ('Universität Potsdam'),
  ('Humboldt Universität Berlin');

INSERT INTO notes (notes_text)
VALUES
  ('');

INSERT INTO course
  (user_id, program_id, course_type_id, focus_id, traditional_id, equipment_id,
   experience_id, university_id, notes_id, number_students,
   students_per_instructor, lab_per_lecture, number_experiments,
   number_projects, start_date_pre, start_date_post, name)
VALUES
  (1, 1, 1, 1, 1, 1, 1, 1, 1, 32, 8, 0.5, 10, 0, '123456789', '123456989',
    'Bachelor Physiker'),
  (1, 2, 2, 2, 2, 2, 2, 2, 1, 16, 8, 0.5, 0, 2, '123456789', '123456989',
    'Master Physiker Projekt'),
  (2, 3, 1, 2, 2, 1, 2, 1, 1, 25, 3, 0.5, 5, 1, '123456889', '123456999',
    'Nebenfach Grundpraktikum');
