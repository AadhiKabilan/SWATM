
# SWATM (Semester-Wise Academic Tracking And Management)

SWATM is a web-based application developed for the management of student attendance and academic tracking. The system helps staff to enter and manage student attendance, while students can view their attendance and academic performance. The application also sends notifications when attendance or grades fall below a specified threshold.

## Features

- **Student Dashboard**: 
  - View attendance and academic performance.
  - Receive email notifications when performance is low.
  
- **Staff Dashboard**: 
  - Manage subjects and courses.
  - Input and update attendance and internal marks for students.

- **Admin Panel**:
  - Manage the entire system, including staff and student records.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript, Tailwind CSS
- **Backend**: Python (Flask/Pyodbc), or any relevant backend framework you used
- **Database**: Oracle SQL
- **Database Management**: Oracle SQL Developer
- **Version Control**: Git, GitHub
- **Email Service**: SMTP for sending email notifications

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AadhiKabilan/SWATM.git

2. Navigate to the project directory:
   ```bash
   cd SWATM

3. Install the required dependencies: If you're using Python, install the dependencies via
   ```bash
   pip install -r requirements.txt

4. Set up the database: Create the database and tables using the SQL scripts provided in sql create table.txt.
    ```bash
    sql create table.txt -> file
5. Run the application:
   ```bash
   python app.py

6. Visit http://localhost:5000 in your web browser to start using the application.
   ```bash
   http://localhost:5000

## Usage

Students can view their attendance and academic status.

Staff can log in to manage subject data and update attendance and marks.

## Contact

For any questions or feedback, feel free to contact me via email at jaadhikabilan@gmail.com.

## Screen Shots

### Here is the Staff data-entry page:
![Capture Image](images/Capture.JPG)
### Here is the Login page:
![Capture Image](images/Capture2.JPG)
### Here is the Student page:
![Capture Image](images/Capture3.JPG)
### Here is the buffer_table in OracleSQL Developer:
![Capture Image](images/Capture4.JPG)

