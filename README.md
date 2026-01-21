<style>
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes slideIn {
    from { transform: translateX(-100%); }
    to { transform: translateX(0); }
}
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}
.fade-in { animation: fadeIn 1s ease-out; }
.slide-in { animation: slideIn 0.8s ease-out; }
.pulse { animation: pulse 2s infinite; }
</style>

<div align="center" class="fade-in">

# <span class="pulse">University Management System</span>

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange?style=for-the-badge&logo=mysql)](https://mysql.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## <span class="slide-in">Academic Database Management Platform</span>

A comprehensive web-based system for managing university operations with MySQL database backend and Streamlit frontend interface.

</div>

---

## <span class="slide-in">Key Features</span>

<div class="fade-in">
| Module | Functionality | Technology |
|--------|---------------|------------|
| **Student Management** | Registration, profile updates, directory view | Streamlit Forms |
| **Course Catalog** | Course creation, instructor assignment, credit validation | MySQL Tables |
| **Enrollment System** | Course registration, drop operations, semester tracking | SQL Transactions |
| **Dashboard Analytics** | Real-time metrics, activity monitoring | Pandas DataFrames |
| **Query Interface** | Direct SQL execution with templates | MySQL Connector |
</div>

---

## <span class="slide-in">Installation & Setup</span>

<div class="fade-in">
### Prerequisites
- Python 3.8+
- MySQL Server 8.0+
- pip package manager

### Quick Setup
```bash
# 1. Download and extract project
cd DB_Project_Code

# 2. Create virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup MySQL
mysql -u root -p
CREATE DATABASE UniversityDB;
CREATE USER 'university_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON UniversityDB.* TO 'university_user'@'localhost';
FLUSH PRIVILEGES;

# 5. Import database
mysql -u root -p UniversityDB < UniversityDB_Schema.sql
mysql -u root -p UniversityDB < UniversityDB_Data.sql

# 6. Update app.py with your credentials
# Edit line 64 in app.py with your database credentials

# 7. Launch application
streamlit run app.py
```

**Access:** http://localhost:8501
</div>

---

## <span class="slide-in">Database Schema</span>

<div class="fade-in">
### Tables Overview
- **DEPARTMENT**: Department information and locations
- **INSTRUCTOR**: Faculty member details and assignments
- **STUDENT**: Student records and enrollment data
- **COURSE**: Course catalog with credits and descriptions
- **REGISTRATION**: Student course enrollments and grades

### Key Relationships
- Departments have multiple instructors and students
- Instructors teach multiple courses
- Students register for multiple courses per semester
- Foreign key constraints ensure data integrity
</div>

---

## <span class="slide-in">System Requirements</span>

<div class="fade-in">
### Minimum Requirements
- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 or higher
- **MySQL**: 8.0 or higher
- **RAM**: 4GB
- **Storage**: 500MB

### Recommended
- **OS**: Windows 11, macOS 12+, Ubuntu 22.04+
- **Python**: 3.11+
- **MySQL**: 8.0.33+
- **RAM**: 8GB+
- **Storage**: 2GB+ SSD
</div>

---

## <span class="slide-in">Usage Examples</span>

<div class="fade-in">
### Student Registration
```python
import mysql.connector

# Connect to database
conn = mysql.connector.connect(
    host="localhost",
    user="university_user",
    password="your_password",
    database="UniversityDB"
)

cursor = conn.cursor()

# Register student
student_data = (
    "John", "Doe", "john.doe@university.edu",
    "555-0123", "2000-01-15", 2023, "CS"
)

cursor.execute("""
    INSERT INTO STUDENT (FirstName, LastName, Email, Phone, DateOfBirth, EnrollmentYear, DeptID)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
""", student_data)

conn.commit()
print(f"Student registered with ID: {cursor.lastrowid}")
conn.close()
```
</div>

---

## <span class="slide-in">Project Structure</span>

<div class="fade-in">
```
DB_Project_Code/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── UniversityDB_Schema.sql # Database schema
├── UniversityDB_Data.sql   # Sample data
├── UniversityDB_Queries.sql # Pre-built queries
├── images/               # UI screenshots
└── README.md            # Project documentation
```
</div>

---

## <span class="slide-in">Troubleshooting</span>

<div class="fade-in">
### Common Issues

**Database Connection Error:**
```bash
# Check MySQL service
# Windows: Get-Service mysql*
# Linux: sudo systemctl status mysql
# macOS: brew services list mysql
```

**Port Already in Use:**
```bash
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :8501
kill -9 <PID>
```

**Module Import Error:**
```bash
pip install -r requirements.txt --force-reinstall
```
</div>

---

## <span class="slide-in">License</span>

<div class="fade-in">
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
</div>

---

## <span class="slide-in">Contact</span>

<div class="fade-in">
- **Email**: shaheenmohammedsh@gmail.com
- **Project**: University Management System
</div>

---

<div align="center" class="fade-in">

**Built with dedication for educational institutions**

[Back to Top](#-university-management-system)

</div>
