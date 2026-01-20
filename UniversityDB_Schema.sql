
-- 1. Setup Database
DROP DATABASE IF EXISTS UniversityDB;
CREATE DATABASE UniversityDB;
USE UniversityDB;

-- ==========================================================
-- 2. DDL: Create Tables
-- ==========================================================

-- Important Note: Tables must be created in this order to avoid Foreign Key errors

-- Table 1: DEPARTMENT (Parent Table)
CREATE TABLE DEPARTMENT (
    DeptID VARCHAR(10) NOT NULL PRIMARY KEY,
    DeptName VARCHAR(100) NOT NULL UNIQUE,
    BuildingLocation VARCHAR(150)
) ENGINE=InnoDB;

-- Table 2: INSTRUCTOR (Depends on DEPARTMENT)
CREATE TABLE INSTRUCTOR (
    InstructorID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    HireDate DATE NOT NULL,
    DeptID VARCHAR(10),
    -- Foreign Key Constraint
    CONSTRAINT FK_Instructor_Dept FOREIGN KEY (DeptID) 
    REFERENCES DEPARTMENT(DeptID) 
    ON UPDATE CASCADE 
    ON DELETE SET NULL
) ENGINE=InnoDB;

-- Table 3: STUDENT (Depends on DEPARTMENT)
CREATE TABLE STUDENT (
    StudentID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Phone VARCHAR(20),
    DateOfBirth DATE NOT NULL,
    EnrollmentYear INT NOT NULL,
    DeptID VARCHAR(10),
    -- Foreign Key Constraint
    CONSTRAINT FK_Student_Dept FOREIGN KEY (DeptID) 
    REFERENCES DEPARTMENT(DeptID) 
    ON UPDATE CASCADE 
    ON DELETE SET NULL
) ENGINE=InnoDB;

-- Table 4: COURSE (Depends on DEPARTMENT and INSTRUCTOR)
CREATE TABLE COURSE (
    CourseCode VARCHAR(10) NOT NULL PRIMARY KEY,
    CourseTitle VARCHAR(100) NOT NULL,
    Credits INT NOT NULL,
    Description TEXT,
    DeptID VARCHAR(10),
    InstructorID INT,
    -- Constraints
    CHECK (Credits > 0 AND Credits <= 6),
    CONSTRAINT FK_Course_Dept FOREIGN KEY (DeptID) 
    REFERENCES DEPARTMENT(DeptID) 
    ON UPDATE CASCADE 
    ON DELETE SET NULL,
    CONSTRAINT FK_Course_Instructor FOREIGN KEY (InstructorID) 
    REFERENCES INSTRUCTOR(InstructorID) 
    ON UPDATE CASCADE 
    ON DELETE SET NULL
) ENGINE=InnoDB;

-- Table 5: REGISTRATION (Associative Entity - Depends on STUDENT and COURSE)
CREATE TABLE REGISTRATION (
    RegistrationID INT AUTO_INCREMENT PRIMARY KEY,
    Semester VARCHAR(20) NOT NULL,
    Grade CHAR(2),
    RegistrationDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    StudentID INT NOT NULL,
    CourseCode VARCHAR(10) NOT NULL,
    -- Foreign Key Constraints
    CONSTRAINT FK_Reg_Student FOREIGN KEY (StudentID) 
    REFERENCES STUDENT(StudentID) 
    ON UPDATE CASCADE 
    ON DELETE CASCADE,
    CONSTRAINT FK_Reg_Course FOREIGN KEY (CourseCode) 
    REFERENCES COURSE(CourseCode) 
    ON UPDATE CASCADE 
    ON DELETE CASCADE
) ENGINE=InnoDB;
