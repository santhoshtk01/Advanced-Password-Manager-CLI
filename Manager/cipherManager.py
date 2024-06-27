from typing import Union

from cryptography.fernet import Fernet


class CipherManager:
    """Performs encryption and decryption of the passwords."""

    def __init__(self, key: bytes, password: Union[str, bytes]) -> None:
        """
        Args:
            key: The key stored in the DB for encryption and decryption for the password.
            password: The password can be either plan text(str) during encryption. Bytes(bytes) during decryption.
        """
        self.password = password
        self.fernetInstance = Fernet(key)

    def encrypt(self) -> bytes:
        return self.fernetInstance.encrypt(self.password.encode())

    def decrypt(self) -> str:
        return self.fernetInstance.decrypt(self.password).decode("utf-8")
