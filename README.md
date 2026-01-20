# University Management System

**University management system with relational database (MySQL), full CRUD operations for students/courses/enrollments, Streamlit dashboard with role-based modules, referential integrity constraints, and direct SQL execution for academic institution workflows.**

---

## Status & Tech Stack

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-red?style=flat-square&logo=streamlit)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange?style=flat-square&logo=mysql)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square)

---

## Overview

This project delivers an enterprise-grade academic management platform for higher education institutions, enabling comprehensive lifecycle management of students, courses, and enrollment operations through an intuitive web interface and direct database access. The system enforces referential integrity across normalized relational schemas, implements transactional consistency via InnoDB, and provides role-based access to critical administrative workflows. Designed for registrar offices, department administrators, and faculty management, it combines production-grade database architecture with accessibility through a modern data visualization framework.

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Student Management** | Full CRUD operations: register new students, update profiles, view directory, handle deletions with referential integrity |
| **Course Catalog** | Create and manage courses with instructor assignments, department mapping, credit validation (1-6 credits) |
| **Enrollment Operations** | Register/drop student courses with duplicate enrollment prevention and semester tracking |
| **Executive Dashboard** | Real-time KPI metrics (student count, active courses, faculty members, departments) with recent activity logs |
| **Advanced Querying** | Direct SQL interface supporting SELECT, INSERT, UPDATE, DELETE with transactional commits and row-impact reporting |
| **Data Integrity** | Cascading delete rules, foreign key constraints, timestamp auditing, and validation checks |

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

## Visualizations & Interface

### Dashboard Overview
![Dashboard](images/1.png)
*Real-time KPI metrics and enrollment activity tracking*

### Student Management Module
![Student Management](images/2.png)
*Comprehensive CRUD operations with form validation*

### Course Catalog Interface
![Course Catalog](images/3.png)
*Department-mapped course listings with instructor assignments*

### Enrollment Management
![Enrollment](images/4.png)
*Streamlined course registration with duplicate prevention*

### SQL Query Execution
![SQL Execution](images/5.png)
*Direct database access with result visualization and audit trails*

### Database Schema Diagram
![Schema](images/6.png)
*Normalized relational design with referential integrity constraints*

### Dynamic Workflow Animation
![Workflow GIF](images/workflow.gif)
*Complete end-to-end student registration workflow demonstration*

---

## Database Schema

### Tables & Relationships
- **DEPARTMENT**: Administrative units (6 departments)
- **INSTRUCTOR**: Faculty with hire dates and department assignments
- **STUDENT**: Enrollment records with demographic tracking
- **COURSE**: Course catalog with credits (1-6), descriptions, and instructor mapping
- **REGISTRATION**: Associative entity linking students to courses with semester and grade tracking

**Constraints:**
- Cascading deletes for data consistency
- Unique constraints on emails and identifiers
- Check constraints for credit validation
- Foreign key references with ON DELETE CASCADE/SET NULL

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

**Made with passion for the academic community**

[⬆ Back to Top](#-university-management-system)

</div>
