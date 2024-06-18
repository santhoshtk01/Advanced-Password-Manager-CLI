import random
import string


def generatePassword(length: int = 8, specialChars: bool = True) -> str:
    """
    Generate a strong password by satisfying the user requirements and standards.
    Args:
        length: The password length the user wants.
        specialChars: Indicates whether to include the special characters or not.
    Returns: Generated password as `str`.
    """
    values = [string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation]
    output = ""

    # Check if the user needs special chars or not.
    if not specialChars:
        values.pop()

    # Generate specified length password and choose random values.
    for _ in range(length):
        chosen = random.choice(values)
        output += random.choice(chosen)

    return output


if __name__ == '__main__':
    print(generatePassword(10, specialChars=False))
