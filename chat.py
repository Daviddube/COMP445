import socket
import threading
import argparse
import os
import datetime

def read_text_from_user_input(string):
    return input(string)
    
def build_message(user_message, user_command, user_name):
    return '' + user_name + '\n' + user_command  + "\n" + user_message + '\n'

def parse_message(application_message):
    user_name = application_message.split("\n")[0]
    user_command = application_message.split("\n")[1]
    user_message = application_message.split("\n")[2]
    return user_name, user_command, user_message

def chat():
    serverName = '127.0.0.1'
    serverPort = 8070
    user_name = read_text_from_user_input("Enter your name: ")
    threading.Thread(target=client, args=(user_name, serverName, serverPort)).start()
    threading.Thread(target=server, args=(serverName, serverPort)).start()


def client(user_name, serverName, serverPort):
    welcomeMessage = build_message('', 'JOIN', user_name)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    clientSocket.sendto(welcomeMessage.encode('ascii'),('255.255.255.255', serverPort))
    clientSocket.close()

    while True:
        user_message = read_text_from_user_input('')
        user_command = 'TALK'
        if(user_message == '/leave'):
            user_command = "LEAVE"
        if(user_message == '/who'):
            user_command = "WHO"
        application_message = build_message(user_message, user_command, user_name)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        if(user_command == "WHO"):
            clientSocket.sendto(application_message.encode('ascii'), (serverName, serverPort))
        else:
            clientSocket.sendto(application_message.encode('ascii'), ('255.255.255.255', serverPort))
        clientSocket.close()
        if(user_command == "LEAVE"):
            user_command = "QUIT"
            application_message = build_message(user_message, user_command, user_name)
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            clientSocket.sendto(application_message.encode('ascii'), (serverName, serverPort))
            clientSocket.close()
            exit(0)
        

def server(serverName, serverPort):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    users = []
    while True:
        application_message, address = serverSocket.recvfrom(2048)
        user_name, user_command, user_message = parse_message(application_message.decode('utf-8'))
        timestamp = datetime.datetime.now()
        if(user_command == "JOIN"):
            user_command = "PING"
            users.append(user_name)
            print(str(timestamp) + ' ' + user_name + ' joined!')
            user_name = users[0]
            if(address[0] != socket.gethostbyname(socket.gethostname())):
                application_message = build_message(user_message, user_command, user_name)
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                print(address)
                clientSocket.sendto(application_message.encode('ascii'), (address[0], serverPort))
                clientSocket.close()
        elif(user_command == "TALK"):
            print(str(timestamp) + ' [' + user_name + ']: ' + user_message)
        elif(user_command == "LEAVE"):
            print(users)
            users.remove(user_name)
            print(str(timestamp) + ' ' + user_name + ' left!')
        elif(user_command == "WHO"):
            print("Connected users: " + str(users))
        elif(user_command == "QUIT"):
            print("Bye now!")
            exit(0)
        elif(user_command == "PING"):
            print('username: ' + user_name)
            users.append(user_name)
        #else:
            #do nothing
chat()
