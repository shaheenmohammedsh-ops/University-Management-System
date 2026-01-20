-- 1-عرض بيانات الطلاب 

SELECT StudentID, FirstName, LastName, Email, EnrollmentYear, DeptID
FROM STUDENT;
-----------------------------------------------------------------------
--2-عرض جميع الكورسات بالتفاصيل 

SELECT CourseCode, CourseTitle, Credits, DeptID, InstructorID
FROM COURSE;
-----------------------------------------------------------------------
-- 3-تسجيل طالب في كورس 

INSERT INTO REGISTRATION (Semester, Grade, StudentID, CourseCode)
VALUES ('Spring 2025', NULL, 1, '022400202');
-----------------------------------------------------------------------
--4-عرض الكورسات المسجل بها طالب معين 

SELECT 
    R.RegistrationID,
    C.CourseTitle,
    R.Semester,
    R.Grade
FROM REGISTRATION R
JOIN COURSE C ON R.CourseCode = C.CourseCode
WHERE R.StudentID = 1;
-----------------------------------------------------------------------
--5-عرض الطلاب المسجلين في كورس معين

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
--6-إدخال درجات الطلاب 

UPDATE REGISTRATION
SET Grade = 'A'
WHERE RegistrationID = 1;
-----------------------------------------------------------------------
--7-إضافة كورس جديد 

INSERT INTO COURSE (CourseCode, CourseTitle, Credits, Description, DeptID, InstructorID)
VALUES ('022400300', 'Data Mining', 3, 'Mining big datasets.', '01', 2);
-----------------------------------------------------------------------
--8-عرض كل مدرس والكورسات التي يدرسها 

SELECT 
    I.InstructorID,
    I.FirstName,
    I.LastName,
    C.CourseTitle
FROM INSTRUCTOR I
LEFT JOIN COURSE C ON I.InstructorID = C.InstructorID;
-----------------------------------------------------------------------
--9-عدد الطلاب في كل قسم 

SELECT DeptID, COUNT(*) AS NumberOfStudents
FROM STUDENT
GROUP BY DeptID;
-----------------------------------------------------------------------
--10-حذف تسجيل طالب 

DELETE FROM REGISTRATION
WHERE RegistrationID = 2;


