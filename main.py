from Authentication.signup import UserSignup
from Authentication.login import UserLogin
from Manager.manager import StorePassword


def start():
    userId = None
    while True:
        choice = int(input("Enter a choice: "))
        if choice == 1:
            username = input("Username : ")
            password = input("Password : ")
            gmail = input("Gmail : ")
            sup = UserSignup(username, password, gmail)
            sup.createAccount()

        elif choice == 2:
            username = input("Username : ")
            password = input("Password : ")
            ulogin = UserLogin(username, password)
            ulogin.multiFactorAuthentication()
        else:
            website = input("Wesite : ")
            username = input("Username : ")
            password = input("Password : ")
            description = input("Description : ")
            url = input("URL : ")
            sp = StorePassword(website, username, password, description, url, 1)
            sp.storeNewPassword()


if __name__ == '__main__':
    start()
