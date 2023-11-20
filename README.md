# Mini Canvas

Mini Canvas is a lightweight learning management application, inspired by Canvas, built by Cytro. This mini version provides simplified features for managing users, courses, and enrollments.

## Setup

Follow these steps to set up Mini Canvas:

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:

   ```bash
   python main.py
   ```

3. Log in as the super admin:

   - Username: **`admin`**
   - Password: **`admin`**

4. The default database route is '/data'. You can customize this in the **`main.py`** file.

## Usage

The main entry point of the application is the **`main.py`** file. It provides functionality for user login and different flows for administrators and students.

### User Login

- Users can log in with their username and password.
- The application supports a maximum number of login attempts to enhance security.

### Admin Flow

- Admins have access to a set of actions, including viewing users, courses, enrollments, creating new students, admins, courses, and enrolling users in courses.

### Student Flow

- Students can view their courses and exit the application

## Application Structure

The application consists of several modules:

- **`main.py`**: The main script to run the application.
- **`classes/user.py`**: Defines the User, Admin, and Student classes.
- **`classes/course.py`**: Defines the Course class.
- **`classes/enrollment.py`**: Defines the Enrollment class.
- **`classes/database.py`**: Manages the application's data storage and retrieval.
- **`utils/utilities.py`**: Contains utility functions used throughout the application.

## Database Class

The **`Database`** class provides functionality to interact with user, course, and enrollment data in the Mini Canvas application. It manages the storage of this data in CSV files, allowing for reading, writing, and querying operations.

### Class Initialization

```python
class Database:
    def __init__(self, folder_path='data'):
        """
        Initialize the Database object with file paths for users, courses, and enrollments.

        Parameters:
        - folder_path (str): Folder path to store all CSV files
        """
```

- **`folder_path`** (optional): The folder path where the CSV files will be stored. The default is 'data'.

### File Structure

The class organizes data into three CSV files:

- **`users.csv`** for user records.
- **`courses.csv`** for course records.
- **`enrollments.csv`** for enrollment records.

### Methods

Check and Create Files

```python
def _check_and_create_files(self):
    """
    Check if the CSV files exist, and create them if they don't.
    """
```

Create Super Admin

```python
def _create_super_admin(self):
    """
    Create a super admin with default info.
    """
```

Check Folder Path

```python
def _check_folder_path(self):
    # Create the folder if it doesn't exist
    os.makedirs(self.folder_path, exist_ok=True)
```

Create File with Header

```python
def _create_file_with_header(self, file_path: str):
    """
    Create a CSV file with the appropriate header.

    Parameters:
    - file_path (str): The path of the CSV file to be created.
    """
```

Check If Field Is Unique

```python
def is_field_unique(self, record_type: str, field: str, value: str):
    """
    Check if a particular field is unique for a given record type.

    Parameters:
    - record_type (str): The type of record (user, course, or enrollment).
    - field (str): The field to check for uniqueness.
    - value (str): The value to check for uniqueness.

    Returns:
    - bool: True if the field is unique, False otherwise.

    Raises:
    - ValueError: If record_type is invalid.
    """
```

Is Enrollment Unique

```python
def is_enrollment_unique(self, user_id, course_id):
    """
    Check if an enrollment with the given user_id and course_id is unique.

    Parameters:
    - user_id (str): The user ID to check for uniqueness.
    - course_id (str): The course ID to check for uniqueness.

    Returns:
    - bool: True if the enrollment is unique, False otherwise.
    """
```

Read Users

```python
def read_users(self):
    """
    Read user records from the users CSV file.

    Returns:
    - list[User]: A list of either Admin or Student based on the role.
    """
```

Read User

```python
def read_user(self, id="", username=""):
    """
    Read a user record from the users CSV file based on id or username.

    Parameters:
    - id (str): Optional. The user ID to filter by.
    - username (str): Optional. The username to filter by.

    Returns:
    - Admin, Student or None: Admin or Student record if a match is found, None otherwise.
    """
```

Write User

```python
def write_user(self, user: dict):
    """
    Write a user record to the users CSV file.

    Parameters:
    - user (dict): A dictionary representing a user record.

    Raises:
    - ValueError: If username is not unique.
    """
```

Read Courses

```python
def read_courses(self):
    """
    Read course records from the courses CSV file.

    Returns:
    - list[Course]: A list of courses.
    """
```

Read Course

```python
def read_course(self, id: str):
    """
    Read a course record from the users CSV file based on id.

    Parameters:
    - id (str): The course ID to filter by.

    Returns:
    - Course or None: Course record if a match is found, None otherwise.
    """
```

Write Course

```python
def write_course(self, course: dict):
    """
    Write a course record to the users CSV file.

    Parameters:
    - course (dict): A dictionary representing a course record.
    """
```

Read Enrollments

```python
def read_enrollments(self):
    """
    Read enrollment records from the courses CSV file.

    Returns:
    - list[Enrollment]: A list of enrollments.
    """
```

Read Enrollment

```python
def read_enrollment(self, id: str):
    """
    Read an enrollment record from the users CSV file based on id.

    Parameters:
    - id (str): The enrollment ID to filter by.

    Returns:
    - Enrollment or None: Enrollment record if a match is found, None otherwise.
    """
```

Query Enrollments

```python
def query_enrollments(self, user_id="", username="", course_id=""):
    """
    Read enrollment records from the enrollments CSV file based on user_id, username, or course_id.

    Parameters:
    - user_id (str): Optional. The user ID to filter by.
    - username (str): Optional. The username to filter by.
    - course_id (str): Optional. The course ID to filter by.

    Returns:
    - list[Enrollment]: A list of Enrollment records that match the given criteria.
    """
```

Write Enrollment

```python
def write_enrollment(self, enrollment: dict):
    """
    Write an enrollment record to the enrollment CSV file.

    Parameters:
    - enrollment (dict): A dictionary representing an enrollment record.

    Raises:
    - ValueError: If the user is already enrolled.
    """
```

### Example Usage

```python
# Create a new db instance
db = database_class.Database()

# Read users from db
db.read_users()
```

## User Class

The **`User`** class represents a generic user in the educational management system. This class serves as the base class for more specialized user types, namely Admin and Student. Each instance of the User class encapsulates essential information about a user, including a unique identifier, name, username, hashed password, role (such as admin or student), the creator (admin who created the user), and timestamps indicating when the user was created and last updated.

### Initialization

```python
class User:
    def __init__(self, id: str, name: str, username: str, password: str, role: str, creator: str, created_at: str, updated_at: str):
    """
    Initialize a User object.

    Parameters:
    - id (str): The unique identifier for the user.
    - name (str): The name of the user.
    - username (str): The username of the user.
    - password (str): The hashed password of the user.
    - role (str): The role of the user (e.g., admin, student).
    - creator (str): The name of admin that created the record
    - created_at (str): The timestamp indicating when the user was created.
    - updated_at (str): The timestamp indicating when the user was last updated.
    """
```

- **`id`** (str): The unique identifier for the user.
- **`name`** (str): The name of the user.
- **`username`** (str): The username of the user.
- **`password`** (str): The hashed password of the user.
- **`role`** (str): The role of the user (e.g., admin, student).
- **`creator`** (str): The name of the admin that created the record.
- **`created_at`** (str): The timestamp indicating when the user was created.
- **`updated_at`** (str): The timestamp indicating when the user was last updated.

### Methods

**`__str__`**

```python
def __str__(self):
    """
    Return a string representation of the User.

    Returns:
    - str: A string representing the User object.
    """
```

To Admin Or Student

```python
def to_admin_or_student(self):
    """
    Convert the User object to either an Admin or Student based on the role.

    Returns:
    - Admin | Student: An instance of either Admin or Student based on the role.

    Raises:
    - ValueError: If role is invalid.
    """
```

## Admin Class

The **`Admin`** class represents an administrator in the Mini Canvas application. Administrators have the authority to manage users, courses, and enrollments within the system. They can perform various actions such as creating new users (both administrators and students), courses, and enrollments. Admins also have the ability to retrieve information about all users, courses, and enrollments in the system, as well as filter enrollments based on specific criteria.

### Initialization

```python
def __init__(self, id: str, name: str, username: str, password: str, role: str, creator: str, created_at: str, updated_at: str):
    """
    Initialize an Admin object.
    """
```

### Methods

Get All Users

```python
def get_all_users(self, db: database_module.Database):
    """
    Get a list of all users.

    Parameters:
    - db (Database): The Database instance.

    Returns:
    - list[User]: A list of all users.
    """
```

Get All Courses

```python
def get_all_courses(self, db: database_module.Database):
    """
    Get a list of all courses.

    Parameters:
    - db (Database): The Database instance.

    Returns:
    - list[Course]: A list of all courses.
    """
```

Get All Enrollments

```python
def get_all_enrollments(self, db: database_module.Database):
    """
    Get a list of all enrollments.

    Parameters:
    - db (Database): The Database instance.

    Returns:
    - list[Enrollment]: A list of all enrollments.
    """
```

Get Enrollments By User

```python
def get_enrollments_by_user(self, db: database_module.Database, username: str):
    """
    Get a list of enrollments for a specific user.

    Parameters:
    - db (Database): The Database instance.
    - username (str): The username of the user.

    Returns:
    - list[Enrollment]: A list of enrollments for the specified user.
    """
```

Get Enrollments By user_id

```python
def get_enrollments_by_user_id(self, db: database_module.Database, user_id: str):
    """
    Get a list of enrollments for a specific user ID.

    Parameters:
    - db (Database): The Database instance.
    - user_id (str): The user ID of the user.

    Returns:
    - list[Enrollment]: A list of enrollments for the specified user ID.
    """
```

Get Enrollments By course_id

```python
def get_enrollments_by_course_id(self, db: database_module.Database, course_id: str):
    """
    Get a list of enrollments for a specific course ID.

    Parameters:
    - db (Database): The Database instance.
    - course_id (str): The course ID of the course.

    Returns:
    - list[Enrollment]: A list of enrollments for the specified course ID.
    """
```

Create User

```python
def create_user(self, db: database_module.Database, student_name: str, student_username: str, student_password: str, role: str):
    """
    Create a new user.

    Parameters:
    - db (Database): The Database instance.
    - student_name (str): The name of the new user.
    - student_username (str): The username of the new user.
    - student_password (str): The password of the new user.
    - role (str): The role of the user (student or admin)

    Returns:
    - User: User record.

    Raises:
    - ValueError: If role is invalid.
    """
```

Create Course

```python
def create_course(self, db: database_module.Database, course_name: str, course_description: str):
    """
    Create a new course.

    Parameters:
    - db (Database): The Database instance.
    - course_name (str): The name of the new course.
    - course_description (str): The description of the new course.

    Returns:
    - Course: Course record.
    """
```

Create Enrollment

```python
def create_enrollment(self, db: database_module.Database, username: str, course_id: str):
    """
    Create a new enrollment.

    Parameters:
    - db (Database): The Database instance.
    - username (str): The username the user.
    - course_id (str): The id of the  course.

    Returns:
    - Enrollment: Enrollment record.

    Raises:
    - ValueError: If user or course id is invalid.
    """
```

### Example Usage

```python
# Create a new admin
new_admin = Admin(id="123", name="Admin Name", username="admin123", password="hashed_password", role="admin", creator="super admin", created_at="2023-01-01 12:00:00", updated_at="2023-01-01 12:00:00")

# Output a string representation of the admin
print(new_admin)
```

## Student Class

The **`Student`** class represents a student in the Mini Canvas application. Students have the ability to access their enrolled courses and view information related to their academic progress. They can view the courses they are currently enrolled in using the get_enrolled_courses method.

### Initialization

```python
def __init__(self, id: str, name: str, username: str, password: str, role: str, creator: str, created_at: str, updated_at: str):
    """
    Initialize a Student object.
    """
```

### Methods

Get Enrolled Courses

```python
def get_enrolled_courses(self, db: database_module.Database):
    """
    Get a list of courses that the student is enrolled in.

    Parameters:
    - db (Database): The Database instance.

    Returns:
    - list[Course]: A list of courses that the student is enrolled in.
    """
```

### Example Usage

```python
# Create a new student
new_student = Student(id="456", name="Student Name", username="student123", password="hashed_password", role="student", creator="admin", created_at="2023-01-01 12:00:00", updated_at="2023-01-01 12:00:00")

# Output a string representation of the student
print(new_student)
```

## Course Class

The **`course.py`** file defines the **`Course`** class, representing the courses in the Mini Canvas application. Each course has unique properties such as an identifier, name, description, and timestamps indicating creation and last update.

### Initialization

```python
def __init__(self, id: str, name: str, description: str, creator: str, created_at: str, updated_at: str):
    """
    Initialize a Course object.

    Parameters:
    - id (str): The unique identifier for the course.
    - name (str): The name of the course.
    - description  (str): The description of the course.
    - creator (str): The name of admin that created the record.
    - created_at (str): The timestamp indicating when the course was created.
    - updated_at (str): The timestamp indicating when the course was last updated.
    """
```

### Methods

**`__str__`**

```python
def __str__(self):
    """
    Return a string representation of the Course.

    Returns:
    - str: A string representing the Course object.
    """
```

Get Enrolled Students

```python
def get_enrolled_students(self, db: database_module.Database):
    """
    Get a list of students enrolled to the course.

    Parameters:
    - db (Database): The Database instance.

    Returns:
    - list[Student]: A list of students enrolled to the course.
    """
```

### Example Usage

```python
# Create a new course
new_course = Course(id="123", name="Introduction to Programming", description="An introductory course on programming.", creator="admin", created_at="2023-01-01 12:00:00", updated_at="2023-01-01 12:00:00")

# Output a string representation of the course
print(new_course)
```

## Enrollment Class

The **`enrollment.py`** file defines the **`Enrollment`** class, representing the enrollments in the Mini Canvas application. Each enrollment has a unique identifier, user ID, username, course ID, course name, and timestamps indicating creation and last update.

### Initialization

```python
def __init__(self, id: str, user_id: str, username: str, course_id: str, course_name: str, creator: str, created_at: str, updated_at: str):
    """
    Initialize a Enrollment object.

    Parameters:
    - id (str): The unique identifier for the enrollment.
    - user_id (str): The id of enrolled user.
    - username  (str): The name of enrolled user.
    - course_id (str): The id of the course
    - course_title (str): The title of the course
    - creator (str): The name of admin that created the record.
    - created_at (str): The timestamp indicating when the enrollment was created.
    - updated_at (str): The timestamp indicating when the enrollment was last updated.
    """
```

### Methods

**`__str__`**

```python
def __str__(self):
    """
    Return a string representation of the enrollment.

    Returns:
    - str: A string representing the Enrollment object.
    """
```

### Example Usage

```python
# Create a new enrollment
new_enrollment = Enrollment(id="456", user_id="789", username="student123", course_id="123", course_name="Introduction to Programming", creator="admin", created_at="2023-01-01 12:00:00", updated_at="2023-01-01 12:00:00")

# Output a string representation of the enrollment
print(new_enrollment)
```

## Utilities Module

The **`utilities`** module provides a set of utility functions and actions essential for the proper functioning of the educational management system. These utilities encompass a range of functionalities, including user authentication, input validation, screen clearing for a better user interface, and the generation of unique identifiers and timestamps. Additionally, the module includes error handling for scenarios where maximum login attempts are exceeded.

### Functions and Actions

Reset Screen

```python
def reset_screen():
    """
    Clears the terminal screen for a clean display.
    """
```

Validate String Input

```python
def validate_string_input(input_string: str):
    """
    Validates string input.

    Parameters:
    - input_string (str): The input string to be validated.

    Returns:
    - bool: True if the input is a non-empty string, False otherwise.
    """
```

**Example Usage**

```python
input_value = "JohnDoe123"
if validate_string_input(input_value):
    print(f"Input '{input_value}' is a valid string.")
else:
    print(f"Input '{input_value}' is not a valid string.")
```

Validate Menu Input

```python
def validate_menu_input(input_value: str, min_value: int, max_value: int):
    """
    Validates menu input to ensure it is a number within a given range.

    Parameters:
    - input_value: The input value to be validated.
    - min_value: The minimum allowed value.
    - max_value: The maximum allowed value.

    Returns:
    - bool: True if the input is a number within the specified range, False otherwise.
    """
```

**Example Usage**

```python
input_value = "2"
min_value = 1
max_value = 3
if validate_menu_input(input_value, min_value, max_value):
    print(f"Input '{input_value}' is a valid menu option.")
else:
    print(f"Input '{input_value}' is not a valid menu option.")
```

Login Flow

```python
def login_flow(db: Database):
    """
    A login flow with a limited number of attempts.

    Parameters:
    - db (Database): The Database instance.

    Returns:
    - User: An instance of either Admin or Student based on the role.
    """
```

Get Unique Id

```python
def get_unique_id():
    """
    Generates a unique UUID.

    Returns:
    - str: A string representation of a unique UUID.
    """
```

**Example Usage**

```python
unique_id = get_unique_id()
print(f"Generated Unique ID: {unique_id}")
```

Get Current Date & Time

```python
def get_current_datetime():
    """
    Generates the current date and time in ISO 8601 format.

    Returns:
    - str: A string representation of the current date and time.
    """
```

Hash Password

```python
def hash_password(password: str):
    """
    Hashes a password using SHA-256.

    Parameters:
    - password (str): The password to be hashed.

    Returns:
    - str: The hashed password.
    """
```

**Example Usage**

```python
password = "securePassword123"
hashed_password = hash_password(password)
print(f"Password: {password}\nHashed Password: {hashed_password}")
```

Compare Password To Hash

```python
def compare_password_to_hash(password: str, hashed_password: str):
    """
    Compares a password to its hashed version.

    Parameters:
    - password (str): The password to be compared.
    - hashed_password (str): The hashed version of the password.

    Returns:
    - bool: True if the password matches the hashed version, False otherwise.
    """
```

**Example Usage**

```python
# Example Usage of compare_password_to_hash

# Suppose you have a user with a known password and hashed password stored in a database
known_password = "securePassword123"
stored_hashed_password = "2a5d9e24c0b2c97d2c63d8343e0eb743d240b42a4159d8f1a8f7b3ff6a3ba745"

# User input (e.g., entered password during login)
user_input_password = input("Enter your password: ")

# Compare the entered password with the stored hashed password
passwords_match = compare_password_to_hash(user_input_password, stored_hashed_password)

if passwords_match:
    print("Password is correct. Login successful!")
else:
    print("Incorrect password. Please try again.")
```

Display Table

```python
def display_table(entity_name: str, field_names: List[str], data: List[Dict]):
    """
    Displays a table containing information for a given entity.

    Parameters:
    - entity_name (str): The name of the entity.
    - field_names (List[str]): A list of field names for the table.
    - data (List[Dict]): A list of dictionaries representing the entity data.

    Each dictionary in the data list should have keys corresponding to the field names.
    """
```

View All Users

```python
def view_all_users(db: Database, admin: Admin):
    """
    Admin action, Shows a table of all users.

    Parameters:
    - db (Database): The Database instance.
    - admin (Admin): Admin user performing action.
    """
```

View All Courses

```python
def view_all_courses(db: Database, admin: Admin):
    """
    Admin action, Shows a table of all courses.

    Parameters:
    - db (Database): The Database instance.
    - admin (Admin): Admin user performing action.
    """
```

View All Enrollments

```python
def view_all_enrollments(db: Database, admin: Admin):
    """
    Admin action, Shows a table of all courses.

    Parameters:
    - db (Database): The Database instance.
    - admin (Admin): Admin user performing action.
    """
```

View Student's Courses

```python
def view_all_student_courses(db: Database):
    """
    Admin action, Shows a table of a student's enrolled courses.

    Parameters:
    - db (Database): The Database instance.
    """
```

View Course's Students

```python
def view_all_course_students(db: Database):
    """
    Admin action, Shows a table of a course's enrolled students.

    Parameters:
    - db (Database): The Database instance.
    """
```

Create New User

```python
def create_new_user(db: Database, admin: Admin, role: str):
    """
    Admin action, Creates a new Student or Admin based to given role.

    Parameters:
    - db (Database): The Database instance.
    - admin (Admin): Admin user performing action.
    - role (str): Type of user to create (student or admin)
    """
```

Create New Course

```python
def create_new_course(db: Database, admin: Admin):
    """
    Admin action, Creates a new course.

    Parameters:
    - db (Database): The Database instance.
    - admin (Admin): Admin user performing action.
    """
```

Enroll Student To Course

```python
def enroll_user_to_course(db: Database, admin: Admin):
    """
    Admin action, Enrolls student to course.

    Parameters:
    - db (Database): The Database instance.
    - admin (Admin): Admin user performing action.
    """
```

View My Courses

```python
def view_my_courses(db: Database, student: Student):
    """
    Student action, Shows a table of all enrolled courses.

    Parameters:
    - db (Database): The Database instance.
    - student (Student): Student user performing action.
    """
```

Quit Program

```python
def quit_program(message: str):
    """
    Admin and Student action, Exits the program.

    Parameters:
    - message (str): sys exit message.
    """
```
