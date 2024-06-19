from Manager import cursor, commit
from Manager import establishConnection as passwordConnection
from cryptography.fernet import Fernet

import datetime


class PasswordManager:

    def __init__(self, website: str, username: str, password: str, description: str, url: str, userId: int) -> None:
        self.website = website
        self.username = username
        self.password = password
        self.description = description
        self.url = url
        self.userId = userId
        self.key = None
        self.passwordId = None
        self.__authenticated = False

    def checkAuthentication(self):
        password_cursor = passwordConnection()
        query = f"SELECT authenticated FROM loggedInUsers WHERE userId={self.userId};"
        password_cursor.execute(query)

        # Check the authenticated column and set.
        if password_cursor.fetchone()[0] == 1:
            self.__authenticated = True


class StorePassword(PasswordManager):

    def __init__(self, website: str, username: str, password: str, description: str, url: str, userId: int) -> None:
        super().__init__(website, username, password, description, url, userId)
        self.checkAuthentication()

    def storeNewPassword(self) -> None:

        # Fetch the encryption key from the database
        self.key = cursor.execute(f"SELECT encryptionKey FROM loggedInUsers WHERE userId={self.userId};")
        self.key = self.key.fetchone()[0]

        # Encrypt the password before storing it.
        self.encryptPassword()
        query = (f"INSERT INTO passwords(website_name, username, password, description, url)"
                 f"VALUES(?, ?, ?, ?, ?, ?);")
        cursor.execute(query, (self.website, self.username, self.password, self.description, self.url, self.userId))
        commit()

        # Fetch the password ID.
        self.passwordId = cursor.execute(f"SELECT password_id FROM passwords WHERE userId={self.userId} AND website_name='{self.website}';")

    def encryptPassword(self):
        fernet_instance = Fernet(self.key)
        self.password = fernet_instance.encrypt(self.password.encode())

    def updateWebsite(self, newWebsite: str) -> str:
        query = f"UPDATE passwords SET website_name='{newWebsite}' WHERE password_id={self.password_id};"
        cursor.execute(query)
        commit()

        return "Website name updated successfully."

    def updateUsername(self, newUsername: str) -> str:
        query = f"UPDATE passwords SET username='{newUsername}' WHERE password_id={self.password_id};"
        cursor.execute(query)
        commit()

        return "Username updated successfully."

    def updateDescription(self, newDescription: str) -> str:
        query = f"UPDATE passwords SET description='{newDescription}' WHERE password_id={self.password_id};"
        cursor.execute(query)
        commit()

        return "Description updated successfully."

    def updateURL(self, newURL: str) -> str:
        query = f"UPDATE passwords SET url='{newURL}' WHERE password_id={self.password_id};"
        cursor.execute(query)
        commit()

        return "URL updated successfully."

    def updatePassword(self, newPassword: str) -> str:

        # Fetch the old password from the DB.
        query = f"SELECT password FROM passwords WHERE password_id={self.password_id};"
        cursor.execute(query)
        oldPassword = cursor.fetchone()[0]

        # Update the new password to the DB.
        query = f"UPDATE passwords SET password='{newPassword}' WHERE password_id={self.password_id};"
        cursor.execute()
        commit()

        # Calculate the today's date.
        today = datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%y %H:%M:%S")

        # Create a new entry in the change history table.
        query = (f"INSERT INTO changeHistory(password_id, date_changed, password)"
                 f"VALUES({self.password_id}, '{today}', '{oldPassword}')")
        cursor.execute()
        commit()

        return "Password Updated Successfully."


class RetrievePassword(PasswordManager):
    def __init__(self, userId: int = None):
        super().__init__(None, None, None, None, None, userId)

    def decryptPassword(self):
        decryption_instance = Fernet(self.key)
        self.password = decryption_instance.decrypt(self.password).decode("utf-8")

    def searchByWebsite(self, website: str) -> None:
        query = f"SELECT * FROM passwords WHERE website='{website}';"
        cursor.execute(query)
        outputs = cursor.fetchone()

        # Assign all the attributes.
        self.website = outputs[1]
        self.username = outputs[2]
        self.password = outputs[3]
        self.description = outputs[4]
        self.url = outputs[5]

    def searchByUsername(self) -> None:
        pass


if __name__ == '__main__':
    rp = RetrievePassword(userId=5)
    rp.searchByWebsite("x")
    print(rp.password)


