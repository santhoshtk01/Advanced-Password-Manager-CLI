from hashlib import sha512

from Authentication import cursor
from Authentication.Utils import MultiFactorAuthentication
from Authentication.user import UserInformation


class UserLogin(UserInformation):
    """
    Contains attributes and methods needed to login the already registered user to the system.
    Methods:
        login(self) -> None
        Fetch the password and gmail from the database of the corresponding `username`.

        __verifyPassword(self) -> bool
        Do check the `password` from the DB against the user entered password.

        multiFactorAuthentication(self) -> None
        Do create QR code for OTP and verify it with the help of `Google authenticator`.
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

    def login(self):
        """Fetch the `password` and `gmail` of the corresponding user and assign the attributes.
        If username doesn't exist the program exit."""
        query = f"SELECT password, gmail FROM userCredentials WHERE username='{self.username}'"
        cursor.execute(query)

        # Fetch details of the users.
        output = cursor.fetchone()
        if output is None:
            print("Username doesn't exist. Please create your account..")
            exit(-1)
        else:
            self.gmail = output[1]
            self.__actualPassword = output[0]

    def __verifyPassword(self) -> bool:
        """Do compare the actualPassword against the enteredPassword."""
        hashed_password = sha512(self.password.encode()).hexdigest()
        if hashed_password == self.__actualPassword:
            return True
        else:
            print("Password incorrect.")
            return False

    def multiFactorAuthentication(self):
        """Perform MFA and ensure the verification of the password and MFA. If wrong information entered program
        exit."""
        mfa = MultiFactorAuthentication()
        self.login()

        if self.__verifyPassword():
            mfa.generateOTP()

            if mfa.verified:
                print("User logged in successfully..")
                self.authenticated = True
                # TODO : Set the authenticated column=True in users passwords field.
            else:
                exit(-1)
        else:
            exit(-1)


if __name__ == "__main__":
    ul = UserLogin("kumargnanam", "Santhosh123#$")
    ul.multiFactorAuthentication()

# TODO : Setup unittest.
