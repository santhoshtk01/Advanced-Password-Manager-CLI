import string

import pyotp
import qrcode

from Authentication import commit, cursor


class MFAInformation:
    def __init__(self, username: str) -> None:
        self.username = username
        self.verified = False


class MultiFactorAuthentication(MFAInformation):
    def __init__(self, username: str):
        super().__init__(username)
        self.totp = pyotp.TOTP(MultiFactorAuthentication.filterKey(username))

    def verifyOTP(self, otp: str) -> bool:
        """
        Do verify the OTP entered by the user. set verified=True in successful attempt.
        """
        if self.totp.verify(otp):
            self.verified = True
            return True
        return False

    @staticmethod
    def filterKey(username: str) -> str:
        key = ""
        for char in username:
            if char not in string.digits and char not in string.punctuation:
                key += char
        return key


class SignUpMFA(MultiFactorAuthentication):
    """Contains attributes and methods needed to perform Multi-Factor Authentication."""

    def __init__(self, username: str) -> None:
        super().__init__(username)
        self.outputURL = self.totp.provisioning_uri()
        self.storeURL()

    def storeURL(self):
        # Store the `outputURL` in the DB.
        query = f"UPDATE userCredentials SET totpURL='{self.outputURL}' WHERE username='{self.username}';"
        cursor.execute(query)
        commit()

    def generateQR(self) -> None:
        # Create a QR Code
        qr = qrcode.make(self.outputURL)
        qr.show()


class LoginMFA(MultiFactorAuthentication):
    def __init__(self, username: str) -> None:
        super().__init__(username)
