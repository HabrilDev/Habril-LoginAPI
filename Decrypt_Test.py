from cryptography.fernet import Fernet
def load_key():
    return open("secret.key", "rb").read()

def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    print(decrypted_message.decode())

decrypt_message(b'gAAAAABiiOaW1K0ZQVCUBgTz434w4rlkAh-f2hHJfLSATkOY-y5HAgoveGnelfpCgUXKkcYBa8XmRK-Af677UeVZa18DfCqRxQ==')