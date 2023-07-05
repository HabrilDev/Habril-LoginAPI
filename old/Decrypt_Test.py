from cryptography.fernet import Fernet
def load_key():
    return open("secret.key", "rb").read()

def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    print(decrypted_message.decode())

decrypt_message(b'gAAAAABiiMNSwMWLN_OCYfhxxILFdgDx3-luAw1hSBFZFQzkP8I-YnspyjuS6U35UrAcrUK-AbZ8U8TyoAc2q-w1QHb9R7ejdQ==')