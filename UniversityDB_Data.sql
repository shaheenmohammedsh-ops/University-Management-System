-- ==========================================================
-- 3. DML: Insert Sample Data for UniversityDB
-- ==========================================================

-- 1. Insert Departments
INSERT INTO DEPARTMENT (DeptID, DeptName, BuildingLocation) VALUES
('01', 'Computing & Data Sciences', 'Main College Building'),
('02', 'Business Analytics', 'Main College Building'),
('03', 'Intelligent Systems', 'Main College Building'),
('04', 'Media Analytics', 'Main College Building'),
('05', 'Healthcare Informatics', 'Main College Building'),
('06', 'Cybersecurity', 'Main College Building');

-- 2. Insert Instructors
INSERT INTO INSTRUCTOR (FirstName, LastName, Email, HireDate, DeptID) VALUES
('Mahmoud', 'Gamal', 'mahmoud.gamal@alexu.edu.eg', '2015-09-01', '01'),  -- ID: 1
('Yasser', 'Fouad', 'yasser.fouad@alexu.edu.eg', '2010-10-01', '03'),   -- ID: 2
('Haidy', 'Shokry', 'haidy.shokry@alexu.edu.eg', '2018-03-20', '05'),  -- ID: 3
('Christine', 'Basta', 'christine.basta@alexu.edu.eg', '2012-02-15', '01'); -- ID: 4

-- 3. Insert Courses
-- Note: Using explicit IDs for Instructors based on the insertion order above
INSERT INTO COURSE (CourseCode, CourseTitle, Credits, Description, DeptID, InstructorID) VALUES
('022400105', 'Programming I', 3, 'Intro to programming concepts.', '01', 1),
('022400205', 'Machine Learning', 3, 'Supervised and Unsupervised learning.', '01', 1),
('022400109', 'Intro to AI', 3, 'Reasoning and Intelligent agents.', '03', 2),
('022400104', 'Intro to Data Sciences', 3, 'Data ecosystem and representation.', '01', 4),
('022400202', 'Intro to Databases', 3, 'Relational model and SQL.', '01', 3),
('022406201', 'Intro to Cybersecurity', 3, 'Info security basics.', '06', NULL),
('022400101', 'Linear Algebra', 3, 'Matrices and Vectors.', '01', NULL);

-- 4. Insert Students
INSERT INTO STUDENT (FirstName, LastName, Email, Phone, DateOfBirth, EnrollmentYear, DeptID) VALUES
('Youssef', 'Kamel', 'y.kamel.st@alexu.edu.eg', '01012345678', '2005-05-10', 2023, '01'), -- ID: 1
('Sara', 'Ali', 's.ali.st@alexu.edu.eg', '01298765432', '2006-08-15', 2024, '03'),    -- ID: 2
('Kareem', 'Hassan', 'k.hassan.st@alexu.edu.eg', '01155667788', '2004-01-20', 2022, '06'); -- ID: 3

-- 5. Insert Registrations
INSERT INTO REGISTRATION (Semester, Grade, StudentID, CourseCode) VALUES
('Fall 2024', 'A-', 1, '022400202'), -- Youssef takes DB
('Spring 2025', NULL, 1, '022400104'), -- Youssef takes Data Science
('Spring 2025', NULL, 2, '022400109'), -- Sara takes AI
('Spring 2025', NULL, 2, '022400105'), -- Sara takes Programming
('Fall 2024', 'A', 3, '022406201');    -- Kareem takes CyberSec

