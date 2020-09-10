from cryptography.fernet import Fernet
import config

def encrypt(plaintext):
    key = config.SECRET
    f=Fernet(key)
    encrypted = f.encrypt(plaintext.encode())
    return encrypted

#openssl rand -base64 32

def decrypt(encrypted):
    key = config.SECRET
    f=Fernet(key)
    decrypted = f.decrypt(encrypted)
    return decrypted.decode()
