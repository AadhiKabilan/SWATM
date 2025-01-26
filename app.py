import pyodbc
from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection string
def get_db_connection():
    return pyodbc.connect(
        'DSN=OracleDSN1;'
        'UID=Aadhi;'
        'PWD=123;'
    )

# Login route
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']
    connection = get_db_connection()
    cursor = connection.cursor()

    # Check login
    cursor.execute("SELECT * FROM students_s WHERE username_s=? AND password_s=?", (username, password))
    user = cursor.fetchone()
    if user:
        session['username'] = username
        if user[-1] == 'staff':
            return redirect(url_for('staff_page'))
        else:
            return redirect(url_for('student_page'))
    else:
        return "Invalid credentials, please try again."

# Sign-in route
@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/sign_in', methods=['POST'])
def handle_sign_in():
    usertype = request.form['usertype']
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        if usertype == 'staff':
            reg_no = random.randint(1000000000, 2000000000)
            username = request.form['username']
            password = request.form['password']

            # Check for existing REG_NO_S
            cursor.execute("SELECT COUNT(*) FROM students_s WHERE REG_NO_S = ?", (reg_no,))
            if cursor.fetchone()[0] > 0:
                return f"Error: REG_NO_S {reg_no} already exists."

            # Check for existing USERNAME_S
            cursor.execute("SELECT COUNT(*) FROM students_s WHERE USERNAME_S = ?", (username,))
            if cursor.fetchone()[0] > 0:
                return f"Error: USERNAME_S {username} already exists."

            # Validate data
            if not username or not password:
                return "Error: Username and Password are required."

            # Insert new staff record
            cursor.execute(
                "INSERT INTO students_s (REG_NO_S, USERNAME_S, PASSWORD_S, USERTYPE) VALUES (?, ?, ?, ?)",
                (reg_no, username, password, usertype)
            )
            connection.commit()
            return f"Staff registered successfully with REG_NO: {reg_no}"

        elif usertype == 'student':
            reg_no = request.form['reg_no']
            username = request.form['username']
            password = request.form['password']

            # Check for required fields
            if not reg_no or not username or not password:
                return "Error: REG_NO_S, Username, and Password are required."

           

            cursor.execute("SELECT COUNT(*) FROM students_s WHERE REG_NO_S = ?", (reg_no))
            exists = cursor.fetchone()[0] > 0

            if exists:
        # Update existing record
                cursor.execute(
                 """
                 UPDATE students_s 
                 SET USERNAME_S = ?, PASSWORD_S = ? 
                 WHERE REG_NO_S = ?
                 """,
                (username, password, reg_no)
                )
                connection.commit()
                return f"Record updated for REG_NO_S: {reg_no}"
            else:
        # Insert new student record
                return "Register Number Doesn't Exist"

        else:
            return "Invalid user type."

    except pyodbc.Error as e:
        print("Database Error:", e)
        return f"A database error occurred: {e}"
    finally:
        if connection:
            connection.close()


@app.route('/fetch_recordn', methods=['GET'])
def fetch_recordn():
    reg_no = request.args.get('reg_no')
    if not reg_no:
        return jsonify({"error": "Register number is required"}), 400

    try:
        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Fetch the record from buffer_students
        cursor.execute("SELECT * FROM buffer_students WHERE REG_NO_b = ?", (reg_no,))
        record = cursor.fetchone()

        if record:
            # Return the record as JSON
            return jsonify({
                "reg_no": record[0],
                "name": record[1],
                "age": record[2],
                "branch": record[3],
                "email": record[4],
                "phone": record[5],
                "semester": record[6]
            })
        else:
            return jsonify({"error": "Record not found"}), 404
    except Exception as e:
        print(f"Error fetching record: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()

# Student Page
@app.route('/student')
def student_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students_s WHERE username_s=?", (username,))
    student_details = cursor.fetchone()
    return render_template('student.html', student=student_details)

# Staff Page
@app.route('/staff')
def staff_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT REG_NO_s, NAME_s, AGE_s, BRANCH_s, EMAIL_ID_s, phonenumber_s, semester_s FROM students_s WHERE usertype='student' ORDER BY REG_NO_S ASC")
    students = cursor.fetchall()
    return render_template('staff.html', students=students)

# Load data from students_s to buffer_students
@app.route('/load_data', methods=['POST'])
def load_data():
    """
    Load all records with usertype='student' from students_s into buffer_students.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Clear the buffer_students table
        cursor.execute("DELETE FROM buffer_students")
        cursor.execute("COMMIT")

        # Insert only records with usertype='student' into buffer_students
        cursor.execute("""
            INSERT INTO buffer_students (REG_NO_b, NAME_b, AGE_b, BRANCH_b, EMAIL_ID_b, phonenumber_b, semester_b)
            SELECT REG_NO_s, NAME_s, AGE_s, BRANCH_s, EMAIL_ID_s, phonenumber_s, semester_s
            FROM students_s
            WHERE usertype = 'student'
        """)
        cursor.execute("COMMIT")

        return "Buffer loaded with student records successfully."
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route('/insert_or_update_buffer', methods=['POST'])
def insert_or_update_buffer():
    """
    Insert or update multiple records in buffer_students table.
    Expects JSON array of student records.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        data = request.json  # This will get the array of student records

        # Validate if each student has all required fields
        for student in data:
            required_fields = ["reg_no", "name", "age", "branch", "email", "phone", "semester"]
            for field in required_fields:
                if not student.get(field):
                    return jsonify({"error": f"Missing value for {field} in student record."}), 400

            # Execute the MERGE operation if all fields are valid
            cursor.execute("""
                MERGE INTO buffer_students b
                USING (SELECT ? AS reg_no, ? AS name, ? AS age, ? AS branch, ? AS email, ? AS phone, ? AS semester FROM dual) new_data
                ON (b.REG_NO_b = new_data.reg_no)
                WHEN MATCHED THEN
                    UPDATE SET
                        NAME_b = new_data.name,
                        AGE_b = new_data.age,
                        BRANCH_b = new_data.branch,
                        EMAIL_ID_b = new_data.email,
                        phonenumber_b = new_data.phone,
                        semester_b = new_data.semester
                WHEN NOT MATCHED THEN
                    INSERT (REG_NO_b, NAME_b, AGE_b, BRANCH_b, EMAIL_ID_b, phonenumber_b, semester_b)
                    VALUES (new_data.reg_no, new_data.name, new_data.age, new_data.branch, new_data.email, new_data.phone, new_data.semester)
            """, (
                student["reg_no"],
                student["name"],
                student["age"],
                student["branch"],
                student["email"],
                student["phone"],
                student["semester"],
            ))

        connection.commit()
        return "Records saved in buffer successfully."
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()


@app.route('/fetch_buffer', methods=['GET'])
def fetch_buffer():
    """
    Fetch all records from the buffer_students table in ascending order by reg_no.
    Returns:
        JSON response containing all student records.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Fetch all records from buffer_students ordered by reg_no in ascending order
        cursor.execute("""
            SELECT REG_NO_b, NAME_b, AGE_b, BRANCH_b, EMAIL_ID_b, phonenumber_b, semester_b 
            FROM buffer_students
            ORDER BY REG_NO_b ASC  -- Ensure ascending order
        """)
        rows = cursor.fetchall()

        # Convert rows to a list of dictionaries
        students = [
            {
                "reg_no": row[0],
                "name": row[1],
                "age": row[2],
                "branch": row[3],
                "email": row[4],
                "phone": row[5],
                "semester": row[6],
            }
            for row in rows
        ]

        # Return data as JSON
        return jsonify(students)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        connection.close()



# Fetch a specific record by register number
@app.route('/fetch_record', methods=['GET'])
def fetch_record():
    reg_no = request.args.get('reg_no')
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM buffer_students WHERE REG_NO_b = ?", (reg_no,))
        record = cursor.fetchone()

        if record:
            return jsonify({
                "reg_no": record[0],
                "name": record[1],
                "age": record[2],
                "branch": record[3],
                "email": record[4],
                "phone": record[5],
                "semester": record[6]
            })
        else:
            return "Record not found.", 404
    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        connection.close()

# Insert a new record into buffer_students
@app.route('/insert_record', methods=['POST'])
def insert_record():
    try:
        data = request.json
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO buffer_students 
            (REG_NO_b, NAME_b, AGE_b, BRANCH_b, EMAIL_ID_b, phonenumber_b, semester_b) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (data['reg_no'], data['name'], data['age'], data['branch'], data['email'], data['phone'], data['semester']))
        cursor.execute("COMMIT")

        return "Record inserted successfully."
    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        connection.close()

# Commit data from buffer_students to students_s
@app.route('/commit_data', methods=['POST'])
def commit_data():
    """
    Commit all records from buffer_students to students_s.
    Update existing records, insert new ones, and delete records marked for deletion.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Update existing records and insert new ones from buffer_students
        cursor.execute("""
            MERGE INTO students_s s
            USING buffer_students b
            ON (s.REG_NO_s = b.REG_NO_b)
            WHEN MATCHED THEN
                UPDATE SET
                    NAME_s = b.NAME_b,
                    AGE_s = b.AGE_b,
                    BRANCH_s = b.BRANCH_b,
                    EMAIL_ID_s = b.EMAIL_ID_b,
                    phonenumber_s = b.phonenumber_b,
                    semester_s = b.semester_b
            WHEN NOT MATCHED THEN
                INSERT (REG_NO_s, NAME_s, AGE_s, BRANCH_s, EMAIL_ID_s, phonenumber_s, semester_s, usertype)
                VALUES (b.REG_NO_b, b.NAME_b, b.AGE_b, b.BRANCH_b, b.EMAIL_ID_b, b.phonenumber_b, b.semester_b, 'student')
        """)
        
        # Commit changes
        connection.commit()

        return "Committed successfully."
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route('/delete_record', methods=['POST'])
def delete_record():
    """
    Delete a specific record from buffer_students table
    """
    try:
        data = request.json
        reg_no = data.get('reg_no')
        
        if not reg_no:
            return jsonify({"error": "No registration number provided"}), 400
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Delete the specific record from buffer_students
        cursor.execute("DELETE FROM buffer_students WHERE REG_NO_b = ?", (reg_no,))
        connection.commit()
        
        return jsonify({"message": "Record deleted successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()
            
@app.route('/data_entry', methods=['GET'])
def data_entry():
    return render_template('data_entry.html')

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    # Ensure the user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        username = session['username']

        # Check if the current password is correct
        if not check_current_password(username, current_password):
            return "Current password is incorrect."

        # Check if the new password matches the confirmation
        if new_password != confirm_password:
            return "New passwords do not match."

        # Update the password in the database
        update_password(username, new_password)
        return "Password successfully changed."

    return render_template('change_password.html')

def check_current_password(username, current_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password_s FROM students_s WHERE username_s = ?", 
        (username,)
    )
    stored_password = cursor.fetchone()
    conn.close()
    return stored_password and stored_password[0] == current_password

def update_password(username, new_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE students_s SET password_s = ? WHERE username_s = ?",
        (new_password, username)
    )
    conn.commit()
    conn.close()





@app.route('/insert_or_update_buffer2', methods=['POST'])
def insert_or_update_buffer2():
    """
    Insert or update multiple records in buffer_students table.
    Expects JSON array of student records.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        data = request.json  # The student data sent from the frontend

        # Loop through each student record
        for student in data:
            cursor.execute("""
                MERGE INTO buffer_students b
                USING (SELECT ? AS reg_no, ? AS name, ? AS age, ? AS branch, ? AS email, ? AS phone, ? AS semester FROM dual) new_data
                ON (b.REG_NO_b = new_data.reg_no)
                WHEN MATCHED THEN
                    UPDATE SET
                        NAME_b = new_data.name,
                        AGE_b = new_data.age,
                        BRANCH_b = new_data.branch,
                        EMAIL_ID_b = new_data.email,
                        phonenumber_b = new_data.phone,
                        semester_b = new_data.semester
                WHEN NOT MATCHED THEN
                    INSERT (REG_NO_b, NAME_b, AGE_b, BRANCH_b, EMAIL_ID_b, phonenumber_b, semester_b)
                    VALUES (new_data.reg_no, new_data.name, new_data.age, new_data.branch, new_data.email, new_data.phone, new_data.semester)
            """, (
                student["reg_no"],
                student["name"],
                student["age"],
                student["branch"],
                student["email"],
                student["phone"],
                student["semester"],
            ))

        connection.commit()
        return jsonify({"message": "Records inserted/updated in buffer successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()


@app.route('/logout')
def logout():
    # Clear the session to log the user out
    session.pop('username', None)  # Remove the student ID from the session

    # Redirect the user to the login page
    return redirect(url_for('login')) 


@app.route('/update_student_details', methods=['POST'])
def update_student_details():
    username = session.get('username')  # Get the username from the session
    if not username:
        return jsonify({"error": "User not logged in"}), 403  # Ensure that the user is logged in

    # Get the updated details from the request body
    data = request.get_json()  # Ensure the data is properly parsed as JSON

    # Extract the updated values
    age = data.get('age')
    email = data.get('email')
    phone = data.get('phone')
    semester = data.get('semester')

    if not (age and email and phone and semester):  # Basic validation to ensure values are provided
        return jsonify({"error": "All fields are required."}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # SQL query to update the student's details
        cursor.execute("""
            UPDATE students_s
            SET AGE_s = ?, EMAIL_ID_s = ?, phonenumber_s = ?, semester_s = ?
            WHERE username_s = ?
        """, (age, email, phone, semester, username))

        connection.commit()  # Commit the changes
        return jsonify({"message": "Details updated successfully."})  # Send success response

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error if something goes wrong
    finally:
        connection.close()



@app.route('/get_student_details', methods=['GET'])
def get_student_details():
    username = session.get('username')  # Get the username from the session
    if not username:
        return redirect('/login')  # Redirect to login page if not logged in
    
    try:
        connection = get_db_connection()  # Your database connection method
        cursor = connection.cursor()
        
        # Fetch student details using the username
        cursor.execute("""
            SELECT REG_NO_s, NAME_s, AGE_s, BRANCH_s, EMAIL_ID_s, phonenumber_s, semester_s
            FROM students_s
            WHERE username_s = ?
        """, (username,))
        
        student = cursor.fetchone()
        if not student:
            return jsonify({"error": "Student not found."}), 404
        
        # Send the student details as a response
        student_data = {
            'reg_no': student[0],
            'name': student[1],
            'age': student[2],
            'branch': student[3],
            'email': student[4],
            'phone': student[5],
            'semester': student[6],
        }
        
        return jsonify(student_data)  # Return student details in JSON format
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()


@app.route('/student_edit', methods=['GET'])
def edit_student_details():
    # This route will render the student edit page.
    return render_template('student_edit.html')


@app.route('/update_internal_marks', methods=['GET', 'POST'])
def update_internal_marks():
    if 'username' not in session:
        return redirect(url_for('login'))  # If not logged in, redirect to login page

    username = session['username']
    
    # Get the student details from the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get student details from 'students_s' table based on username
    cursor.execute('SELECT reg_no_s, branch_s, semester_s FROM students_s WHERE username_s = ?', (username,))
    student = cursor.fetchone()

    if not student:
        return "Student not found", 404  # If student not found, return error

    reg_no_s, branch_s, semester_s = student

    # Get department_id from 'departments_s' table based on branch_s (department name)
    cursor.execute('SELECT department_id FROM departments_s WHERE department_name = ?', (branch_s,))
    department_id_result = cursor.fetchone()

    if not department_id_result:
        return "Department not found", 404  # If department not found, return error

    department_id = department_id_result[0]  # Extract department_id from the result

    # Fetch subjects for the student's department and semester
    cursor.execute('SELECT subject_id, subject_name FROM subjects_s WHERE department_id = ? AND semester = ?', (department_id, semester_s))
    subjects = cursor.fetchall()

    # Fetch existing marks for the student for each subject
    marks = {}
    for subject_id, _ in subjects:
        cursor.execute('SELECT TEST_1, TEST_2, TEST_3 FROM internal_marks_s WHERE reg_no_s = ? AND subject_id = ?', (reg_no_s, subject_id))
        existing_marks = cursor.fetchone()
        if existing_marks:
            marks[subject_id] = {
                'test1': existing_marks[0],
                'test2': existing_marks[1],
                'test3': existing_marks[2]
            }
        else:
            marks[subject_id] = {'test1': '', 'test2': '', 'test3': ''}  # If no marks, set to empty

    if request.method == 'POST':
        # Loop through the subjects and update internal marks for all three tests
        for subject in subjects:
            subject_id, _ = subject
            test1_marks = request.form.get(f"test1_{subject_id}")
            test2_marks = request.form.get(f"test2_{subject_id}")
            test3_marks = request.form.get(f"test3_{subject_id}")
            
            if test1_marks and test2_marks and test3_marks:  # If all marks are provided
                # Use MERGE to either update or insert marks for each test
                cursor.execute('''
    MERGE INTO internal_marks_s im
    USING dual
    ON (im.reg_no_s = ? AND im.subject_id = ?)
    WHEN MATCHED THEN
        UPDATE SET
            im."TEST_1" = ?, 
            im."TEST_2" = ?, 
            im."TEST_3" = ?
    WHEN NOT MATCHED THEN
        INSERT (reg_no_s, subject_id, "TEST_1", "TEST_2", "TEST_3") 
        VALUES (?, ?, ?, ?, ?)
''', (reg_no_s, subject_id, test1_marks, test2_marks, test3_marks, 
      reg_no_s, subject_id, test1_marks, test2_marks, test3_marks))

        # Commit changes after all updates
        conn.commit()
        return redirect(url_for('update_internal_marks'))  # Reload the page after updating marks

    # Close the database connection
    conn.close()

    return render_template('update_internal_marks.html', subjects=subjects, marks=marks)

@app.route('/view_marks', methods=['GET', 'POST'])
def view_marks():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect if not logged in

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all students for the dropdown list
    cursor.execute('SELECT reg_no_s, name_s FROM students_s')
    students = cursor.fetchall()

    # Initialize marks and selected student variables
    marks = {}
    selected_student = None

    if request.method == 'POST':
        # Get the selected student's registration number from the form
        selected_student = request.form['student_reg_no']

        if selected_student:
            # Fetch marks for the selected student
            cursor.execute('''SELECT im.subject_id, sub.subject_name, im.test1_marks, im.test2_marks, im.test3_marks
                  FROM internal_marks_s im
                  JOIN subjects_s sub ON im.subject_id = sub.subject_id
                  WHERE im.reg_no_s = ?''', (selected_student,))

            marks = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Render the page with the list of all students or marks of the selected student
    return render_template('view_marks.html', students=students, marks=marks, selected_student=selected_student)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
