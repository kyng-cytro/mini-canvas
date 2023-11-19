class Enrollment:
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
        self.id = id
        self.user_id = user_id
        self.username = username
        self.course_id = course_id
        self.course_name = course_name
        self.creator = creator
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        """
        Return a string representation of the enrollment.

        Returns:
        - str: A string representing the Enrollment object.
        """
        return f"Id {self.id} (Username: {self.username}, Course Name: {self.course_name})"
