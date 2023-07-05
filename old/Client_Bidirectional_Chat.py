import socket


def client_program():
    host = "cryotec.boldmoon.in"  # as both code is running on same pc
    port = 5555
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    message = input("---> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response
        print('Received from server: ' + data)  # show in terminal
        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


client_program()