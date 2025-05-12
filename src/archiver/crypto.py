import os
import base64
from archiver.config import Config
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

AES_KEY = base64.b64decode(Config.AES_KEY)


def decrypt(data: str) -> str:
    encrypted_blob = base64.b64decode(data)
    nonce = encrypted_blob[:12]
    ciphertext = encrypted_blob[12:]
    aesgcm = AESGCM(AES_KEY)
    decrypted_data = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
    return decrypted_data.decode("utf-8")


def encrypt(data: str) -> str:
    data_bytes = data.encode("utf-8")
    aesgcm = AESGCM(AES_KEY)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, data_bytes, associated_data=None)
    encrypted_blob = base64.b64encode(nonce + ciphertext).decode("utf-8")
    return encrypted_blob
