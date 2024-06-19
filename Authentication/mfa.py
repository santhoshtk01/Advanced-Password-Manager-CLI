import pyotp
import qrcode
import getpass
import string

from Authentication import cursor, commit


class MultiFactorAuthentication:
    """Contains attributes and methods needed to perform Multi-Factor Authentication."""

    def __init__(self, username: str):
        self.totp = pyotp.TOTP(MultiFactorAuthentication.filterKey(username))
        self.verified = False
        self.username = username
        self.outputURL = self.totp.provisioning_uri()
        self.storeURL()

    def storeURL(self):
        # Store the `outputURL` in the DB.
        query = f"UPDATE userCredentials SET totpURL='{self.outputURL}' WHERE username='{self.username}';"
        cursor.execute(query)
        commit()

    def verifyOTP(self):
        """
        Do verify the OTP entered by the user. Logs in a successful attempt. After three unsuccessful attempts
        system exits.
        Args:
            attemptCount: Keeps track of the unsuccessful attempts.
            To calculate failure attempt : 3 - attemptCount.
        """
        attemptCount = 3

        # Verify the otp and set verified=True
        otp = getpass.getpass("Enter the OTP: ")
        if self.totp.verify(otp):
            print("OTP Verification Successful..")
            self.verified = True
        else:
            print("Invalid OTP try again.")

            # Check if exceeds three attempts.
            # TODO: Mark the time and don't let the user login for 10 minutes after 3 invalid attempts.
            if attemptCount == 0:
                print("Attempts exceeded try again after some time.")
                exit(-1)
            else:
                attemptCount -= 1
                print(f"You have {attemptCount} left.")
                self.verifyOTP()

    def generateQR(self) -> None:
        # Create a QR Code
        qr = qrcode.make(self.outputURL)
        qr.show()
        self.verifyOTP()

    @staticmethod
    def filterKey(username: str) -> str:
        key = ""

        for char in username:
            if char not in string.digits and char not in string.punctuation:
                key += char

        return key


if __name__ == '__main__':
    mfaa = MultiFactorAuthentication("santhosh@#")
    mfaa.generateQR()

    # TODO : Don't show the QR on each time. Show it initially and store the URL.
