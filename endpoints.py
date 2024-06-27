from fastapi import Body, FastAPI

from Authentication.login import UserLogin
from Authentication.mfa import LoginMFA, SignUpMFA
from Authentication.signup import UserSignup
from Manager.manager import RetrievePassword, StorePassword

app = FastAPI()
currentUser = None


@app.post("/passkey/signup")
async def createAccount(user=Body()):
    global currentUser
    user = dict(user)

    # Create an instance to signup the user.
    currentUser = UserSignup(user["username"], user["password"], user["gmail"])

    # Perform MultiFactor Authentication
    mfa = SignUpMFA(user["username"])
    return mfa.outputURL


@app.get("/passkey/signup/{otp}")
async def verifySignUpOTP(otp: str):
    mfa = SignUpMFA(currentUser.username)
    if mfa.verifyOTP(otp):
        mfa.verified = True
    else:
        return "Incorrect OTP."

    currentUser.mfaCompleted = True
    output = currentUser.createAccount()

    return output


@app.post("/passkey/login")
async def loginUser(user=Body()):
    global currentUser
    user = dict(user)
    currentUser = UserLogin(user["username"], user["password"])
    output = currentUser.login()
    if output[0]:
        passwordVerification = currentUser.verifyPassword()
        if passwordVerification[0]:
            return "Proceed to mfa"
        else:
            return passwordVerification
    else:
        return output


@app.get("/passkey/login/{otp}")
async def verifyLoginOTP(otp: str):
    mfa = LoginMFA(currentUser.username)
    if mfa.verifyOTP(otp):
        mfa.verified = True
        currentUser.setAuthenticated()
        return "OTP Verification Successful."
    else:
        return "Incorrect OTP."


@app.post("/passkey/storepassword/{userId}")
async def storePassword(userId: int, passwordInformation=Body()):
    passwordInformation = dict(passwordInformation)
    sp = StorePassword(
        passwordInformation["website"],
        passwordInformation["username"],
        passwordInformation["password"],
        passwordInformation["description"],
        passwordInformation["url"],
        userId,
    )
    output = sp.storeNewPassword()
    return output


@app.post("/passkey/retrievepassword/{userId}")
async def getPassword(userId: int, searchKey=Body()):
    # For specific password to be returned the user has to specify either
    # website name or username in the searchKey(as a body).
    searchKey = dict(searchKey)
    rp = RetrievePassword(userId)
    output = rp.search(searchKey["website"], searchKey["username"])

    if output[0]:
        output = {
            "website": rp.website,
            "username": rp.username,
            "password": rp.password,
            "description": rp.description,
            "URL": rp.url,
        }
    else:
        return output[1]
    return output
