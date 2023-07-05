import socket
import time
import threading
import mysql.connector
from cryptography.fernet import Fernet


class ServerLogin:
    def __init__(self):
        # self.new_user_handler_thread = None
        self.thread = None
        self.conn = None
        self.address = None
        # self.end = False
        # self.thread_user_handler_end = True
        self.host = ''
        self.port = 5555
        self.active_threads = list()
        self.connected_sockets = list()
        self.key = open("secret.key", "rb").read()
        self.server_socket = socket.socket()
        self.server_socket.bind((self.host, self.port))
        self.connection = mysql.connector.connect(host='ip',
                                                  database='db',
                                                  user='uname',
                                                  password='pwd')
        # self.standby_input_thread = threading.Thread(target=self.standby_input)
        # self.standby_input_thread.start()

    def start(self):
        self.new_user_handler()

    # def standby_input(self):
    #     while not self.end:
    #         request = input("")
    #         if request == "KILL ALL":
    #             self.end = True

    def new_user_handler(self):
        self.server_socket.listen(20)
        for index in range(20):
            self.conn, self.address = self.server_socket.accept()
            self.thread = threading.Thread(target=self.thread_user_handler, args=(self.conn, self.address, index + 1))
            self.active_threads.append(self.thread)
            self.thread.start()

    def thread_user_handler(self, sock, ip, thread_id):
        print(f"New thread created, user's ip is {ip}, thread id is {thread_id}")
        self.get_uname(sock, ip, thread_id)
        sock.close()
        # uname_thread = threading.Thread(target=self.get_uname, args=(sock, ip, thread_id))
        # uname_thread.start()
        # while self.thread_user_handler_end:
        #     if self.end:
        #         print("Kill by standby input")
        #         sock.send(self.encrypt_message("KILL INITIATED"))
        #         print("Kill message sent to user")
        #         time.sleep(5)
        #         sock.close()
        #         print("sock close")
        #         self.thread_user_handler_end = False

    def encrypt_message(self, message):
        encoded_message = message.encode()
        fernet = Fernet(self.key)
        encrypted_message = fernet.encrypt(encoded_message)
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        fernet = Fernet(self.key)
        decrypted_message = fernet.decrypt(encrypted_message)
        return decrypted_message.decode()

    def get_uname(self, uname_sock, uname_ip, uname_thread_id):
        uname_loop_ctrl = True
        sql_uname_select_query = "select Username from LoginSystem"
        uname_cursor = self.connection.cursor()
        uname_cursor.execute(sql_uname_select_query)
        uname_records = uname_cursor.fetchall()
        while uname_loop_ctrl:
            client_uname = uname_sock.recv(1024)
            client_uname = self.decrypt_message(client_uname)
            for uname_list in uname_records:
                if uname_list[0] == client_uname:
                    print(f"Valid username provided by {uname_ip} in thread {uname_thread_id}")
                    uname_sock.send(self.encrypt_message("VUNAME"))
                    uname_loop_ctrl = False
                    time.sleep(5)
                    break
            if uname_loop_ctrl:
                uname_sock.send(self.encrypt_message("UDE"))
                print(f"Invalid username provided by {uname_ip} in thread {uname_thread_id}")
                continue


har = ServerLogin()
har.start()
