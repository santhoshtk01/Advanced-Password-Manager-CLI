import datetime
from typing import Tuple

from Manager import commit, cursor
from Manager import establishConnection as passwordConnection
from Manager.cipherManager import CipherManager


class PasswordManager:
    def __init__(
        self,
        website: str,
        username: str,
        password: str,
        description: str,
        url: str,
        userId: int,
    ) -> None:
        self.website = website
        self.username = username
        self.password = password
        self.description = description
        self.url = url
        self.userId = userId
        self.key = None
        self.authenticated = False

    def checkAuthentication(self):
        password_cursor = passwordConnection()
        query = f"SELECT authenticated FROM loggedInUsers WHERE userId={self.userId};"
        password_cursor.execute(query)

        # Check the authenticated column and set.
        if password_cursor.fetchone()[0] == 1:
            self.authenticated = True


class StorePassword(PasswordManager):
    def __init__(
        self,
        website: str,
        username: str,
        password: str,
        description: str,
        url: str,
        userId: int,
    ) -> None:
        super().__init__(website, username, password, description, url, userId)
        self.checkAuthentication()

    def storeNewPassword(self) -> str:
        if self.authenticated:
            # Fetch the encryption key from the database
            self.key = cursor.execute(
                f"SELECT encryptionKey FROM loggedInUsers WHERE userId={self.userId};"
            )
            self.key = self.key.fetchone()[0]

            # Encrypt the password before storing it.
            self.encryptPassword()
            query = (
                f"INSERT INTO passwords(website_name, username, password, description, url, userId)"
                f"VALUES(?, ?, ?, ?, ?, ?);"
            )
            cursor.execute(
                query,
                (
                    self.website,
                    self.username,
                    self.password,
                    self.description,
                    self.url,
                    self.userId,
                ),
            )
            commit()

            return "Password Stored Successfully."

        return "User not logged in to the system."

    def encryptPassword(self):
        cipherManager = CipherManager(self.key, self.password)
        self.password = cipherManager.encrypt()


class UpdateInformation:
    def __init__(self, passwordId: int):
        self.passwordId = passwordId

    def updateWebsite(self, newWebsite: str) -> str:
        query = f"UPDATE passwords SET website_name='{newWebsite}' WHERE password_id={self.passwordId};"
        cursor.execute(query)
        commit()

        return "Website name updated successfully."

    def updateUsername(self, newUsername: str) -> str:
        query = f"UPDATE passwords SET username='{newUsername}' WHERE password_id={self.passwordId};"
        cursor.execute(query)
        commit()

        return "Username updated successfully."

    def updateDescription(self, newDescription: str) -> str:
        query = f"UPDATE passwords SET description='{newDescription}' WHERE password_id={self.passwordId};"
        cursor.execute(query)
        commit()

        return "Description updated successfully."

    def updateURL(self, newURL: str) -> str:
        query = (
            f"UPDATE passwords SET url='{newURL}' WHERE password_id={self.passwordId};"
        )
        cursor.execute(query)
        commit()

        return "URL updated successfully."

    def updatePassword(self, newPassword: str) -> str:
        # Fetch the old password from the DB.
        query = f"SELECT password FROM passwords WHERE password_id={self.passwordId};"
        cursor.execute(query)
        oldPassword = cursor.fetchone()[0]

        # Update the new password to the DB.
        query = f"UPDATE passwords SET password='{newPassword}' WHERE password_id={self.passwordId};"
        cursor.execute(query)
        commit()

        # Calculate the today's date.
        today = datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%y %H:%M:%S")

        # Create a new entry in the change history table.
        query = (
            f"INSERT INTO changeHistory(password_id, date_changed, password)"
            f"VALUES({self.passwordId}, '{today}', '{oldPassword}')"
        )
        cursor.execute(query)
        commit()

        return "Password Updated Successfully."


class RetrievePassword(PasswordManager):
    def __init__(self, userId: int = None):
        super().__init__(None, None, None, None, None, userId)

    def decryptPassword(self):
        # Fetch the encryption key from the database
        self.key = cursor.execute(
            f"SELECT encryptionKey FROM loggedInUsers WHERE userId={self.userId};"
        )
        self.key = self.key.fetchone()[0]

        cipher_manager = CipherManager(self.key, self.password)
        self.password = cipher_manager.decrypt()

    def search(self, website: str = "", username: str = "") -> Tuple[bool, str]:
        self.checkAuthentication()
        if self.authenticated:
            # Check which is used for searching
            if website:
                searchKey = website
            else:
                searchKey = username

            query = f"SELECT * FROM passwords WHERE username='{searchKey}';"
            cursor.execute(query)
            outputs = cursor.fetchone()

            # Assign all the attributes.
            self.website = outputs[1]
            self.username = outputs[2]
            self.password = outputs[3]
            self.description = outputs[4]
            self.url = outputs[5]

            self.decryptPassword()
            return True, "User Authenticated."

        return False, "User Not Logged Into the System."


if __name__ == "__main__":
    rp = RetrievePassword(1)
    rp.search("", "22z433")
    print(rp.password)
