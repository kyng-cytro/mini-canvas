import sys
import classes.user as user_class
import classes.course as course_class
import classes.database as database_class
from utils.utilities import MaxAttemptsExceededError, display_table, login_flow, validate_menu_input, reset_screen, validate_string_input

db = database_class.Database()


def main():
    reset_screen()

    CURRENT_USER: user_class.Admin | user_class.Student | None = None

    try:

        while not CURRENT_USER:
            try:
                CURRENT_USER = login_flow(db)

            except MaxAttemptsExceededError as e:
                sys.exit(f"{e}")

            except Exception as e:
                print(f"\nAn unkowned error occured {e}")

        if isinstance(CURRENT_USER, user_class.Admin):
            """
            Admin flow with various actions.
            """
            while True:
                print(f"\nHi {CURRENT_USER.name}, Menu:")
                print("1. View all users")
                print("2. View all courses")
                print("3. View all enrollments")
                print("4. View student courses")
                print("5. View course student")
                print("6. Create a new student")
                print("7. Create a new admin")
                print("8. Create a new course")
                print("9. Enroll a user to a course")
                print("10. Exit")

                choice = input("Enter your choice (1-10): ")

                if not validate_menu_input(choice, 1, 10):
                    print("Invalid option. Please try again.")
                    continue

                # View all users
                if choice == "1":
                    reset_screen()
                    try:
                        users = CURRENT_USER.get_all_users(db)
                        display_table(
                            "User", ["id", "username", "name", "role", "creator", "created_at"], [user.__dict__ for user in users])

                    except KeyError:
                        print(
                            "\nEach dictionary in the data list should have keys corresponding to the field names.")

                    except Exception as e:
                        print(f"\nAn unkowned error occured {e}")

                # View all courses
                if choice == "2":
                    reset_screen()
                    try:
                        courses = CURRENT_USER.get_all_courses(db)
                        display_table(
                            "Course", ["id", "name", "description", "creator", "created_at"], [course.__dict__ for course in courses])

                    except KeyError:
                        print(
                            "\nEach dictionary in the data list should have keys corresponding to the field names.")

                    except Exception as e:
                        print(f"\nAn unkowned error occured {e}")

                # View all enrollment
                if choice == "3":
                    reset_screen()
                    try:
                        enrollments = CURRENT_USER.get_all_enrollments(db)
                        display_table(
                            "Enrollment", ["id", "user_id", "username", "course_id", "course_name", "creator", "created_at"], [enrollment.__dict__ for enrollment in enrollments])

                    except KeyError:
                        print(
                            "\nEach dictionary in the data list should have keys corresponding to the field names.")

                    except Exception as e:
                        print(f"\nAn unkowned error occured {e}")

                # View student courses
                if choice == "4":
                    reset_screen()
                    try:
                        value = input("Enter username or id: ")

                        if not validate_string_input(value):
                            print("\nInvalid username or id")
                            continue

                        student = db.read_user(id=value, username=value)

                        if isinstance(student, user_class.Student):
                            courses = student.get_enrolled_courses(db)
                            display_table(f"{student.name}'s Course", ["id", "name", "description", "creator", "created_at"], [
                                          course.__dict__ for course in courses])
                            continue

                        print("\nDidn't find a student with that username or id")

                    except KeyError:
                        print(
                            "\nEach dictionary in the data list should have keys corresponding to the field names.")

                    except Exception as e:
                        print(f"\nAn unkowned error occured {e}")

                # View course student
                if choice == "5":
                    reset_screen()
                    try:
                        value = input("Enter course id: ")

                        if not validate_string_input(value):
                            print("\nCourse id can not be empty")
                            continue

                        course = db.read_course(id=value)

                        if isinstance(course, course_class.Course):
                            users = course.get_enrolled_students(db)
                            display_table(f"{course.name}'s Student", ["id", "username", "name", "role", "creator", "created_at"], [
                                          user.__dict__ for user in users])
                            continue

                        print("\nDidn't find a course with that id")

                    except KeyError:
                        print(
                            "\nEach dictionary in the data list should have keys corresponding to the field names.")

                    except Exception as e:
                        print(f"\nAn unkowned error occured {e}")

                # Create a new student
                if choice == "6":
                    reset_screen()
                    try:
                        username = input("Enter student's username: ")
                        full_name = input("Enter student's full name: ")
                        password = input("Enter student's password: ")

                        if not validate_string_input(username):
                            print("\nUsername can not be empty")
                            continue

                        if not validate_string_input(full_name):
                            print("\nFull name can not be empty")
                            continue

                        if not validate_string_input(password):
                            print("\nPassword can not be empty")
                            continue

                        student = CURRENT_USER.create_user(
                            db, full_name, username, password, "student")

                        print(f"\nStudent Created Successfully {student}")

                    except ValueError as e:
                        print(f"\n{e}")

                    except Exception as e:
                        print(f"\nAn unkowned error occured {e}")

                # Create a new admin
                if choice == "7":
                    reset_screen()
                    try:
                        username = input("Enter admin's username: ")
                        full_name = input("Enter admin's full name: ")
                        password = input("Enter admin's password: ")

                        if not validate_string_input(username):
                            print("\nUsername can not be empty")
                            continue

                        if not validate_string_input(full_name):
                            print("\nFull name can not be empty")
                            continue

                        if not validate_string_input(password):
                            print("\nPassword can not be empty")
                            continue

                        admin = CURRENT_USER.create_user(
                            db, full_name, username, password, "admin")

                        print(f"\nAdmin Created Successfully {admin}")

                    except ValueError as e:
                        print(f"\n{e}")

                    except Exception as e:
                        print(f"\nAn unkowned error occured {e}")

                # Create a new course
                if choice == "8":
                    reset_screen()
                    try:
                        course_name = input("Enter the course name: ")
                        course_description = input(
                            "Enter the course description: ")

                        if not validate_string_input(course_name):
                            print("\nUsername can not be empty")
                            continue

                        if not validate_string_input(course_description):
                            print("\nFull name can not be empty")
                            continue

                        course = CURRENT_USER.create_course(
                            db, course_name, course_description)

                        print(f"\nCourse Created Successfully {course}")

                    except ValueError as e:
                        print(f"\n{e}")

                    except Exception as e:
                        print(f"\nAn unkowned error occured {e}")

        if isinstance(CURRENT_USER, user_class.Student):
            """
            Student flow with various actions.
            """
            while True:
                print(f"\nHi {CURRENT_USER.name}, Menu:")
                break

    except KeyboardInterrupt:
        print("\nExited by user")


if __name__ == "__main__":
    main()
