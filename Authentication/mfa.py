import pyotp
import qrcode
import getpass


class MultiFactorAuthentication:
    """Contains attributes and methods needed to perform Multi-Factor Authentication."""
    def __init__(self):
        self.totp = None
        self.verified = False

    def generateOTP(self):
        """
        Do use TOTP to generate OTP. And shows a QR code. Scanned by the user with the help of Google
        Authenticator.
        Maximum of 3 OTP attempts allowed. If exceeds the system will exit.
        """
        def verifyOTP(attemptCount: int):
            """
            Do verify the OTP entered by the user. Logs in a successful attempt. After three unsuccessful attempts
            system exits.

            Args:
                attemptCount: Keeps track of the unsuccessful attempts.
                To calculate failure attempt : 3 - attemptCount.
            """

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
                    verifyOTP(attemptCount)

        self.totp = pyotp.TOTP(pyotp.random_base32())
        outputURL = self.totp.provisioning_uri()

        # Create a QR Code
        qr = qrcode.make(outputURL)
        qr.show()
        verifyOTP(3)


if __name__ == '__main__':
    mfaa = MultiFactorAuthentication()
    mfaa.generateOTP()
