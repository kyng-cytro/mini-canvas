import os
import csv
import classes.course as course_class
import classes.enrollment as enrollment_class
import classes.user as user_class
from utils.utilities import get_current_datetime, get_unique_id, hash_password


class Database:
    def __init__(self, folder_path='data'):
        """
        Initialize the Database object with file paths for users, courses, and enrollments.

        Parameters:
        - folder_path (str): Folder path to store all csv files
        """
        self.folder_path = folder_path
        self.users_file = os.path.join(folder_path, 'users.csv')
        self.courses_file = os.path.join(folder_path, "courses.csv")
        self.enrollments_file = os.path.join(folder_path, "enrollments.csv")
        self.defualt_field_names = ['creator', 'created_at', 'updated_at']
        self.users_field_names = ['id', 'name', 'username',
                                  'password', 'role', *self.defualt_field_names]
        self.courses_field_names = ['id', 'name', 'description',
                                    *self.defualt_field_names]
        self.enrollments_field_names = ['id', 'user_id', 'username', 'course_id', 'course_name',
                                        *self.defualt_field_names]

        self._check_and_create_files()

    def _check_folder_path(self):
        # Create the folder if it doesn't exist
        os.makedirs(self.folder_path, exist_ok=True)

    def _check_and_create_files(self):
        """
        Check if the CSV files exist, and create them if they don't.
        """
        file_paths = [self.users_file,
                      self.courses_file, self.enrollments_file]

        self._check_folder_path()

        for file_path in file_paths:
            if not os.path.exists(file_path):
                self._create_file_with_header(file_path)

    def _create_file_with_header(self, file_path: str):
        """
        Create a CSV file with the appropriate header.

        Parameters:
        - file_path (str): The path of the CSV file to be created.
        """
        field_names = []

        if "users" in file_path:
            field_names = self.users_field_names

        elif 'courses' in file_path:
            field_names = self.courses_field_names

        elif 'enrollments' in file_path:
            field_names = self.enrollments_field_names

        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            if "users" in file_path:
                self._create_super_admin()

    def _create_super_admin(self):
        """
        Create a super admin with defualt info
        """
        id = get_unique_id()
        now = get_current_datetime()
        # NOTE: Hard coded password
        hashed_password = hash_password("admin")

        data = {"id": id, "name": "super admin", "username": "admin",
                "password": hashed_password, 'role': 'admin', "creator": "system", "created_at": now, "updated_at": now}

        with open(self.users_file, 'a', newline='') as file:
            writer = csv.DictWriter(
                file, fieldnames=self.users_field_names)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)

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
        if record_type not in ['user', 'course', 'enrollment']:
            raise ValueError(
                "Invalid record type. Allowed types: user, course, enrollment")

        file_name = None
        if record_type == 'user':
            file_name = self.users_file
        elif record_type == 'course':
            file_name = self.courses_file
        elif record_type == 'enrollment':
            file_name = self.enrollments_file

        if not file_name:
            raise ValueError(f"Invalid record type '{record_type}'")

        with open(file_name, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row[field] == value:
                    return False

        return True

    def is_enrollment_unique(self, user_id, course_id):
        """
        Check if an enrollment with the given user_id and course_id is unique.

        Parameters:
        - user_id (str): The user ID to check for uniqueness.
        - course_id (str): The course ID to check for uniqueness.

        Returns:
        - bool: True if the enrollment is unique, False otherwise.
        """
        with open(self.enrollments_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['user_id'] == user_id and row['course_id'] == course_id:
                    return False

        return True

    def read_users(self):
        """
        Read user records from the users CSV file.

        Returns:
        - list[User]: A list of either Admin or Student based on the role.
          """
        users: list[user_class.Admin | user_class.Student] = []

        with open(self.users_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = user_class.User(**row)
                users.append(user.to_admin_or_student())

        return users

    def read_user(self, id="", username=""):
        """
        Read a user record from the users CSV file based on id or username.

        Parameters:
        - id (str): Optional. The user ID to filter by.
        - username (str): Optional. The username to filter by.

        Returns:
        - Admin, Student or None: Admin or Student record if a match is found, None otherwise.
        """
        if (not id and not username):
            return None

        with open(self.users_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id'] == id or row['username'] == username:
                    return user_class.User(**row).to_admin_or_student()

    def write_user(self, user: dict):
        """
        Write a user record to the users CSV file.

        Parameters:
        - user (dict): A dictionary representing a user record.

        Raises:
        - ValueError: If username is not unique.
        """
        if (not self.is_field_unique('user', 'username', user['username'])):
            raise ValueError("username must be unique")

        with open(self.users_file, 'a', newline='') as file:
            writer = csv.DictWriter(
                file, fieldnames=self.users_field_names)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(user)

    def read_courses(self):
        """
        Read course records from the courses CSV file.

        Returns:
        - list[Course]: A list of courses.
          """
        courses: list[course_class.Course] = []

        with open(self.courses_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                course = course_class.Course(**row)
                courses.append(course)

        return courses

    def read_course(self, id: str):
        """
        Read a course record from the users CSV file based on id.

        Parameters:
        - id (str): The course ID to filter by.

        Returns:
        - Course or None: Course record if a match is found, None otherwise.
        """

        with open(self.courses_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if (row['id'] == id):
                    return course_class.Course(**row)

    def write_course(self, course: dict):
        """
        Write a course record to the users CSV file.

        Parameters:
        - course (dict): A dictionary representing a course record.
        """
        with open(self.courses_file, 'a', newline='') as file:
            writer = csv.DictWriter(
                file, fieldnames=self.courses_field_names)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(course)

    def read_enrollments(self):
        """
        Read enrollment records from the courses CSV file.

        Returns:
        - list[Enrollment]: A list of enrollments.
          """
        enrollments: list[enrollment_class.Enrollment] = []

        with open(self.enrollments_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                enrollment = enrollment_class.Enrollment(**row)
                enrollments.append(enrollment)

        return enrollments

    def read_enrollment(self, id: str):
        """
        Read a enrollment record from the users CSV file based on id.

        Parameters:
        - id (str): The enrollment ID to filter by.

        Returns:
        - Enrollment or None: Enrollment record if a match is found, None otherwise.
        """
        with open(self.enrollments_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if (row['id'] == id):
                    return enrollment_class.Enrollment(**row)

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
        enrollments: list[enrollment_class.Enrollment] = []

        with open(self.enrollments_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['user_id'] == user_id or row['username'] == username or row['course_id'] == course_id:
                    enrollment = enrollment_class.Enrollment(**row)
                    enrollments.append(enrollment)

        return enrollments

    def write_enrollment(self, enrollment: dict):
        """
        Write a enrollment record to the enrollment CSV file.

        Parameters:
        - enrollment (dict): A dictionary representing a enrollment record.

        Raises:
        - ValueError: If user is already enrolled.
        """
        if (not self.is_enrollment_unique(enrollment['user_id'], enrollment['course_id'])):
            raise ValueError("user is already enrolled to that course.")

        with open(self.enrollments_file, 'a', newline='') as file:
            writer = csv.DictWriter(
                file, fieldnames=self.enrollments_field_names)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(enrollment)
