# app/services/security.py

import os
from cryptography.fernet import Fernet

FERNET_SECRET_KEY = os.getenv("FERNET_SECRET_KEY")
fernet = Fernet(FERNET_SECRET_KEY.encode())

def encrypt(token: str) -> str:
    return fernet.encrypt(token.encode()).decode()

def decrypt(encrypted_token: str) -> str:
    return fernet.decrypt(encrypted_token.encode()).decode()
