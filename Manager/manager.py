from Manager import cursor, commit
from cryptography.fernet import Fernet


class PasswordManager:

    def __init__(self, website: str, username: str, password: str, description: str, url: str, userId: int) -> None:
        self.website = website
        self.username = username
        self.password = password
        self.description = description
        self.url = url
        self.userId = userId


class StorePassword(PasswordManager):

    def __init__(self, website: str, username: str, password: str, description: str, url: str, userId: int) -> None:
        super().__init__(website, username, password, description, url, userId)
        self.password_id = None

    def storeNewPassword(self) -> None:
        query = (f"INSERT INTO passwords(website_name, username, password, description, url)"
                 f"VALUES('{self.website}', '{self.username}', '{self.password}', '{self.description}', '{self.url}');")
        cursor.execute(query)
        commit()

    def encryptPassword(self, key: str):
        fernet = Fernet(key)
        password_bytes = self.password.encode()
        encrypted_data = fernet.encrypt(password_bytes)

        self.password = encrypted_data

    def updateWebsite(self, newWebsite: str) -> None:
        pass

    def updateUsername(self, newUsername: str) -> None:
        pass

    def updateDescription(self, newDescription: str) -> None:
        pass

    def updateURL(self, newURL: str) -> None:
        pass

    def updatePassword(self, newPassword: str) -> None:
        # TODO : Make sure to add this in the change history.
        pass


class RetrievePassword(PasswordManager):
    def __init__(self):
        super().__init__(None, None, None, None, None, None)

    def decryptPassword(self, key: str):
        fernet = Fernet(key)
        password_bytes = fernet.decrypt(self.password)
        password_data = password_bytes.decode()

        self.password = password_data


