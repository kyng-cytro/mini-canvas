import os
import uuid
import hashlib
from getpass import getpass
from datetime import datetime
from prettytable import PrettyTable


MAX_ATTEMPTS = 5


class MaxAttemptsExceededError(Exception):
    """Exception raised when the maximum login attempts are exceeded."""
    pass


def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def reset_screen():
    clear_screen()
    print(
        """
   ▄▄   ▄▄ ▄▄▄ ▄▄    ▄ ▄▄▄    ▄▄▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄    ▄ ▄▄   ▄▄ ▄▄▄▄▄▄ ▄▄▄▄▄▄▄ 
  █  █▄█  █   █  █  █ █   █  █       █      █  █  █ █  █ █  █      █       █
  █       █   █   █▄█ █   █  █       █  ▄   █   █▄█ █  █▄█  █  ▄   █  ▄▄▄▄▄█
  █       █   █       █   █  █     ▄▄█ █▄█  █       █       █ █▄█  █ █▄▄▄▄▄ 
  █       █   █  ▄    █   █  █    █  █      █  ▄    █       █      █▄▄▄▄▄  █
  █ ██▄██ █   █ █ █   █   █  █    █▄▄█  ▄   █ █ █   ██     ██  ▄   █▄▄▄▄▄█ █
  █▄█   █▄█▄▄▄█▄█  █▄▄█▄▄▄█  █▄▄▄▄▄▄▄█▄█ █▄▄█▄█  █▄▄█ █▄▄▄█ █▄█ █▄▄█▄▄▄▄▄▄▄█
""")


def validate_string_input(input_string):
    """
    Validates string input.

    Parameters:
    - input_string (str): The input string to be validated.

    Returns:
    - bool: True if the input is a non-empty string, False otherwise.
    """
    return isinstance(input_string, str) and len(input_string) > 0


def validate_menu_input(input_value, min_value, max_value):
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
            print("Invalid username or password")
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


def hash_password(password):
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


def compare_password_to_hash(password, hashed_password):
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
