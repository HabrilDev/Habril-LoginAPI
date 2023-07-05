import socket
import mysql.connector
import logging


class ServerLogin:
    def __init__(self):
        logging.basicConfig(filename="ServerLogin.log", format="%(asctime)s - %(levelname)s - %(message)s",
                            filemode="w")
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.info("The code is in INIT segment: ")
        self.logger.info("Initializing DB connection.")
        self.connection = mysql.connector.connect(host='ip',
                                                  database='db',
                                                  user='uname',
                                                  password='pwd')
        self.host = ''
        self.port = 5555
        self.logger.info("Creating socket instance.")
        self.server_socket = socket.socket()
        self.logger.info("Binding the port with host.")
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        self.logger.info(f"Accepting socket connection on port {self.port}")
        self.conn, self.address = self.server_socket.accept()
        self.logger.info(f"Connection from: {str(self.address)}")
        print("Connection from: " + str(self.address))

    def get_uname(self):
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("\nThe code is in USERNAME segment: ")
        uname_loop_ctrl = True
        self.logger.debug("Requesting db DB for User name list from LoginSystem table..")
        sql_uname_select_query = "select Username from LoginSystem"
        uname_cursor = self.connection.cursor()
        uname_cursor.execute(sql_uname_select_query)
        uname_records = uname_cursor.fetchall()
        self.logger.debug(f"Total number of username rows in table: {uname_cursor.rowcount}")
        while uname_loop_ctrl:
            self.logger.debug(f"Entered username control loop.")
            self.logger.debug(f"Waiting for username from {str(self.address)}")
            client_uname = self.conn.recv(1024).decode()
            self.logger.debug(f"Received username from {str(self.address)}")
            for uname_list in uname_records:
                if uname_list[0] == client_uname:
                    self.logger.debug("Username is valid, verified")
                    self.conn.send("UNAME_OK".encode())
                    print("Valid username")
                    uname_loop_ctrl = False
                    self.logger.debug("Changing uname_loop_ctrl to false, breaking record search FOR loop.")
                    break
            if uname_loop_ctrl:
                self.conn.send("UDE".encode())
                self.logger.debug("Username is not valid, out of FOR loop, going to continue in WHILE loop.")
                print("Not a valid username")
                continue
        self.logger.debug("Username verification is done, quitting get_uname method.")


har = ServerLogin()

har.get_uname()
