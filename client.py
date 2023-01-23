"""
Server.
"""

import socket
from _thread import *
import threading  

class Client:

    def __init__(self) -> None:
        # Define the port on which you want to connect
        self.port = 12345
        self.ip = ''
        self.localhost = '127.0.0.1'
        self.msg = ''
        self.IsConnected = False
        self.IsConnecting = False
        self.IsSender = False
        self.max_connection_retries = 5
        
        self.ChatIsRunning = False
        self.chat_thread = threading.Thread(target=self.start_chat_service)

    def connect(self, ip):
        """
        Connect client to target ip.
        """
        
        self.ip = ip
        self.client_thread = threading.Thread(target=self.run_client, args=(ip, self.port))
        self.client_thread.start()

    def reconnect(self, ip):
        pass

    def run_client(self, addr, port):
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if self.IsConnecting:
            return
        self.IsConnecting = True

        print(f"Connecting to server...")
        try:
            c.connect((addr, port))
        except:
            print(f"Failed to connect to local server")
            self.IsConnecting = False
            return

        print(f"Connected to local server {addr}")
        self.IsConnecting = False
        self.IsConnected = True
        
        if not self.ChatIsRunning:
            self.chat_thread.start()

        while self.IsConnected:
            try:
                #print("Receiving")
                reply = c.recv(1024).decode('UTF-8').strip()

                if self.msg != '':
                    c.send(self.msg.encode())
                    self.msg = ''
                elif reply == 'ping':
                    #print("Received Ping")
                    c.send('pong'.encode())
                else:
                    print(f"{addr}: {reply}")
                    self.IsSender = True
            except:
                print(f"Disconnected from the host.")
                c.close()
                self.IsConnected = False
                self.connect(self.ip)

    def start_chat_service(self):
        """
        Chat.
        """
        
        self.ChatIsRunning = True

        # while game is running
        while True:
            # Establish connection with client.
            if self.IsConnected:
                if self.IsSender == True:
                    input_msg = input("[Client]> ")
                    self.msg = input_msg
                    self.IsSender = False
            