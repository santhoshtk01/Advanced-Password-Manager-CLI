from Authentication import cursor, commit
from Authentication.Utils import AuthenticationUtilities


class UserSignup:

    def __init__(self, username: str, password: str, gmail: str) -> None:
        self.username = username
        self.password = password
        self.gmail = gmail

        # Google disabled access to gmail account by unknown apps
        # So for now I am setting the verification True by default.
        # TODO : Implement a mechanism to ensure the gmail exist.
        self.gmailVerified = True

    def createAccount(self) -> None:

        auth = AuthenticationUtilities(self.username, self.password, self.gmail)
        auth.startMFA()

        if auth.verificationSuccessful and self.gmailVerified:
            query = ("INSERT INTO "
                     "userCredentials(username, gmail, password)" +
                     f"VALUES('{self.username}', '{self.gmail}', '{self.password}');")
            cursor.execute(query)
            commit()
        else:
            print("There a problem with creating your account.")


if __name__ == '__main__':
    usp = UserSignup("santhosh123", "Santhosh123#$", "santhoshofficial.py@gmail.com")
    usp.createAccount()
