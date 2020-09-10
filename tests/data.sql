INSERT INTO user (email, password)
VALUES
  ('admin', 'pbkdf2:sha256:50000$3DuknOd6$bb5e82c10ab92c0750bb6c012c1ba5957d647823e4799500d57202930e11f6f8'),
  ('test1@gmail.com', 'pbkdf2:sha256:50000$b3I4RIgB$1db4c82583dd102b5141b2d7eb1777d034bf315dabafa19a987c203fc0e2ec3d'),
  ('test2@web.de', 'pbkdf2:sha256:50000$ZpAT7tJG$bee562ed5dfeee0ee6784b841e73024620d667c350597272e99bcd608d593b19');

INSERT INTO course
  (identifier, user_id, program_id, course_type_id, focus_id, traditional_id, equipment_id,
   experience_id, university_id, university_type_id, number_students,
   students_per_instructor, hours_per_lab, lab_per_lecture, number_labs, number_experiments,
   number_projects, start_date_pre, start_date_post, name,
  frequency_phys_principle, frequency_known_principle, frequency_unknown_principle,
  students_questions, students_plan, students_design, students_apparatus, students_analysis, students_troubleshoot, students_groups,
  modeling_mathematics, modeling_model, modeling_tools, modeling_measurement, modeling_predictions, modeling_uncertainty, modeling_calibrate,
  analysis_uncertainty, analysis_calculate, analysis_computer, analysis_control,
  communication_oral, communication_written, communication_lab, communication_journal, communication_test)
VALUES
  ('abxce', 2, 1, 1, 1, 1, 1, 1, 1, 1, 32, 8, 2.5, 0.5, 0, 10, 0, '123456789', '123456989',
    'Bachelor Physiker', 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
  ('tryui', 2, 2, 2, 2, 2, 2, 2, 2, 1, 16, 8, 1.5, 0.5, 5, 0, 2, '123456789', '123456989',
    'Master Physiker Projekt', 0, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
  ('oiuyt', 3, 3, 1, 2, 2, 1, 2, 1, 2, 25, 3, 3.0, 0.5, 3, 5, 1, '123456889', '123456999',
    'Nebenfach Grundpraktikum', 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
  ('ertyu', 3, 1, 1, 2, 2, 1, 1, 1, 2, 25, 3, 3.0, 0.5, 3, 5, 1, '123456889', '123456999',
    'Bachelor Physiker 2', 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
