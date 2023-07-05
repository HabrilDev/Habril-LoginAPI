import socket
import threading

import mysql.connector
from cryptography.fernet import Fernet


class ServerLogin:
    def __init__(self):
        self.thread = None
        self.conn = None
        self.address = None
        self.end = False
        self.active_cons = []
        self.total_users = 0
        self.host = ''
        self.port = 5555
        self.key = open("secret.key", "rb").read()
        self.server_socket = socket.socket()
        self.server_socket.bind((self.host, self.port))
        self.connection = mysql.connector.connect(host='ip',
                                                  database='db',
                                                  user='uname',
                                                  password='pwd')
        self.standby_input_thread = threading.Thread(target=self.standby_input)
        self.standby_input_thread.start()

    def start(self):
        self.new_user_handler()

    def standby_input(self):
        while not self.end:
            request = input("")
            if request == "KILL ALL":
                for cons in self.active_cons:
                    cons.close()
                print("No issues")
            elif request == "at":
                print(threading.active_count())
            elif request == "tu":
                print(self.total_users)
            elif request == "atu":
                print(threading.active_count()-2)

    def new_user_handler(self):
        self.server_socket.listen(20)
        for index in range(20):
            self.conn, self.address = self.server_socket.accept()
            self.thread = threading.Thread(target=self.thread_user_handler, args=(self.conn, self.address, index+1))
            self.active_cons.append(self.conn)
            self.total_users = self.total_users+1
            self.thread.start()

    def thread_user_handler(self, sock, ip, thread_id):
        print(f"New thread created, user's ip is {ip}, thread id is {thread_id}")
        while True:
            uname = self.get_uname(sock, ip, thread_id)
            if self.get_pwd(sock, ip, thread_id, uname) == 'RLIN':
                print(f"RLIN for {ip} in thread {thread_id}")
                continue
            break
        sock.close()
        self.active_cons.remove(sock)
        print(f'Thread {thread_id} has ended')

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
                    return client_uname
            if uname_loop_ctrl:
                uname_sock.send(self.encrypt_message("UDE"))
                print(f"Invalid username provided by {uname_ip} in thread {uname_thread_id}")
                continue
            print("THis is wrong")
            break

    def get_pwd(self, pwd_sock, pwd_ip, pwd_thread_id, uname):
        sql_pwd_select_query = f"select Password from LoginSystem where Username = '{uname}'"
        pwd_cursor = self.connection.cursor()
        pwd_cursor.execute(sql_pwd_select_query)
        pwd_records = pwd_cursor.fetchall()
        pwd_record = pwd_records[0][0].encode()
        while True:
            client_pwd = pwd_sock.recv(1024)
            if self.decrypt_message(client_pwd) == self.decrypt_message(pwd_record):
                print(f"Valid username provided by {pwd_ip} in thread {pwd_thread_id}")
                pwd_sock.send(self.encrypt_message("CPWD"))
                break
            else:
                print(f"Wrong password provided by {pwd_ip} in thread {pwd_thread_id} for the username {uname}")
                pwd_sock.send(self.encrypt_message("WPWD"))
                return_rpwd_data = pwd_sock.recv(1024)
                return_rpwd_data = self.decrypt_message(return_rpwd_data)
                if return_rpwd_data == 'RLIN':
                    return 'RLIN'
                else:
                    continue


har = ServerLogin()
har.start()
