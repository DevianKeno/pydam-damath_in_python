# first of all import the socket library
import socket
from _thread import *
import threading

class Server:

    def __init__(self, console):
        # Game console
        self.console = console
        self.IsConnected = False
        self.port = 12345
        self.msg = ''
        self.reply = ''

        self.server_thread = threading.Thread(target=self.chat)

    def start(self):
        """
        Start the server.
        """
        
        # Create a socket object	
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
        print("Socket successfully created")

        # reserve a port on your computer in our
        # case it is 12345 but it can be anything
        self.IsConnected = False

        # Next bind to the port
        # we have not typed any ip in the ip field
        # instead we have inputted an empty string
        # this makes the server listen to requests
        # coming from other computers on the network
        self.socket.bind(('', self.port))
        print("Socket binded to %s" %(self.port))
        # Listen for outside connections
        self.listen_for_connections()

        self.IsSender = True
        
    def listen_for_connections(self):

        # Wait for one connection
        self.socket.listen(1)
        print ("Socket is listening...")        # Debug

        c, addr = self.socket.accept()
        # self.IsSender = True
        print("Got connection from ", addr)

        x = threading.Thread(target=self.server, args=(c, addr))
        x.start()
        # s.settimeout(10)
        self.server_thread.start()

    def server(self, conn, addr):
        # global msg, self.IsSender, connected
        self.IsConnected = True

        while self.IsConnected:
            try:
                if msg == '':
                    conn.send('ping'.encode())
                    #print("Sending ping")
                    self.reply = conn.recv(1024).decode('UTF-8').strip()

                    if (self.reply != 'pong'):
                        print(f"{addr}: {self.reply}")
                        # self.run_console_command(reply)
                        self.IsSender = True
                else:
                    conn.send(msg.encode())
                    msg = ''
                    self.IsSender = False
            except:
                print("Client has disconnected")
                self.IsConnected = False
                self.start()

    def chat(self):
        """
        Chat.
        """
        
        # while game is running
        while True:
            # Establish connection with client.
            if self.IsConnected:
                if self.IsSender == True:
                    input_msg = input(">> ")
                    self.msg = input_msg
                    self.IsSender = False

    def get_ip(self):
        ip = ''
        return ip

    def run_console_command(self, command):
        # Run string command
        self.console.run_command(command)