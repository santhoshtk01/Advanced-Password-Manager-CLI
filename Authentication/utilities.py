import re
from typing import Tuple


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

    if re.search(r'^.*?[\W].*?$', password) is None:
        return False, "The password should contain atleast one special character."

    return True, "Meets all the requirements."
