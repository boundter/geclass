-- Generate two users test1 with password test and test2 with password foo
INSERT INTO user (email, password)
VALUES
  ('test1', 'pbkdf2:sha256:50000$b3I4RIgB$1db4c82583dd102b5141b2d7eb1777d034bf315dabafa19a987c203fc0e2ec3d'),
  ('test2', 'pbkdf2:sha256:50000$ZpAT7tJG$bee562ed5dfeee0ee6784b841e73024620d667c350597272e99bcd608d593b19');

INSERT INTO course (user_id, course_identifier)
VALUES
  (1, 'uni_potsdam_biochem_2018'),
  (1, 'uni_potsdam_phys_2018'),
  (2, 'uni_hamburg_phys_2018');
