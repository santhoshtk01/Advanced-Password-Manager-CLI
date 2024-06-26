from hashlib import sha512
from typing import Tuple

from cryptography.fernet import Fernet

from Authentication import commit, cursor
from Authentication.user import UserInformation
from Manager import commit as password_commit
from Manager import establishConnection


class UserSignup(UserInformation):
    """
    Contains attributes and methods to signup the new user into the system.
    Methods:
        createAccount(self) -> None
        Create a new account for the user after ensuring the credentials meet the standards.
    """

    def __init__(self, username: str, password: str, gmail: str) -> None:
        """
        All the information are get from the user.
        Args:
            username: Unique username of the user.
            password: password entered by the user with standard password guidelines.
            gmail: gmail for the user.
        """
        super().__init__(username, password, gmail)

        # Google disabled access to gmail account by unknown apps
        # So, for now I am setting the verification True by default.
        # TODO : Implement a mechanism to ensure the gmail exist.
        self.gmailVerified = True

    def createAccount(self) -> Tuple[bool, str]:
        """
        Create a new account for the user with username, password and gmail.
        - Performs password validation.
        - Ensures that username doesn't exist already.
        - Ensures that multifactor authentication is successful.
        """

        # Creating the instance of the Auth utilities and starting the MFA.
        if not self.verify():
            return False, "Username Already Exist."

        # Creates a new record in the DB after MFA verification.
        if self.mfaCompleted and self.gmailVerified:
            hashed_password = sha512(self.password.encode()).hexdigest()
            query = (
                "INSERT INTO "
                "userCredentials(username, gmail, password)"
                + f"VALUES('{self.username}', '{self.gmail}', '{hashed_password}');"
            )
            cursor.execute(query)

            # Add a new record to the `loggedInUsers` table in the `usersPasswords.db`.
            self.userId = cursor.execute(
                f"SELECT userId FROM userCredentials WHERE username='{self.username}';"
            )
            self.userId = self.userId.fetchone()[0]
            password_cursor = establishConnection()
            query = "INSERT INTO loggedInUsers(userId, username, encryptionKey)VALUES(?, ?, ?);"
            password_cursor.execute(
                query, (self.userId, self.username, Fernet.generate_key())
            )
            commit()
            password_commit()

            return True, "Account Created Successfully."

        else:
            return False, "There was a problem creating your account."

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
            return False

        return True
