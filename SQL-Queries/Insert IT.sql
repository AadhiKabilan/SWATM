
INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Mathematics - I', 1);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Physics', 1);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Chemistry', 1);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'English for Communication', 1);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Workshop and Manufacturing Practice', 1);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Physics Laboratory', 1);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Chemistry Laboratory', 1);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Mathematics - II', 2);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Basic Electrical Engineering', 2);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Programming for Problem Solving', 2);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Engineering Graphics and Computer Aided Drawing', 2);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Environmental Science', 2);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Basic Electrical Engineering Laboratory', 2);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Programming Laboratory', 2);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Electronic Circuits', 3);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Digital System Design', 3);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Data Structures', 3);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Object Oriented Programming using C++ & Java', 3);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Biology for Engineers', 3);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Digital Laboratory', 3);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Data Structures Laboratory', 3);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Object Oriented Programming Laboratory', 3);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Indian Constitution', 3);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Mathematics for Computing', 4);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Operating Systems', 4);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Computer Architecture', 4);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Microprocessors and Applications', 4);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Design and Analysis of Algorithms', 4);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Operating Systems Laboratory with UNIX/Linux', 4);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Microprocessor Laboratory', 4);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Design and Analysis of Algorithms Laboratory', 4);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Database Management System', 5);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Resource Management and Graph Theory', 5);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Computer Networks', 5);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Information Coding Techniques', 5);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Program Elective – I', 5);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Database Management System Laboratory', 5);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Computer Networks Laboratory', 5);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Information Coding Techniques Laboratory', 5);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Essence of Indian Traditional Knowledge', 5);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Software Engineering', 6);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Automata and Formal Languages', 6);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Web Technology', 6);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Program Elective – II', 6);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Program Elective – III', 6);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Entrepreneurship', 6);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Web Technology Laboratory', 6);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Software Engineering Laboratory', 6);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Artificial Intelligence', 7);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Industrial Economics and Management', 7);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Program Elective – IV', 7);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Program Elective – V', 7);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Artificial Intelligence Laboratory', 7);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Seminar', 7);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Mini Project', 7);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Professional Ethics', 7);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Open Elective through SWAYAM', 8);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Internship', 8);

INSERT INTO subjects_s (department_id, subject_name, semester)
VALUES (1, 'Project Work', 8);

Select * from subjects_s where semester=5;
select * from departments_s;

ALTER TABLE internal_marks_s
ADD (TEST1_MARKS Number(3), TEST2_MARKS number(3), TEST3_MARKS number(3));
select * from internal_marks_s;