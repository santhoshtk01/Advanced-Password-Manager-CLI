import hashlib
import random
import re
import string
from typing import Tuple

import requests

from Manager import establishConnection


def checkPassword(password: str) -> Tuple[bool, str]:
    """
    Check if the password meets the standards or not.
    Returns:
        Tuple[bool, str]: False,  meaning full message if it doesn't meet the standards.
    """
    if len(password) < 8:
        return False, "The password length should be minimum of 8 characters."

    if re.search(r"[A-Z]", password) is None:
        return False, "The password should contain atleast one upper case letter."

    if re.search(r"[a-z]", password) is None:
        return False, "The password should contain atleast one lower case letter."

    if re.search(r"\d", password) is None:
        return False, "The password should contain atleast one digit."

    if re.search(r"^.*?[\W].*?$", password) is None:
        return False, "The password should contain atleast one special character."

    return True, "Meets all the requirements."


def generatePassword(length: int = 8, specialChars: bool = True) -> str:
    """
    Generate a strong password by satisfying the user requirements and standards.
    Args:
        length: The password length the user wants.
        specialChars: Indicates whether to include the special characters or not.
    Returns: Generated password as `str`.
    """
    values = [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        string.punctuation,
    ]
    output = ""

    # Check if the user needs special chars or not.
    if not specialChars:
        values.pop()

    # Generate specified length password and choose random values.
    for _ in range(length):
        chosen = random.choice(values)
        output += random.choice(chosen)

    return output


def checkExpose(password: str, password_id: int) -> None:
    # Convert the password into sha1
    sha1 = hashlib.sha1(password.encode()).hexdigest()
    proxyServers = [
        "http://139.224.117.52",
        "http://103.120.133.141",
        "http://190.61.47.78",
        "http://115.159.65.66",
        "http://135.125.56.179",
    ]

    # Make a request and check.
    url = f"https://api.pwnedpasswords.com/range/{sha1.upper()[:5]}"
    proxy = {"http": random.choice(proxyServers)}
    try:
        response = requests.get(url, proxies=proxy)
        hashes = [value.split(":") for value in response.text.splitlines()]

        # Check if any hash found.
        for exposed, count in hashes:
            if sha1.upper()[5:] == exposed:
                passwordCursor = establishConnection()
                passwordCursor.execute(
                    f"UPDATE passwords SET breached=1 WHERE password_id={password_id};"
                )
                print("Breached..")
                break
        print("Safe Password..")
    except Exception as error:
        print(error)
