-- 1. View Student Records

SELECT StudentID, FirstName, LastName, Email, EnrollmentYear, DeptID
FROM STUDENT;
-----------------------------------------------------------------------
-- 2. View All Course Details 

SELECT CourseCode, CourseTitle, Credits, DeptID, InstructorID
FROM COURSE;
-----------------------------------------------------------------------
-- 3. Register Student in Course 

INSERT INTO REGISTRATION (Semester, Grade, StudentID, CourseCode)
VALUES ('Spring 2025', NULL, 1, '022400202');
-----------------------------------------------------------------------
-- 4. View Courses Registered by a Specific Student 

SELECT 
    R.RegistrationID,
    C.CourseTitle,
    R.Semester,
    R.Grade
FROM REGISTRATION R
JOIN COURSE C ON R.CourseCode = C.CourseCode
WHERE R.StudentID = 1;
-----------------------------------------------------------------------
-- 5. View Students Registered in a Specific Course

SELECT 
    S.StudentID,
    S.FirstName,
    S.LastName,
    R.Semester,
    R.Grade
FROM REGISTRATION R
JOIN STUDENT S ON R.StudentID = S.StudentID
WHERE R.CourseCode = '022400202';
-----------------------------------------------------------------------
-- 6. Input Student Grades 

UPDATE REGISTRATION
SET Grade = 'A'
WHERE RegistrationID = 1;
-----------------------------------------------------------------------
-- 7. Add New Course 

INSERT INTO COURSE (CourseCode, CourseTitle, Credits, Description, DeptID, InstructorID)
VALUES ('022400300', 'Data Mining', 3, 'Mining big datasets.', '01', 2);
-----------------------------------------------------------------------
-- 8. View Instructors and Their Assigned Courses 

SELECT 
    I.InstructorID,
    I.FirstName,
    I.LastName,
    C.CourseTitle
FROM INSTRUCTOR I
LEFT JOIN COURSE C ON I.InstructorID = C.InstructorID;
-----------------------------------------------------------------------
-- 9. Student Count per Department 

SELECT DeptID, COUNT(*) AS NumberOfStudents
FROM STUDENT
GROUP BY DeptID;
-----------------------------------------------------------------------
-- 10. Delete Student Registration 

DELETE FROM REGISTRATION
WHERE RegistrationID = 2;


