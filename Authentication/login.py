from hashlib import sha512
from typing import Tuple

from Authentication import cursor
from Authentication.user import UserInformation


class UserLogin(UserInformation):
    """
    Contains attributes and methods needed to login the already registered user to the system.
    Methods:
        login(self) -> None
        Fetch the password and gmail from the database of the corresponding `username`.

        verifyPassword(self) -> bool
        Do check the `password` from the DB against the user entered password.
    """

    def __init__(self, username: str, password: str) -> None:
        """
        User entered information: username, __enteredPassword
        System fetched information: __actualPassword, gmail

        Args:
            username: Unique `username` entered by the user.
            password: `password` entered by the user.
        """
        super().__init__(username, password, None)
        self.__actualPassword = None
        self.authenticated = False

    def login(self) -> Tuple[bool, str]:
        """Fetch the `password` and `gmail` of the corresponding user and assign the attributes."""
        query = f"SELECT userId, password, gmail FROM userCredentials WHERE username='{self.username}';"
        cursor.execute(query)

        # Fetch details of the users.
        output = cursor.fetchone()
        if output is None:
            return False, "User Doesn't exist create your account."
        else:
            self.gmail = output[2]
            self.__actualPassword = output[1]
            self.userId = output[0]

        return True, "Proceed to MFA."

    def verifyPassword(self) -> Tuple[bool, str]:
        """Do compare the actualPassword against the enteredPassword."""
        hashed_password = sha512(self.password.encode()).hexdigest()
        if hashed_password == self.__actualPassword:
            return True, "Password Correct."
        else:
            return False, "Password Incorrect."
