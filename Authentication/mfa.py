import pyotp
import qrcode
import getpass


class MultiFactorAuthentication:

    def __init__(self):
        self.totp = None
        self.verified = False

    def generateOTP(self):
        def verifyOTP(attemptCount: int):
            # Verify the otp
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
