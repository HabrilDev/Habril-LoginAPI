import socket
import threading
from cryptography.fernet import Fernet


class ClientLogin:
    def __init__(self):
        self.key = open("secret.key", "rb").read()
        self.host = "cryotec.boldmoon.in"
        self.port = 5555
        self.client_socket = socket.socket()
        self.client_socket.connect((self.host, self.port))
    #     self.background_listen_thread = threading.Thread(target=self.background_listen)
    #     self.background_listen_thread.start()
    #     self.kill_signal = False
    #
    # def background_listen(self):
    #     back_listen = self.client_socket.recv(1024)
    #     back_listen = self.decrypt_message(back_listen)
    #     if back_listen == "KILL INITIATED":
    #         self.kill_signal = True
    #         print("Master KILL")
    #         self.client_socket.close()

    def encrypt_message(self, message):
        encoded_message = message.encode()
        fernet = Fernet(self.key)
        encrypted_message = fernet.encrypt(encoded_message)
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        fernet = Fernet(self.key)
        decrypted_message = fernet.decrypt(encrypted_message)
        return decrypted_message.decode()

    def send_uname(self):
        while True:
            uname = input("Username: ")
            uname = uname.lower()
            self.client_socket.send(self.encrypt_message(uname))
            return_uname_data = self.client_socket.recv(1024)
            return_uname_data = self.decrypt_message(return_uname_data)
            if return_uname_data == "UDE":
                print("Username does not exist please enter correct username or create a Habril Account")
            else:
                break
        self.client_socket.close()


ash = ClientLogin()
ash.send_uname()
