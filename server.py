# first of all import the socket library
import socket
from _thread import *
import threading

class Server:

    def __init__(self, console):
        # Game console
        self.console = console
        self.IsConnected = False
        # reserve a port on your computer in our
        # case it is 12345 but it can be anything
        self.port = 12345
        self.msg = ''
        self.reply = ''

        self.ChatIsRunning = False
        self.chat_thread = threading.Thread(target=self.chat)

    def start(self):
        """
        Start the server.
        """
        
        # Create a socket object	
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
        print("Socket successfully created")

        # Next bind to the port
        # we have not typed any ip in the ip field
        # instead we have inputted an empty string
        # this makes the server listen to requests
        # coming from other computers on the network
        self.socket.bind(('', self.port))
        print("Socket binded to %s" %(self.port))

        self.ip = self.port
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()

    def listen_for_connections(self):
        # Wait for one connection
        self.socket.listen(1)
        print ("Socket is listening...")

        c, addr = self.socket.accept()
        self.IsConnected = True
        self.IsSender = True
        print(f"Got connection from {addr}")
        return c, addr

    def run_server(self):
        # Listen for outside connections
        c, addr = self.listen_for_connections()
        self.ip = addr
        
        if not self.ChatIsRunning:
            self.chat_thread.start()

        while self.IsConnected:
            try:
                if msg == '':
                    c.send('ping'.encode())
                    #print("Sending ping")
                    self.reply = c.recv(1024).decode('UTF-8').strip()

                    if (self.reply != 'pong'):
                        print(f"{addr}: {self.reply}")
                        # self.run_console_command(reply)
                        self.IsSender = True
                else:
                    c.send(msg.encode())
                    msg = ''
                    self.IsSender = False
            except:
                print(f"{addr} has disconnected")
                self.IsConnected = False
                # self.server_thread.start()

    def chat(self):
        """
        Chat.
        """
        
        self.ChatIsRunning = True

        # while game is running
        while True:
            # Establish connection with client.
            if self.IsConnected:
                if self.IsSender == True:
                    input_msg = input("Enter message> ")
                    self.msg = input_msg
                    self.IsSender = False

    def get_ip(self):
        return self.ip

    def run_console_command(self, command):
        # Run string command
        self.console.run_command(command)