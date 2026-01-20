import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date

# ---------------------------------------------------------
# 1. System Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="University Management System",
    layout="wide"
)

# ---------------------------------------------------------
# 2. SQL Queries Repository 
# ---------------------------------------------------------
QUERIES = {
    "Custom SQL Query": "",

    "1. View Student Records":
    """SELECT StudentID, FirstName, LastName, Email, EnrollmentYear, DeptID
FROM STUDENT;""",

    "2. View All Course Details":
    """SELECT CourseCode, CourseTitle, Credits, DeptID, InstructorID
FROM COURSE;""",

    "3. Register Student in Course (Static Example)":
    """INSERT INTO REGISTRATION (Semester, Grade, StudentID, CourseCode)
VALUES ('Spring 2025', NULL, 1, '022400202');""",

    "4. View Courses Registered by a Student (Student ID 1)":
    """SELECT
    R.RegistrationID,
    C.CourseTitle,
    R.Semester,
    R.Grade
FROM REGISTRATION R
JOIN COURSE C ON R.CourseCode = C.CourseCode
WHERE R.StudentID = 1;""",

    "5. View Students Registered in a Course (Course 022400202)":
    """SELECT
    S.StudentID,
    S.FirstName,
    S.LastName,
    R.Semester,
    R.Grade
FROM REGISTRATION R
JOIN STUDENT S ON R.StudentID = S.StudentID
WHERE R.CourseCode = '022400202';""",

    "6. Input Student Grades (Update Registration ID 1)":
    """UPDATE REGISTRATION
SET Grade = 'A'
WHERE RegistrationID = 1;""",

    "7. Add New Course (Example: Data Mining)":
    """INSERT INTO COURSE (CourseCode, CourseTitle, Credits, Description, DeptID, InstructorID)
VALUES ('022400300', 'Data Mining', 3, 'Mining big datasets.', '01', 2);""",

    "8. View Instructors and Their Assigned Courses":
    """SELECT
    I.InstructorID,
    I.FirstName,
    I.LastName,
    C.CourseTitle
FROM INSTRUCTOR I
LEFT JOIN COURSE C ON I.InstructorID = C.InstructorID;""",

    "9. Student Count per Department":
    """SELECT DeptID, COUNT(*) AS NumberOfStudents
FROM STUDENT
GROUP BY DeptID;""",

    "10. Delete Student Registration (Delete Registration ID 2)":
    """DELETE FROM REGISTRATION
WHERE RegistrationID = 2;"""
}

# ---------------------------------------------------------
# 3. Database Connection Helper
# ---------------------------------------------------------
def get_connection():
    """Establishes connection to the MySQL database."""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Update if your DB has a password
            database="UniversityDB"
        )
    except mysql.connector.Error as err:
        st.error(f"Database Connection Error: {err}")
        return None

# ---------------------------------------------------------
# 4. Sidebar Navigation
# ---------------------------------------------------------
st.sidebar.title("University System")
view_selection = st.sidebar.radio(
    "Main Menu",
    [
        "Dashboard",
        "Student Management",
        "Course Management",
        "Enrollment Management",
        "SQL Query Execution"
    ]
)

# ---------------------------------------------------------
# 5. Application Modules
# ---------------------------------------------------------

# === MODULE 1: DASHBOARD ===
if view_selection == "Dashboard":
    st.title("System Dashboard")
    st.markdown("Overview of university key performance indicators.")

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        col1, col2, col3, col4 = st.columns(4)

        # Metrics
        cursor.execute("SELECT COUNT(*) FROM STUDENT")
        col1.metric("Total Students", cursor.fetchone()[0])

        cursor.execute("SELECT COUNT(*) FROM COURSE")
        col2.metric("Active Courses", cursor.fetchone()[0])

        cursor.execute("SELECT COUNT(*) FROM INSTRUCTOR")
        col3.metric("Faculty Members", cursor.fetchone()[0])

        cursor.execute("SELECT COUNT(*) FROM DEPARTMENT")
        col4.metric("Departments", cursor.fetchone()[0])

        st.markdown("---")
        st.subheader("Recent Activity Log")

        # Recent Registration Activity
        recent_activity_query = """
            SELECT r.RegistrationID, s.FirstName, s.LastName, c.CourseTitle, r.Semester
            FROM REGISTRATION r
            JOIN STUDENT s ON r.StudentID = s.StudentID
            JOIN COURSE c ON r.CourseCode = c.CourseCode
            ORDER BY r.RegistrationID DESC LIMIT 5
        """
        df = pd.read_sql(recent_activity_query, conn)
        st.dataframe(df, use_container_width=True, hide_index=True)

        conn.close()

# === MODULE 2: STUDENT MANAGEMENT (FULL CRUD) ===
elif view_selection == "Student Management":
    st.title("Student Administration")

    conn = get_connection()
    if conn:
        # Create 3 Tabs: Create, Update/Delete, Read
        tab_add, tab_manage, tab_view = st.tabs(["Register New Student", "Edit / Delete Student", "View Directory"])

        # --- TAB 1: ADD NEW STUDENT (Auto Clear Form) ---
        with tab_add:
            st.subheader("New Student Registration")
            # 'clear_on_submit=True' solves the issue of fields not refreshing after submission
            with st.form("add_student_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                f_name = col1.text_input("First Name")
                l_name = col2.text_input("Last Name")

                col3, col4 = st.columns(2)
                email = col3.text_input("Email")
                phone = col4.text_input("Phone")

                col5, col6 = st.columns(2)
                dob = col5.date_input("Date of Birth", min_value=date(1990, 1, 1))
                enroll_year = col6.number_input("Enrollment Year", value=2024, step=1)

                # Fetch Departments for dropdown
                cursor = conn.cursor()
                cursor.execute("SELECT DeptID, DeptName FROM DEPARTMENT")
                depts = cursor.fetchall()
                dept_choice = st.selectbox("Department", depts, format_func=lambda x: x[1]) if depts else None

                submitted = st.form_submit_button("Save Student Record")

                if submitted:
                    if f_name and l_name and dept_choice:
                        try:
                            qry = "INSERT INTO STUDENT (FirstName, LastName, Email, Phone, DateOfBirth, EnrollmentYear, DeptID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                            cursor.execute(qry, (f_name, l_name, email, phone, dob, enroll_year, dept_choice[0]))
                            conn.commit()
                            st.success("Student added successfully.")
                            st.rerun() # Refresh to update UI
                        except mysql.connector.Error as e:
                            st.error(f"Database Error: {e}")
                    else:
                        st.warning("First Name, Last Name, and Department are required.")

        # --- TAB 2: EDIT / DELETE STUDENT ---
        with tab_manage:
            st.subheader("Manage Existing Students")

            # Select Student to Edit/Delete
            cursor.execute("SELECT StudentID, FirstName, LastName FROM STUDENT")
            students = cursor.fetchall()
            student_select = st.selectbox("Select Student to Manage", students, format_func=lambda x: f"{x[1]} {x[2]} (ID: {x[0]})")

            if student_select:
                st.markdown("---")
                # Fetch current details for the selected student
                s_id = student_select[0]
                cursor.execute("SELECT * FROM STUDENT WHERE StudentID = %s", (s_id,))
                current_data = cursor.fetchone()

                col_edit, col_delete = st.columns([2, 1])

                # Edit Section
                with col_edit:
                    st.markdown("#### Edit Details")
                    with st.form("edit_student_form"):
                        new_fname = st.text_input("First Name", value=current_data[1])
                        new_lname = st.text_input("Last Name", value=current_data[2])
                        new_email = st.text_input("Email", value=current_data[3])
                        new_phone = st.text_input("Phone", value=current_data[4])

                        update_btn = st.form_submit_button("Update Details")

                        if update_btn:
                            try:
                                update_qry = "UPDATE STUDENT SET FirstName=%s, LastName=%s, Email=%s, Phone=%s WHERE StudentID=%s"
                                cursor.execute(update_qry, (new_fname, new_lname, new_email, new_phone, s_id))
                                conn.commit()
                                st.success("Student details updated successfully.")
                                st.rerun()
                            except mysql.connector.Error as e:
                                st.error(f"Update Failed: {e}")

                # Delete Section
                with col_delete:
                    st.markdown("#### Danger Zone")
                    st.error("Deleting a student record is permanent.")
                    if st.button("Delete Student", type="primary"):
                        try:
                            cursor.execute("DELETE FROM STUDENT WHERE StudentID = %s", (s_id,))
                            conn.commit()
                            st.success("Student deleted successfully.")
                            st.rerun()
                        except mysql.connector.Error as e:
                            st.error(f"Cannot delete: Student has related records (e.g., registration). Error: {e}")

        # --- TAB 3: VIEW ALL ---
        with tab_view:
            st.subheader("Student Directory")
            df = pd.read_sql("SELECT * FROM STUDENT", conn)
            st.dataframe(df, use_container_width=True)

        conn.close()

# === MODULE 3: COURSE MANAGEMENT (FULL CRUD) ===
elif view_selection == "Course Management":
    st.title("Course Catalog Administration")

    conn = get_connection()
    if conn:
        tab_add_c, tab_manage_c, tab_view_c = st.tabs(["Add Course", "Edit / Delete Course", "View Catalog"])

        # --- TAB 1: ADD COURSE ---
        with tab_add_c:
            st.subheader("Create New Course")
            with st.form("add_course_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                c_code = col1.text_input("Course Code (Unique Identifier)")
                c_title = col2.text_input("Course Title")

                col3, col4, col5 = st.columns(3)
                c_credits = col3.number_input("Credits", min_value=1, max_value=6, value=3)

                cursor = conn.cursor()
                cursor.execute("SELECT DeptID, DeptName FROM DEPARTMENT")
                depts = cursor.fetchall()
                c_dept = col4.selectbox("Department", depts, format_func=lambda x: x[1]) if depts else None

                cursor.execute("SELECT InstructorID, FirstName, LastName FROM INSTRUCTOR")
                instructors = cursor.fetchall()
                c_instr = col5.selectbox("Instructor", instructors, format_func=lambda x: f"{x[1]} {x[2]}") if instructors else None

                c_desc = st.text_area("Description")

                if st.form_submit_button("Add Course"):
                    if c_code and c_title and c_dept and c_instr:
                        try:
                            qry = "INSERT INTO COURSE (CourseCode, CourseTitle, Credits, Description, DeptID, InstructorID) VALUES (%s, %s, %s, %s, %s, %s)"
                            cursor.execute(qry, (c_code, c_title, c_credits, c_desc, c_dept[0], c_instr[0]))
                            conn.commit()
                            st.success("Course added successfully.")
                            st.rerun()
                        except mysql.connector.Error as e:
                            st.error(f"Database Error: {e}")
                    else:
                        st.warning("Course Code, Title, Department, and Instructor are required fields.")

        # --- TAB 2: EDIT / DELETE COURSE ---
        with tab_manage_c:
            st.subheader("Manage Courses")
            cursor.execute("SELECT CourseCode, CourseTitle FROM COURSE")
            courses = cursor.fetchall()
            course_select = st.selectbox("Select Course to Manage", courses, format_func=lambda x: f"{x[1]} ({x[0]})")

            if course_select:
                c_code_key = course_select[0]
                cursor.execute("SELECT * FROM COURSE WHERE CourseCode = %s", (c_code_key,))
                curr_c = cursor.fetchone()

                st.markdown("---")
                col_c_edit, col_c_del = st.columns([2, 1])

                with col_c_edit:
                    with st.form("edit_course_form"):
                        new_c_title = st.text_input("Title", value=curr_c[1])
                        new_c_credits = st.number_input("Credits", value=curr_c[2])
                        new_c_desc = st.text_area("Description", value=curr_c[3])

                        if st.form_submit_button("Update Course"):
                            try:
                                cursor.execute("UPDATE COURSE SET CourseTitle=%s, Credits=%s, Description=%s WHERE CourseCode=%s",
                                               (new_c_title, new_c_credits, new_c_desc, c_code_key))
                                conn.commit()
                                st.success("Course updated successfully.")
                                st.rerun()
                            except mysql.connector.Error as e:
                                st.error(f"Update Failed: {e}")

                with col_c_del:
                    st.error("Deleting a course removes it permanently from the catalog.")
                    if st.button("Delete Course", type="primary"):
                        try:
                            cursor.execute("DELETE FROM COURSE WHERE CourseCode = %s", (c_code_key,))
                            conn.commit()
                            st.success("Course deleted successfully.")
                            st.rerun()
                        except mysql.connector.Error as e:
                            st.error(f"Cannot delete: Students are currently registered in this course. Error: {e}")

        # --- TAB 3: VIEW CATALOG ---
        with tab_view_c:
            qry_view = """
                SELECT c.CourseCode, c.CourseTitle, c.Credits, d.DeptName, CONCAT(i.FirstName, ' ', i.LastName) as Instructor
                FROM COURSE c
                LEFT JOIN DEPARTMENT d ON c.DeptID = d.DeptID
                LEFT JOIN INSTRUCTOR i ON c.InstructorID = i.InstructorID
            """
            df = pd.read_sql(qry_view, conn)
            st.dataframe(df, use_container_width=True)

        conn.close()

# === MODULE 4: ENROLLMENT (ADD & DROP) ===
elif view_selection == "Enrollment Management":
    st.title("Enrollment Operations")

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        tab_reg, tab_drop = st.tabs(["Register Student", "Drop Course"])

        # Register
        with tab_reg:
            st.subheader("Assign Course to Student")
            # Using form to clear selection after successful submission
            with st.form("enroll_form", clear_on_submit=True):
                col1, col2 = st.columns(2)

                cursor.execute("SELECT StudentID, FirstName, LastName FROM STUDENT")
                students = cursor.fetchall()
                s_id = col1.selectbox("Student", students, format_func=lambda x: f"{x[1]} {x[2]}") if students else None

                cursor.execute("SELECT CourseCode, CourseTitle FROM COURSE")
                courses = cursor.fetchall()
                c_code = col2.selectbox("Course", courses, format_func=lambda x: f"{x[1]}") if courses else None

                if st.form_submit_button("Confirm Registration"):
                    if s_id and c_code:
                        try:
                            # Check for duplicate enrollment in the same semester
                            cursor.execute("SELECT * FROM REGISTRATION WHERE StudentID=%s AND CourseCode=%s AND Semester='Spring 2025'", (s_id[0], c_code[0]))
                            if cursor.fetchone():
                                st.warning("This student is already enrolled in this course for the current semester.")
                            else:
                                cursor.execute("INSERT INTO REGISTRATION (StudentID, CourseCode, Semester) VALUES (%s, %s, 'Spring 2025')", (s_id[0], c_code[0]))
                                conn.commit()
                                st.success("Student enrolled successfully.")
                        except mysql.connector.Error as e:
                            st.error(f"Database Error: {e}")

        # Drop
        with tab_drop:
            st.subheader("Drop Course")
            cursor.execute("SELECT StudentID, FirstName, LastName FROM STUDENT")
            all_students = cursor.fetchall()
            s_drop = st.selectbox("Select Student", all_students, format_func=lambda x: f"{x[1]} {x[2]}", key="drop_s_sel")

            if s_drop:
                # Dynamic filter: Only show courses this specific student is currently registered for
                cursor.execute("SELECT r.CourseCode, c.CourseTitle FROM REGISTRATION r JOIN COURSE c ON r.CourseCode = c.CourseCode WHERE r.StudentID=%s", (s_drop[0],))
                s_courses = cursor.fetchall()

                if s_courses:
                    c_drop = st.selectbox("Select Course to Drop", s_courses, format_func=lambda x: x[1], key="drop_c_sel")
                    if st.button("Drop Course", type="primary"):
                        cursor.execute("DELETE FROM REGISTRATION WHERE StudentID=%s AND CourseCode=%s", (s_drop[0], c_drop[0]))
                        conn.commit()
                        st.success("Course dropped successfully.")
                        st.rerun()
                else:
                    st.info("No active enrollments found for this student.")

        conn.close()

# === MODULE 5: SQL QUERY EXECUTION (Professionally Handled) ===
elif view_selection == "SQL Query Execution":
    st.title("System Reporting & Direct Execution")
    st.markdown("Execute direct SQL commands on the database regardless of type (SELECT, INSERT, UPDATE, DELETE).")
    st.warning("Caution: Actions like INSERT, UPDATE, and DELETE are irreversible. Proceed with care.")

    # Dropdown populated by the new English QUERIES dictionary
    report_type = st.selectbox("Select SQL Template", list(QUERIES.keys()))

    # Text area for SQL code (editable)
    default_sql = QUERIES[report_type]
    sql_input = st.text_area("SQL Command Editor", value=default_sql, height=250)

    if st.button("Execute Query", type="primary"):
        conn = get_connection()
        if conn:
            try:
                # Strip whitespace and determine the command type based on the first word
                cleaned_sql = sql_input.strip().upper()

                # --- Case 1: Data Retrieval Queries (SELECT) ---
                if cleaned_sql.startswith("SELECT"):
                    # Use pandas read_sql as it's optimized for fetching and displaying result sets
                    df = pd.read_sql(sql_input, conn)
                    st.success(f"Execution Successful. Records found: {len(df)}")
                    st.dataframe(df, use_container_width=True)

                # --- Case 2: Data Modification Queries (INSERT, UPDATE, DELETE) ---
                else:
                    # Use standard cursor execution for commands that do not return a result set
                    cursor = conn.cursor()
                    cursor.execute(sql_input)
                    # CRITICAL STEP: Explicitly commit changes to the database
                    conn.commit()
                    # Display success message indicating row impact instead of a data table
                    st.success(f"Action executed successfully. Rows affected: {cursor.rowcount}")
                    cursor.close()

            except mysql.connector.Error as err:
                # Catch database-specific errors (e.g., foreign key constraints, syntax errors)
                st.error(f"Database execution error: {err}")
            except Exception as e:
                # Catch general Python exceptions during execution
                st.error(f"An unexpected error occurred: {e}")
            finally:
                # Ensure the database connection is closed regardless of outcome
                if conn and conn.is_connected():
                    conn.close()