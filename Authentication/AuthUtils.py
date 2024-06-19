import re
from typing import Tuple

from Authentication import cursor
from Authentication.Exceptions import UsernameAlreadyExist
from Authentication.mfa import MultiFactorAuthentication
from Authentication.user import UserInformation


class AuthenticationUtilities(UserInformation):
    """
    Contains attributes and methods need to support the Authentication Process.
    Methods:
        verify(self) -> None
        Do check if the username entered by the user already exist.

        checkPassword(self) -> Tuple[bool, str]
        Do check if the password meets the standards or not.

        multiFactorAuthentication(self) -> None
        Do perform multi-factor authentication.
    """
    def __init__(self, username: str, password: str, gmail: str):
        super().__init__(username, password, gmail)
        self.verificationSuccessful = False

    def verify(self) -> bool:
        """
        Ensures that the `username` doesn't exist already.
        Returns:
            bool: True if the username doesn't already exist.
        Raises:
            UsernameAlreadyExist: If the username already exist in the DB.
        """
        query = "SELECT username FROM userCredentials;"
        cursor.execute(query)

        # Fetch all the usernames and check already exist.
        output = []
        for value in cursor.fetchall():
            output.append(value[0])

        if self.username in output:
            raise UsernameAlreadyExist()

        return True

    def checkPassword(self) -> Tuple[bool, str]:
        """
        Check if the password meets the standards or not.
        Returns:
            Tuple[bool, str]: False,  meaning full message if it doesn't meet the standards.
        """
        if len(self.password) < 8:
            return False, "The password length should be minimum of 8 characters."

        if re.search(r"[A-Z]", self.password) is None:
            return False, "The password should contain atleast one upper case letter."

        if re.search(r"[a-z]", self.password) is None:
            return False, "The password should contain atleast one lower case letter."

        if re.search(r"\d", self.password) is None:
            return False, "The password should contain atleast one digit."

        if re.search(r'^.*?[\W].*?$', self.password) is None:
            return False, "The password should contain atleast one special character."

        return True, "Meets all the requirements."

    def multiFactorAuthentication(self):
        """Do Perform multifactor authentication and set verficationSuccessful=True."""

        # Check if the username already exist or not.
        try:
            self.verify()
        except UsernameAlreadyExist as error:
            print(error)
            exit(-1)

        # Check if the password meets the requirements.
        output = self.checkPassword()

        if output[0]:
            # Create an instance of the mfa and start.
            mfa = MultiFactorAuthentication(self.username)
            mfa.generateQR()

            if mfa.verified:
                self.verificationSuccessful = True
        else:
            print(output[1])
