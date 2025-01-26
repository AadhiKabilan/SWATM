CREATE TABLE buffer_students (
    REG_NO_b       VARCHAR2(15) PRIMARY KEY,  -- Registration Number (as a string to allow for large values)
    NAME_b         VARCHAR2(100) UNIQUE,      -- Student's Name (unique)
    AGE_b          NUMBER(3),                 -- Student's Age
    BRANCH_b       VARCHAR2(50),              -- Student's Branch
    EMAIL_ID_b     VARCHAR2(100),             -- Student's Email ID
    phonenumber_b  VARCHAR2(15),              -- Student's Phone Number (as a string)
    semester_b     NUMBER(2)                 -- Student's Semester   
);
CREATE TABLE students_s (
    REG_NO_s       VARCHAR2(15) PRIMARY KEY,  -- Registration Number (as a string to allow for large values)
    username_s     VARCHAR2(100) UNIQUE,      -- Student's Username (unique)
    password_s     VARCHAR2(100),             -- Student's Password
    NAME_s         VARCHAR2(100) UNIQUE,      -- Student's Name (unique)
    AGE_s          NUMBER(3),                 -- Student's Age
    BRANCH_s       VARCHAR2(50),              -- Student's Branch
    EMAIL_ID_s     VARCHAR2(100),             -- Student's Email ID
    phonenumber_s  VARCHAR2(15),              -- Student's Phone Number (as a string)
    semester_s     NUMBER(2),                 -- Student's Semester
    usertype       VARCHAR2(100)              -- Type of user (e.g., 'student', 'staff', etc.)
);

commit;




CREATE TABLE departments_s (
    department_id NUMBER PRIMARY KEY,
    department_name VARCHAR2(255) NOT NULL
);

CREATE SEQUENCE department_id_seq
START WITH 1
INCREMENT BY 1;

CREATE OR REPLACE TRIGGER department_id_trigger
BEFORE INSERT ON departments_s
FOR EACH ROW
BEGIN
    :NEW.department_id := department_id_seq.NEXTVAL;
END;
/

CREATE TABLE subjects_s (
    subject_id NUMBER PRIMARY KEY,
    department_id NUMBER NOT NULL,  -- Foreign key to departments_s
    subject_name VARCHAR2(255) NOT NULL,
    semester NUMBER NOT NULL,
    CONSTRAINT fk_department
        FOREIGN KEY (department_id) 
        REFERENCES departments_s(department_id)
);

CREATE SEQUENCE subject_id_seq
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;
CREATE OR REPLACE TRIGGER subject_id_trigger
    BEFORE INSERT ON subjects_s
    FOR EACH ROW
BEGIN
    :NEW.subject_id := subject_id_seq.NEXTVAL;
END;
/

CREATE TABLE internal_marks_s (
    mark_id NUMBER PRIMARY KEY,
    reg_no_s VARCHAR2(15) NOT NULL,  -- Foreign key to the students_s table (using REG_NO_s)
    subject_id NUMBER NOT NULL,      -- Foreign key to the subjects_s table
    test_1 NUMBER,                   -- Marks for internal test 1
    test_2 NUMBER,                   -- Marks for internal test 2
    test_3 NUMBER,                   -- Marks for internal test 3

    -- Foreign Key referencing the REG_NO_s column in the students_s table
    CONSTRAINT fk_student
        FOREIGN KEY (reg_no_s) 
        REFERENCES students_s(REG_NO_s),
    
    -- Foreign Key referencing the subject_id column in the subjects_s table
    CONSTRAINT fk_subject
        FOREIGN KEY (subject_id) 
        REFERENCES subjects_s(subject_id)
);

CREATE SEQUENCE mark_id_seq
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE OR REPLACE TRIGGER mark_id_trigger
    BEFORE INSERT ON internal_marks_s
    FOR EACH ROW
BEGIN
    :NEW.mark_id := mark_id_seq.NEXTVAL;
END;
/

