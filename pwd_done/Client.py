import socket

from cryptography.fernet import Fernet


class ClientLogin:
    def __init__(self):
        self.key = open("secret.key", "rb").read()
        self.host = "cryotec.boldmoon.in"
        self.port = 5555
        self.client_socket = socket.socket()
        self.client_socket.connect((self.host, self.port))
        # self.background_listen_thread = threading.Thread(target=self.background_listen)
        # self.background_listen_thread.start()
        self.kill_signal = False
        self.uname = None

    def start(self):
        while True:
            self.send_uname()
            if self.send_pwd() == "LIN":
                print("logged in")
                break
            else:
                print("Please retry logging in.\n")
                self.client_socket.send(self.encrypt_message('RLIN'))
                continue

    def background_listen(self):
        back_listen = self.client_socket.recv(1024)
        back_listen = self.decrypt_message(back_listen)
        if back_listen == "KILL INITIATED":
            print("Master KILL")

    def encrypt_message(self, message):
        encoded_message = message.encode()
        fernet = Fernet(self.key)
        encrypted_message = fernet.encrypt(encoded_message)
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        if encrypted_message == b'':
            return None
        fernet = Fernet(self.key)
        decrypted_message = fernet.decrypt(encrypted_message)
        return decrypted_message.decode()

    def send_uname(self):
        while True:
            self.uname = input("Username: ")
            self.uname = self.uname.lower()
            self.client_socket.send(self.encrypt_message(self.uname))
            return_uname_data = self.client_socket.recv(1024)
            return_uname_data = self.decrypt_message(return_uname_data)
            if return_uname_data == "UDE":
                print("Username does not exist please enter correct username or create a Habril Account")
            else:
                break

    def send_pwd(self):
        while True:
            pwd = input("Password: ")
            pwd = self.encrypt_message(pwd)
            self.client_socket.send(pwd)
            return_pwd_data = self.client_socket.recv(1024)
            return_pwd_data = self.decrypt_message(return_pwd_data)
            if return_pwd_data == "CPWD":
                return "LIN"
            else:
                print(f"The entered password is not correct for the username {self.uname}.")
                retry_pwd = input(f"Do you want to change the entered username (CU) or retype the password for the "
                                  f"username {self.uname} (RP) ")
                if retry_pwd == "RP" or retry_pwd == "rp":
                    self.client_socket.send(self.encrypt_message('RP'))
                    continue
                else:
                    return "RLIN"


ash = ClientLogin()
ash.start()
