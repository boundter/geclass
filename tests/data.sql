INSERT INTO user (email, password)
VALUES
  ('test1', 'some weird hash'),
  ('test2', 'another weird hash');

INSERT INTO course (user_id, course_identifier)
VALUES
  (1, 'uni_potsdam_biochem_2018'),
  (1, 'uni_potsdam_phys_2018'),
  (2, 'uni_hamburg_phys_2018');
