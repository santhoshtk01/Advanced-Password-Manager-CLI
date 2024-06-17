

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
