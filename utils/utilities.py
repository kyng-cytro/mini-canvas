import os
import sys
import uuid
import hashlib
from getpass import getpass
from datetime import datetime
import classes.user as user_class
import classes.course as course_class
from prettytable import PrettyTable


MAX_ATTEMPTS = 5


class MaxAttemptsExceededError(Exception):
    """Exception raised when the maximum login attempts are exceeded."""
    pass


def reset_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(
        """
   ▄▄   ▄▄ ▄▄▄ ▄▄    ▄ ▄▄▄    ▄▄▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄    ▄ ▄▄   ▄▄ ▄▄▄▄▄▄ ▄▄▄▄▄▄▄
  █  █▄█  █   █  █  █ █   █  █       █      █  █  █ █  █ █  █      █       █
  █       █   █   █▄█ █   █  █       █  ▄   █   █▄█ █  █▄█  █  ▄   █  ▄▄▄▄▄█
  █       █   █       █   █  █     ▄▄█ █▄█  █       █       █ █▄█  █ █▄▄▄▄▄
  █       █   █  ▄    █   █  █    █  █      █  ▄    █       █      █▄▄▄▄▄  █
  █ ██▄██ █   █ █ █   █   █  █    █▄▄█  ▄   █ █ █   ██     ██  ▄   █▄▄▄▄▄█ █
  █▄█   █▄█▄▄▄█▄█  █▄▄█▄▄▄█  █▄▄▄▄▄▄▄█▄█ █▄▄█▄█  █▄▄█ █▄▄▄█ █▄█ █▄▄█▄▄▄▄▄▄▄█
  
                                                            by Tolulope Bello
""")


def validate_string_input(input_string: str):
    """
    Validates string input.

    Parameters:
    - input_string (str): The input string to be validated.

    Returns:
    - bool: True if the input is a non-empty string, False otherwise.
    """
    return isinstance(input_string, str) and len(input_string) > 0


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
    try:
        input_number = int(input_value)
        return min_value <= input_number <= max_value

    except ValueError:
        return False


def login_flow(db):
    """
    A login flow with a limited number of attempts.

    Parameters:
    - db (Database): The Database instance.

    Returns:
    - User: An instance of either Admin or Student based on the role.
    """
    attempts = 0

    while attempts < MAX_ATTEMPTS:
        username = input("Enter your username: ")
        password = getpass(prompt="Enter your password: ")

        attempts += 1

        if not validate_string_input(username) or not validate_string_input(password):
            print("username and password can not be empty.")
            continue

        user = db.read_user(username=username)

        if not user:
            print("Invalid username or password")
            continue

        if not compare_password_to_hash(password, user.password):
            print("Invalid username or password")
            continue

        return user.to_admin_or_student()

    raise MaxAttemptsExceededError(
        "Exceeded maximum login attempts. Try again later.")


def get_unique_id():
    """
    Generate a unique UUID.

    Returns:
    - str: A string representation of a unique UUID.
    """
    return str(uuid.uuid4())


def get_current_datetime():
    """
    Generate the current date and time in ISO 8601 format.

    Returns:
    - str: A string representation of the current date and time.
    """
    current_datetime = datetime.now()
    return current_datetime.isoformat()


def hash_password(password: str):
    """
    Hash a password using SHA-256.

    Parameters:
    - password (str): The password to be hashed.

    Returns:
    - str: The hashed password.
    """
    # Convert the password to bytes before hashing
    password_bytes = password.encode('utf-8')

    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()

    # Update the hash object with the password bytes
    sha256_hash.update(password_bytes)

    # Get the hexadecimal representation of the hash
    hashed_password = sha256_hash.hexdigest()

    return hashed_password


def compare_password_to_hash(password: str, hashed_password: str):
    """
    Compare a password to its hashed version.

    Parameters:
    - password (str): The password to be compared.
    - hashed_password (str): The hashed version of the password.

    Returns:
    - bool: True if the password matches the hashed version, False otherwise.
    """
    # Hash the provided password
    hashed_input_password = hash_password(password)

    # Compare the hashed input password to the stored hashed password
    return hashed_input_password == hashed_password


def display_table(entity_name: str, field_names: list[str], data: list[dict]):
    """
    Displays a table containing information for a given entity.

    Parameters:
    - entity_name (str): The name of the entity.
    - field_names (list[str]): A list of field names for the table.
    - data (list[dict]): A list of dictionaries representing the entity data.

    Each dictionary in the data list should have keys corresponding to the field names.
    """
    table = PrettyTable()
    table.field_names = ["S/N", *[name.title() for name in field_names]]

    for index, item in enumerate(data):
        table.add_row([index + 1, *[item[field.lower()]
                      for field in field_names]])

    header = f"{entity_name} Information Table"
    separator = "=" * len(header)

    print()
    print(header)
    print(separator)
    print(table)


def view_all_users(db, admin):
    """
    Admin action, Shows a table of all users.

    Parameters:
    - db (Database): The Database instance.
    - admin (Admin): Admin user performing action.
    """
    reset_screen()
    try:
        users = admin.get_all_users(db)
        display_table(
            "User", ["id", "username", "name", "role", "creator", "created_at"], [user.__dict__ for user in users])

    except KeyError:
        print(
            "\nEach dictionary in the data list should have keys corresponding to the field names.")

    except Exception as e:
        print(f"\nAn unkowned error occured {e}.")


def view_all_courses(db, admin):
    """
    Admin action, Shows a table of all courses.

    Parameters:
    - db (Database): The Database instance.
    - admin (Admin): Admin user performing action.
    """
    reset_screen()
    try:
        courses = admin.get_all_courses(db)
        display_table(
            "Course", ["id", "name", "description", "creator", "created_at"], [course.__dict__ for course in courses])

    except KeyError:
        print(
            "\nEach dictionary in the data list should have keys corresponding to the field names.")

    except Exception as e:
        print(f"\nAn unkowned error occured {e}.")


def view_all_enrollments(db, admin):
    """
    Admin action, Shows a table of all courses.

    Parameters:
    - db (Database): The Database instance.
    - admin (Admin): Admin user performing action.
    """
    reset_screen()
    try:
        enrollments = admin.get_all_enrollments(db)
        display_table(
            "Enrollment", ["id", "user_id", "username", "course_id", "course_name", "creator", "created_at"], [enrollment.__dict__ for enrollment in enrollments])

    except KeyError:
        print(
            "\nEach dictionary in the data list should have keys corresponding to the field names.")

    except Exception as e:
        print(f"\nAn unkowned error occured {e}.")


def view_all_student_courses(db):
    """
    Admin action, Shows a table of a student's enrolled courses.

    Parameters:
    - db (Database): The Database instance.
    """
    reset_screen()
    try:
        value = input("Enter username or id: ")

        if not validate_string_input(value):
            print("\nInvalid username or id.")
            return

        student = db.read_user(id=value, username=value)

        if isinstance(student, user_class.Student):
            courses = student.get_enrolled_courses(db)
            display_table(f"{student.name}'s Course", ["id", "name", "description", "creator", "created_at"], [
                course.__dict__ for course in courses])
            return

        print("\nDidn't find a student with that username or id.")

    except KeyError:
        print(
            "\nEach dictionary in the data list should have keys corresponding to the field names.")

    except Exception as e:
        print(f"\nAn unkowned error occured {e}.")


def view_all_course_students(db):
    """
    Admin action, Shows a table of a course's enrolled students.

    Parameters:
    - db (Database): The Database instance.
    """
    reset_screen()
    try:
        value = input("Enter course id: ")

        if not validate_string_input(value):
            print("\nCourse id can not be empty.")
            return

        course = db.read_course(id=value)

        if isinstance(course, course_class.Course):
            users = course.get_enrolled_students(db)
            display_table(f"{course.name}'s Student", ["id", "username", "name", "role", "creator", "created_at"], [
                user.__dict__ for user in users])
            return

        print("\nDidn't find a course with that id.")

    except KeyError:
        print(
            "\nEach dictionary in the data list should have keys corresponding to the field names.")

    except Exception as e:
        print(f"\nAn unkowned error occured {e}.")


def create_new_user(db, admin, role: str):
    """
    Admin action, Creates a new Student or Admin based to given role.

    Parameters:
    - db (Database): The Database instance.
    - admin (Admin): Admin user performing action.
    - role (str): Type of user to create (student or admin)
    """
    reset_screen()
    try:
        username = input(f"Enter {role}'s username: ")
        full_name = input(f"Enter {role}'s full name: ")
        password = input(f"Enter {role}'s password: ")

        if not validate_string_input(username):
            print("\nUsername can not be empty.")
            return

        if not validate_string_input(full_name):
            print("\nFull name can not be empty.")
            return

        if not validate_string_input(password):
            print("\nPassword can not be empty.")
            return

        student = admin.create_user(
            db, full_name, username, password, role)

        print(f"\n{role.title()} Created Successfully {student}.")

    except ValueError as e:
        print(f"\n{e}")

    except Exception as e:
        print(f"\nAn unkowned error occured {e}.")


def create_new_course(db, admin):
    """
    Admin action, Creates a new course.

    Parameters:
    - db (Database): The Database instance.
    - admin (Admin): Admin user performing action.
    """
    reset_screen()
    try:
        course_name = input("Enter the course name: ")
        course_description = input(
            "Enter the course description: ")

        if not validate_string_input(course_name):
            print("\nCourse name can not be empty.")
            return

        if not validate_string_input(course_description):
            print("\nCourse description can not be empty.")
            return

        course = admin.create_course(
            db, course_name, course_description)

        print(f"\nCourse Created Successfully {course}.")

    except Exception as e:
        print(f"\nAn unkowned error occured {e}")


def enroll_user_to_course(db, admin):
    """
    Admin action, Enrolls student to course.

    Parameters:
    - db (Database): The Database instance.
    - admin (Admin): Admin user performing action.
    """
    reset_screen()
    try:
        username = input("Enter username of user to enroll: ")
        course_id = input(
            "Enter course id of course to enroll to: ")

        if not validate_string_input(username):
            print("\nUsername can not be empty")
            return

        if not validate_string_input(course_id):
            print("\nFull name can not be empty")
            return

        enrollment = admin.create_enrollment(
            db,  username, course_id)

        print(
            f"\nEnrollment Created Successfully {enrollment}.")

    except ValueError as e:
        print(f"\n{e}")

    except Exception as e:
        print(f"\nAn unkowned error occured {e}.")


def view_my_courses(db, student):
    """
    Student action, Shows a table of all enrolled courses.

    Parameters:
    - db (Database): The Database instance.
    - student (Student): Student user performing action.
    """
    reset_screen()
    try:
        courses = student.get_enrolled_courses(db)
        display_table(
            "My Courses", ["id", "name", "description", "creator", "created_at"], [course.__dict__ for course in courses])

    except KeyError:
        print(
            "\nEach dictionary in the data list should have keys corresponding to the field names.")

    except Exception as e:
        print(f"\nAn unkowned error occured {e}.")


def quit_program(message: str):
    """
    Admin and Student action, Exits the program.

    Parameters:
    - message (str): sys exit message.

    """
    sys.exit(message)
