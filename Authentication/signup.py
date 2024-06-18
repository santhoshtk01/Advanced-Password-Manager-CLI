from hashlib import sha512

from Authentication import cursor, commit
from Authentication.AuthUtils import AuthenticationUtilities
from Authentication.user import UserInformation


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

    def createAccount(self) -> None:
        """
        Create a new account for the user with username, password and gmail.
        - Performs password validation.
        - Ensures that username doesn't exist already.
        - Performs MultiFactor Authentication with Google Authenticator.
        """

        # Creating the instance of the Auth utilities and starting the MFA.
        auth = AuthenticationUtilities(self.username, self.password, self.gmail)
        auth.multiFactorAuthentication()

        # Creates a new record in the DB after MFA verification.
        if auth.verificationSuccessful and self.gmailVerified:
            hashed_password = sha512(self.password.encode()).hexdigest()
            query = ("INSERT INTO "
                     "userCredentials(username, gmail, password)" +
                     f"VALUES('{self.username}', '{self.gmail}', '{hashed_password}');")
            cursor.execute(query)
            commit()
        else:
            print("There a problem with creating your account.")


if __name__ == '__main__':
    usp = UserSignup("sandy", "Santhosh123#$", "santhoshofficial.py@gmail.com")
    usp.createAccount()
