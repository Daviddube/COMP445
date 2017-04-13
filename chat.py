import socket
import threading
import argparse
import os
import datetime

def read_text_from_user_input(string):
    return input(string)
    
def build_message(user_message, user_name):
    return '[' + user_name + ']:\n' + user_message + '\n'

def parse_message(application_message):
    print(application_message.split("\n"))
    user_name = application_message.split("\n")[0]
    user_message = application_message.split("\n")[1]
    return user_name, user_message

def chat():
    serverName = '127.0.0.1'
    serverPort = 8070
    user_name = read_text_from_user_input("Enter your name: ")
    threading.Thread(target=client, args=(user_name, serverName, serverPort)).start()
    threading.Thread(target=server, args=(serverName, serverPort)).start()


def client(user_name, serverName, serverPort):
    welcomeMessage = user_name + " joined!\n"
    welcomeMessage = build_message(welcomeMessage, '')
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSocket.sendto(welcomeMessage.encode('ascii'),(serverName, serverPort))
    clientSocket.close()
    while True:
        user_message = read_text_from_user_input('')
        application_message = build_message(user_message, user_name)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientSocket.sendto(application_message.encode('ascii'), (serverName, serverPort))
        clientSocket.close()
    
        

def server(serverName, serverPort):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    
    while True:
        application_message, address = serverSocket.recvfrom(2048)
        user_name, user_message = parse_message(application_message.decode('utf-8'))
        timestamp = datetime.datetime.now()
        print(str(timestamp) + ' ' + user_name + ' ' + user_message)
chat()
