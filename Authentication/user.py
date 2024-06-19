from Manager import establishConnection, commit


class UserInformation:

    def __init__(self, username: str, password: str, gmail: str) -> None:
        """
        Args:
            username: Unique username of the user.
            password: Password entered by the user with standards.
            gmail: The gmail of the user.
        """
        self.username = username
        self.password = password
        self.gmail = gmail
        self.userId = None

    def setAuthenticated(self):
        password_cursor = establishConnection()
        query = f"UPDATE loggedInUsers SET authenticated=1 WHERE userId={self.userId};"
        password_cursor.execute(query)
        commit()

    def unsetAuthenticated(self):
        password_cursor = establishConnection()
        query = f"UPDATE loggedInUsers SET authenticated=0 WHERE userId={self.userId};"
        password_cursor.execute(query)
        commit()
