import classes.course as course_module
import classes.database as database_module
import classes.enrollment as enrollment_module
from utils.utilities import get_current_datetime, get_unique_id, hash_password


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
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.role = role
        self.creator = creator
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        """
        Return a string representation of the User.

        Returns:
        - str: A string representing the User object.
        """
        return f"Id {self.id} (Name: {self.name}, Username: {self.username})"

    def to_admin_or_student(self):
        """
        Convert the User object to either an Admin or Student based on the role.

        Returns:
        - User: An instance of either Admin or Student based on the role.

        Raises:
        - ValueError: If role is invalid.
        """
        if self.role not in ['student', 'admin']:
            raise ValueError(
                "Invalid role. Allowed roles: student, admin")

        if self.role == "admin":
            return Admin(**self.__dict__)

        return Student(**self.__dict__)


class Admin(User):
    def __init__(self, id: str, name: str, username: str, password: str, role: str, creator: str, created_at: str, updated_at: str):
        """
        Initialize an Admin object.
        """
        super().__init__(id, name, username, password,
                         role, creator, created_at, updated_at)

    def get_all_users(self, db: database_module.Database):
        """
        Get a list of all users.

        Parameters:
        - db (Database): The Database instance.

        Returns:
        - list[User]: A list of all users.
        """
        return db.read_users()

    def get_all_courses(self, db: database_module.Database):
        """
        Get a list of all courses.

        Parameters:
        - db (Database): The Database instance.

        Returns:
        - list[Course]: A list of all courses.
        """
        return db.read_courses()

    def get_all_enrollments(self, db: database_module.Database):
        """
        Get a list of all enrollments.

        Parameters:
        - db (Database): The Database instance.

        Returns:
        - list[Enrollment]: A list of all enrollments.
        """
        return db.read_enrollments()

    def get_enrollments_by_user(self, db: database_module.Database, username: str):
        """
        Get a list of enrollments for a specific user.

        Parameters:
        - db (Database): The Database instance.
        - username (str): The username of the user.

        Returns:
        - list[Enrollment]: A list of enrollments for the specified user.
        """
        return db.query_enrollments(username=username)

    def get_enrollments_by_user_id(self, db: database_module.Database, user_id: str):
        """
        Get a list of enrollments for a specific user ID.

        Parameters:
        - db (Database): The Database instance.
        - user_id (str): The user ID of the user.

        Returns:
        - list[Enrollment]: A list of enrollments for the specified user ID.
        """
        return db.query_enrollments(user_id=user_id)

    def get_enrollments_by_course_id(self, db: database_module.Database, course_id: str):
        """
        Get a list of enrollments for a specific course ID.

        Parameters:
        - db (Database): The Database instance.
        - course_id (str): The course ID of the course.

        Returns:
        - list[Enrollment]: A list of enrollments for the specified course ID.
        """
        return db.query_enrollments(course_id=course_id)

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
        if role not in ['student', 'admin']:
            raise ValueError(
                "Invalid role. Allowed roles: student, admin")

        id = get_unique_id()
        now = get_current_datetime()
        hashed_password = hash_password(student_password)

        user = User(id, student_name, student_username,
                    hashed_password, role, self.name, now, now)

        db.write_user(user.__dict__)

        return user

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
        id = get_unique_id()
        now = get_current_datetime()

        course = course_module.Course(id, course_name, course_description,
                                      self.name, now, now)

        db.write_course(course.__dict__)

        return course

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

        user = db.read_user(username=username)

        if not isinstance(user, Student):
            raise ValueError(
                "Invalid user_id. No student with that id was found in the database.")

        course = db.read_course(course_id)

        if not isinstance(course, course_module.Course):
            raise ValueError(
                "Invalid course_id. No course with that id was found in the database.")

        id = get_unique_id()
        now = get_current_datetime()

        enrollment = enrollment_module.Enrollment(
            id, user.id, user.username, course.id, course.name, self.name, now, now)

        db.write_enrollment(enrollment.__dict__)

        return enrollment


class Student(User):
    def __init__(self, id: str, name: str, username: str, password: str, role: str, creator: str, created_at: str, updated_at: str):
        """
        Initialize a Student object.
        """
        super().__init__(id, name, username, password,
                         role, creator, created_at, updated_at)

    def get_enrolled_courses(self, db: database_module.Database):
        """
        Get a list of courses that the student is enrolled in.

        Parameters:
        - db (Database): The Database instance.

        Returns:
        - list[Course]: A list of courses that the student is enrolled in.
        """
        enrollments = db.query_enrollments(user_id=self.id)

        courses = []
        for enrollment in enrollments:
            course = db.read_course(id=enrollment.course_id)
            if course:
                courses.append(course)

        return courses
