import uuid
import hashlib
from datetime import datetime


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
