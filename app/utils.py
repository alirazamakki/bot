# === FILE: app/utils.py ===
from cryptography.fernet import Fernet
import os


KEY_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'secret.key')


def get_or_create_key():
if os.path.exists(KEY_PATH):
return open(KEY_PATH, 'rb').read()
key = Fernet.generate_key()
open(KEY_PATH, 'wb').write(key)
return key


def encrypt_text(text: str) -> bytes:
key = get_or_create_key()
f = Fernet(key)
return f.encrypt(text.encode())


def decrypt_text(token: bytes) -> str:
key = get_or_create_key()
f = Fernet(key)
return f.decrypt(token).decode()