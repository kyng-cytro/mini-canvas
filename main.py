import classes.course as course_class
import classes.user as user_class
import classes.database as database_class

db = database_class.Database()

users = db.read_users()
print(users)

print()

courses = db.read_courses()
print(courses)

print()

admin = db.read_user("d7b96250-a320-4213-a768-269609ea81a5")

print(admin)

course = db.read_course("c2ab7fe0-96c2-4263-8de5-788fb7f4aef8")

print(course)

if isinstance(admin, user_class.Admin):
    try:
        admin.create_user(db, "John Doe", "Cytro", "test", 'student')
        admin.create_course(db, "Python II", "test def")

    except Exception as e:
        print(e)

if isinstance(admin, user_class.Admin) and isinstance(course, course_class.Course):
    try:
        # enroll = admin.create_enrollment(db, users[1].id, course.id)
        # print(enroll)
        print(users[1].get_enrolled_courses(db))
    except Exception as e:
        print(e)
