import re
from typing import Tuple

from Authentication import cursor
from Authentication.Exceptions import UsernameAlreadyExist
from Authentication.mfa import MultiFactorAuthentication


class AuthenticationUtilities:

    def __init__(self, username: str, password: str, gmail: str):
        self.username = username
        self.password = password
        self.gmail = gmail
        self.verificationSuccessful = False

    def verify(self) -> bool:
        """
        Ensures that the `username` doesn't exist already and the password
        in our context that the master-password meets the standards.
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
        """Check if the password meets the standards or not."""
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

    def startMFA(self):
        # Check if the username already exist or not.
        try:
            self.verify()
        except UsernameAlreadyExist as error:
            print(error)
            exit(-1)

        # Check if the password meets the requirements.
        output = self.checkPassword()
        if output[0]:
            mfa = MultiFactorAuthentication()
            mfa.generateOTP()

            if mfa.verified:
                self.verificationSuccessful = True
        else:
            print(output[1])
