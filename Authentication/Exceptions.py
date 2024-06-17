

class UsernameAlreadyExist(Exception):
    def __init__(self):
        super().__init__("The username already exist in the Database.")
