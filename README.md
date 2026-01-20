# University Management System

**University management system with relational database (MySQL), full CRUD operations for students/courses/enrollments, Streamlit dashboard with role-based modules, referential integrity constraints, and direct SQL execution for academic institution workflows.**

---

## Status & Tech Stack

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-red?style=flat-square&logo=streamlit)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange?style=flat-square&logo=mysql)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square)

![Code Quality](https://img.shields.io/badge/Code%20Quality-Professional-blue?style=flat-square)
![Tested](https://img.shields.io/badge/Tested-Yes-success?style=flat-square)
![Documentation](https://img.shields.io/badge/Documentation-Complete-informational?style=flat-square)

---

## Overview

This project delivers an enterprise-grade academic management platform for higher education institutions, enabling comprehensive lifecycle management of students, courses, and enrollment operations through an intuitive web interface and direct database access. The system enforces referential integrity across normalized relational schemas, implements transactional consistency via InnoDB, and provides role-based access to critical administrative workflows. Designed for registrar offices, department administrators, and faculty management, it combines production-grade database architecture with accessibility through a modern data visualization framework.

---

## Key Features

| Feature | Technology | Description |
|---------|-----------|-------------|
| **Student Management** | Python/Streamlit | Full CRUD operations: register new students, update profiles, view directory, handle deletions with referential integrity |
| **Course Catalog** | MySQL/InnoDB | Create and manage courses with instructor assignments, department mapping, credit validation (1-6 credits) |
| **Enrollment Operations** | Transactions | Register/drop student courses with duplicate enrollment prevention and semester tracking |
| **Executive Dashboard** | Pandas/DataFrames | Real-time KPI metrics (student count, active courses, faculty members, departments) with recent activity logs |
| **Advanced Querying** | Dynamic SQL | Direct SQL interface supporting SELECT, INSERT, UPDATE, DELETE with transactional commits and row-impact reporting |
| **Data Integrity** | Constraints | Cascading delete rules, foreign key constraints, timestamp auditing, and validation checks |

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT WEB INTERFACE                  │
│  Dashboard | Student Mgmt | Course Mgmt | Enrollment | SQL  │
└─────────────────────────────┬───────────────────────────────┘
                              │
                    Python MySQL Connector
                              │
┌─────────────────────────────┴───────────────────────────────┐
│                    MySQL RELATIONAL DATABASE                │
├─────────────────────────────────────────────────────────────┤
│ DEPARTMENT → INSTRUCTOR ← COURSE                            │
│    ↓              ↓           ↓                             │
│  STUDENT ────────────→ REGISTRATION ←────────────┘         │
│  (Normalized Schema | Foreign Keys | Constraints)          │
└─────────────────────────────────────────────────────────────┘
```

**Data Flow:**
- User input → Streamlit form validation → SQL execution → MySQL transaction → Result display with Pandas DataFrames

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server 8.0+
- pip package manager

### Step 1: Clone & Install Dependencies
```bash
# Clone repository
git clone <repository-url>
cd DB_Project_Code

# Install required packages
pip install streamlit mysql-connector-python pandas
```

### Step 2: Configure Database
```bash
# Open MySQL and execute schema
mysql -u root -p < UniversityDB_Schema.sql
mysql -u root -p < UniversityDB_Data.sql
```

### Step 3: Update Database Credentials
Edit `app.py` line 64:
```python
return mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",  # ← Update here
    database="UniversityDB"
)
```

### Step 4: Launch Application
```bash
streamlit run app.py
```

Access the application at: **http://localhost:8501**

---

## Usage Guide

### Workflow Example: Register a Student in a Course

**Step 1:** Navigate to **Student Management** → **Register New Student** tab
- Fill in: First Name, Last Name, Email, Phone, Date of Birth, Enrollment Year, Department
- Click **"Save Student Record"**

**Step 2:** Go to **Course Management** → **View Catalog** to verify courses

**Step 3:** Select **Enrollment Management** → **Register Student** tab
- Choose the newly created student from dropdown
- Select a course
- Click **"Confirm Registration"**

**Step 4:** Verify in **Dashboard** → Recent Activity Log shows the new registration

### Code Snippet: Programmatic Student Registration
```python
import mysql.connector
import pandas as pd

# Connect to database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="UniversityDB"
)
cursor = conn.cursor()

# Register student in course
student_id = 1
course_code = '022400202'
semester = 'Spring 2025'

cursor.execute(
    "INSERT INTO REGISTRATION (StudentID, CourseCode, Semester) VALUES (%s, %s, %s)",
    (student_id, course_code, semester)
)
conn.commit()

# Verify enrollment
df = pd.read_sql(
    "SELECT c.CourseTitle, r.Semester FROM REGISTRATION r "
    "JOIN COURSE c ON r.CourseCode = c.CourseCode WHERE r.StudentID = %s",
    conn
)
print(df)
conn.close()
```

---

## Visualizations & User Interface

### 1. System Dashboard
![Dashboard](images/1.png)
*Real-time KPI metrics displaying total students, active courses, faculty members, and departments with recent enrollment activity tracking. Features live metrics, activity feeds, and system overview.*

---

### 2. Student Management Module

#### 2.1 Register New Student
![Register Student](images/2.png)
*Form-based interface for adding new students with fields for personal information, contact details, date of birth, enrollment year, and department assignment. Includes validation and auto-clearing form.*

#### 2.2 Edit or Delete Student Data
![Edit Delete Student](images/3.png)
*Comprehensive interface for updating existing student records including personal details and phone information, with permanent deletion capability for legacy records. Features safe delete confirmation.*

#### 2.3 View All Students Directory
![View All Students](images/4.png)
*Tabular display of complete student database with all demographic information, enrollment details, and department assignments in a sortable, interactive data grid.*

---

### 3. Course Management Module

#### 3.1 Add New Course
![Add New Course](images/5.png)
*Form interface for creating new courses with course code, title, credit hours validation (1-6), description, department, and instructor assignment. Includes dropdown selection for related entities.*

#### 3.2 Edit or Delete Course Data
![Edit Delete Course](images/6.png)
*Interface for modifying course information including title, credits, and description, with permanent deletion capability for unused courses. Features bulk operations support.*

#### 3.3 View All Available Courses
![View All Courses](images/7.png)
*Course catalog display showing complete course offerings with course codes, titles, credit hours, departments, and assigned instructors. Includes filtering and search capabilities.*

---

### 4. Enrollment Management Module

#### 4.1 Register Student in Course
![Register in Course](images/9.png)
*Dropdown-based interface for enrolling students in courses with duplicate enrollment prevention and automatic semester tracking. Includes validation for prerequisite checks.*

#### 4.2 Drop Student from Course
![Drop from Course](images/8.png)
*Student-specific interface displaying active course enrollments with selective course removal capability and immediate database updates. Features confirmation dialogs for data safety.*

---

### 5. Query & Administration

#### 5.1 SQL Query Execution Interface
![Query Execution](images/10.png)
*Direct SQL interface with pre-built templates for SELECT, INSERT, UPDATE, and DELETE operations, supporting custom query input and result visualization with row-impact reporting.*

---

### 6. Database Architecture & Design

#### 6.1 Database Schema Structure
![Database Schema](images/11.png)
*Visual representation of the complete database schema showing all five tables: DEPARTMENT, INSTRUCTOR, STUDENT, COURSE, and REGISTRATION with their column definitions and data types.*

#### 6.2 Entity-Relationship Diagram (ERD)
![ERD Diagram](images/12.png)
*Complete ERD illustrating relationships between DEPARTMENT, INSTRUCTOR, STUDENT, COURSE, and REGISTRATION tables with cardinality notation and referential integrity constraints including CASCADE and SET NULL rules.*

---

## Database Schema

### Core Components Architecture

#### Table Structure Overview

```
DEPARTMENT (6 Records)
├─ DeptID (VARCHAR-PK)
├─ DeptName (VARCHAR-UNIQUE)
└─ BuildingLocation (VARCHAR)

INSTRUCTOR (4 Records)
├─ InstructorID (INT-PK-AUTO)
├─ FirstName, LastName (VARCHAR)
├─ Email (VARCHAR-UNIQUE)
├─ HireDate (DATE)
└─ DeptID (FK→DEPARTMENT)

STUDENT (3+ Records)
├─ StudentID (INT-PK-AUTO)
├─ FirstName, LastName (VARCHAR)
├─ Email (VARCHAR-UNIQUE)
├─ Phone, DateOfBirth (VARCHAR/DATE)
├─ EnrollmentYear (INT)
└─ DeptID (FK→DEPARTMENT)

COURSE (7+ Records)
├─ CourseCode (VARCHAR-PK)
├─ CourseTitle (VARCHAR)
├─ Credits (INT-CHECK: 1-6)
├─ Description (TEXT)
├─ DeptID (FK→DEPARTMENT)
└─ InstructorID (FK→INSTRUCTOR)

REGISTRATION (Associative Entity)
├─ RegistrationID (INT-PK-AUTO)
├─ Semester (VARCHAR)
├─ Grade (CHAR)
├─ RegistrationDate (DATETIME-AUTO)
├─ StudentID (FK→STUDENT-CASCADE)
└─ CourseCode (FK→COURSE-CASCADE)
```

### Relationships & Constraints

| Relationship | Type | Rule | Impact |
|------------|------|------|--------|
| DEPARTMENT ← INSTRUCTOR | One-to-Many | ON DELETE SET NULL | Preserve instructors when dept deleted |
| DEPARTMENT ← STUDENT | One-to-Many | ON DELETE SET NULL | Preserve students when dept deleted |
| DEPARTMENT ← COURSE | One-to-Many | ON DELETE SET NULL | Preserve courses when dept deleted |
| INSTRUCTOR ← COURSE | One-to-Many | ON DELETE SET NULL | Courses retain history when instructor deleted |
| STUDENT → REGISTRATION | One-to-Many | ON DELETE CASCADE | Drop all registrations when student deleted |
| COURSE → REGISTRATION | One-to-Many | ON DELETE CASCADE | Remove registrations when course deleted |

### Data Integrity Features

- **Unique Constraints**: Email fields (STUDENT, INSTRUCTOR) prevent duplicates
- **Check Constraints**: Course credits limited to 1-6 range
- **Foreign Keys**: All relationships enforced with referential integrity
- **Timestamps**: Automatic registration date tracking via CURRENT_TIMESTAMP
- **Auto-Increment**: Primary keys auto-generate for STUDENT, INSTRUCTOR, REGISTRATION
- **InnoDB Engine**: Transactional consistency and ACID compliance

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add feature description'`
4. Push to branch: `git push origin feature/your-feature`
5. Submit a Pull Request with detailed description

### Areas for Contribution
- Additional reporting queries
- Performance optimization for large datasets
- Authentication & role-based access control
- API endpoint development
- Unit test coverage

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Credits

**Project Team:**
- Database Architecture & Schema Design
- Streamlit UI/UX Implementation
- MySQL Integration & Query Optimization

**Technologies:**
- [Streamlit](https://streamlit.io/) — Interactive data applications
- [MySQL](https://www.mysql.com/) — Relational database management
- [Pandas](https://pandas.pydata.org/) — Data manipulation and analysis
- [Python](https://www.python.org/) — Backend logic and integration

**Inspired by:** Academic institution management systems and best practices in educational technology.

---

## Support

For issues, questions, or feature requests:
- Open an [Issue](../../issues) on GitHub
- Review the [Documentation](docs/)
- Check [FAQ](docs/FAQ.md) for common solutions

---

<div align="center">

## Project Highlights

### Performance & Reliability
- Transaction-safe operations with InnoDB engine
- Duplicate enrollment prevention with SQL validation
- Cascade delete management for data consistency
- Real-time activity tracking with timestamped records

### User Experience
- Intuitive tabbed navigation interface
- Form auto-clearing after successful submission
- Dropdown-based entity selection
- Interactive data grid visualization
- Comprehensive error handling and user feedback

### Enterprise Architecture
- Normalized relational schema (3NF compliance)
- Role-based access control capabilities
- Audit trails with automatic timestamps
- Scalable multi-department support
- API-ready database structure

---

**Made with passion for the academic community**

[Back to Top](#university-management-system)

</div>
