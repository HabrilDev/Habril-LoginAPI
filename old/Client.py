import socket
import logging


class ClientLogin:
    def __init__(self):
        logging.basicConfig(filename="ClientLogin.log", format="%(asctime)s - %(levelname)s - %(message)s",
                            filemode="w")
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.info("The code is in INIT segment: ")
        self.host = "cryotec.boldmoon.in"
        self.port = 5555
        self.logger.info("Creating socket instance.")
        self.client_socket = socket.socket()
        self.logger.info(f"Connecting to {self.host} on the port {self.port}.")
        self.client_socket.connect((self.host, self.port))
        self.logger.info(f"Connected to {self.host} on the port {self.port}.")

    def send_uname(self):
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("\nThe code is in USERNAME segment: ")
        while True:
            self.logger.debug("Entered username loop.")
            self.logger.debug("Requesting user for username")
            uname = input("Username: ")
            uname = uname.lower()
            self.logger.debug(f"Sending the entered username to {self.host}")
            self.client_socket.send(uname.encode())
            self.logger.debug(f"Waiting username verification response from {self.host}")
            return_uname_data = self.client_socket.recv(1024).decode()
            self.logger.debug(f"Received username verification response from {self.host}")
            if return_uname_data == "UDE":
                self.logger.debug(f"UDE response from {self.host}")
                print("Username does not exist please enter correct username or create a Habril Account")
            else:
                self.logger.debug(f"User name exists, going to break uname loop.")
                break


ash = ClientLogin()
ash.send_uname()
