import classes.user as user_class
import classes.database as database_class
from utils.utilities import MaxAttemptsExceededError, create_new_course, create_new_user,  enroll_user_to_course, login_flow, quit_program, validate_menu_input, reset_screen, view_all_course_students, view_all_courses, view_all_enrollments, view_all_student_courses, view_all_users, view_my_courses

db = database_class.Database()


def main():
    reset_screen()

    CURRENT_USER: user_class.Admin | user_class.Student | None = None

    try:

        while not CURRENT_USER:
            try:
                CURRENT_USER = login_flow(db)

            except MaxAttemptsExceededError as e:
                quit_program(f"{e}")

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
                    print("\nInvalid option. Please try again.")
                    continue

                # View all users
                if choice == "1":
                    view_all_users(db, CURRENT_USER)

                # View all courses
                if choice == "2":
                    view_all_courses(db, CURRENT_USER)

                # View all enrollments
                if choice == "3":
                    view_all_enrollments(db, CURRENT_USER)

                # View student courses
                if choice == "4":
                    view_all_student_courses(db)

                # View course student
                if choice == "5":
                    view_all_course_students(db)

                # Create a new student
                if choice == "6":
                    create_new_user(db, CURRENT_USER, "student")
                # Create a new admin
                if choice == "7":
                    create_new_user(db, CURRENT_USER, "admin")

                # Create a new course
                if choice == "8":
                    create_new_course(db, CURRENT_USER)

                # Enroll a user to a course
                if choice == "9":
                    enroll_user_to_course(db, CURRENT_USER)

                # Exit
                if choice == "10":
                    quit_program("Good bye.")

        if isinstance(CURRENT_USER, user_class.Student):
            """
            Student flow with various actions.
            """
            while True:
                print(f"\nHi {CURRENT_USER.name}, Menu:")
                print("1. View my courses")
                print("2. Exit")

                choice = input("Enter your choice (1-1): ")

                if not validate_menu_input(choice, 1, 2):
                    print("\nInvalid option. Please try again.")
                    continue

                # View my courses
                if choice == "1":
                    view_my_courses(db, CURRENT_USER)

                # Exit
                if choice == "2":
                    quit_program("Good bye.")

    except KeyboardInterrupt:
        print("\nExited by user.")


if __name__ == "__main__":
    main()
