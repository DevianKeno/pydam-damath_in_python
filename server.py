"""
Server.
"""

import socket
from _thread import *
import threading

class Server:

    def __init__(self):
        # reserve a port on your computer in our
        # case it is 12345 but it can be anything
        self.port = 12345
        self.msg = ''
        self.reply = ''
        self.IsRunning = False
        self.IsConnected = False
        self.connected_clients_count = 0

        self.ChatIsRunning = False
        self.chat_thread = threading.Thread(target=self.start_chat_service)

    def start(self):
        """
        Start the server.
        """
        
        if self.IsRunning:
            return
        self.IsRunning = True

        # Create a socket object	
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
        # print("Socket successfully created")

        # Next bind to the port
        # we have not typed any ip in the ip field
        # instead we have inputted an empty string
        # this makes the server listen to requests
        # coming from other computers on the network
        self.s.bind(('', self.port))
        # print("Socket binded to %s" %(self.port))

        self.ip = self.port
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()

    def stop(self):
        # Close everything that needs to be closed
        self.IsRunning = False

    def listen_for_connections(self, count):
        """
        Wait for connections
        """
        self.s.listen(count)
        print (f"Waiting for players... ({self.connected_clients_count + 1}/2)")

        c, addr = self.s.accept()
        self.connected_clients_count += 1
        self.IsConnected = True
        self.IsSender = True
        print(f"Got connection from {addr}")
        return c, addr

    def run_server(self):
        # Listen for outside connections
        c, addr = self.listen_for_connections(1)
        self.ip = addr
        
        if not self.ChatIsRunning:
            self.chat_thread.start()

        while self.IsConnected:
            try:
                if self.msg == '':
                    c.send('ping'.encode())
                    #print("Sending ping")
                    self.reply = c.recv(1024).decode('UTF-8').strip()

                    if (self.reply != 'pong'):
                        print(f"{addr}: {self.reply}")
                        # self.run_console_command(reply)
                        self.IsSender = True
                else:
                    c.send(self.msg.encode())
                    self.msg = ''
                    self.IsSender = False
            except:
                print(f"{addr} has disconnected")
                self.connected_clients_count -= 1
                self.IsConnected = False
                # self.server_thread.start()

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
                    input_msg = input("[Server]> ")
                    self.msg = input_msg
                    self.IsSender = False

    def listen_for_commands(self, command):
        pass

    def get_ip(self):
        return self.ip