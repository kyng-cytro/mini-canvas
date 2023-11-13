class Course:
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
        self.id = id
        self.name = name
        self.description = description
        self.creator = creator
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        """
        Return a string representation of the Course.

        Returns:
        - str: A string representing the Course object.
        """
        return f"Id {self.id} (Name: {self.name}, Description: {self.description})"
