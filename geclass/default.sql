INSERT INTO program (program_name)
VALUES
  ('Mono Bachelor Physik'),
  ('Bachelor Physik Lehramt'),
  ('Mono Master Physik'),
  ('Master Physik Lehramt'),
  ('Bachelor Nebenfach'),
  ('Master Nebenfach'),
  ('Medizinpraktikum');

INSERT INTO course_type (course_type_name)
VALUES
  ('Grundpraktikum'),
  ('Fortgeschrittenen Praktikum'),
  ('Projektpraktikum');

INSERT INTO focus (focus_name)
VALUES
  ('Vermittlung von Experimentierkompetenzen'),
  ('Physikalische Konzeptvermittlung oder Konzeptvertiefung'),
  ('Beides');

INSERT INTO traditional (traditional_name)
VALUES
  ('Folgen einer detaillierten Anleitung (Traditionelles Praktikum)'),
  ('Offene Gestaltung mit Anleitung'),
  ('Offene Gestaltung ohne Anleitung'),
  ('Anderes');


INSERT INTO equipment (equipment_type)
VALUES
  ('Leybold LD'),
  ('Pasco'),
  ('PHYWE'),
  ('Selbstgebaut'),
  ('Thorlabs'),
  ('Andere');

INSERT INTO experience (experience_level)
VALUES
  ('1./2. Semester'),
  ('3. Semester & später');

INSERT INTO university (university_name)
VALUES
  ('Universität Potsdam'),
  ('Humboldt Universität Berlin');

INSERT INTO university_type (university_type_name)
VALUES
  ('Universität'),
  ('Fachhochschule'),
  ('Andere');
