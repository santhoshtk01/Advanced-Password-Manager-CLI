import hashlib
import threading

from Authentication import establishConnection
from Manager import establishConnection as managerConnection
from Manager.cipherManager import CipherManager
from utilities import checkExpose


class BreachMonitor:
    def __init__(self, userId: int):
        self.userId = userId
        self.key = None
        self.passwords = None
        self.passwordCursor = None
        self.__getInformationFromDB()

    @staticmethod
    def getSha1(password: str) -> str:
        hashedPassword = hashlib.sha1(password.encode()).hexdigest()
        return hashedPassword

    def __getInformationFromDB(self):
        self.passwordCursor = managerConnection()
        self.passwords = self.passwordCursor.execute(
            f"SELECT password_id, website_name, username, password "
            f"FROM passwords WHERE userId={self.userId};"
        ).fetchmany(3339)
        self.key = self.passwordCursor.execute(
            f"SELECT encryptionKey FROM loggedInUsers " f"WHERE userId={self.userId};"
        ).fetchone()[0]

    def checkForBreach(self):
        for information in self.passwords:
            passwordId, website_name, username, password = information
            password = CipherManager(self.key, password).decrypt()

            # Create a new thread for each password.
            newThread = threading.Thread(
                target=checkExpose, args=(self.getSha1(password), passwordId)
            )
            newThread.start()
            newThread.join()


def startMonitoring():
    userCursor = establishConnection()
    userCursor.execute("SELECT userId FROM userCredentials;")

    # Start an instance for each user in the DB.
    for user in userCursor.fetchall():
        breachMonitor = BreachMonitor(user[0])
        print(breachMonitor.checkForBreach())


if __name__ == "__main__":
    pass
