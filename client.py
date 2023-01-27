"""
Server.
"""

from _thread import *
from options import maxBufferSize
import socket
import threading  

class Client:

    def __init__(self) -> None:
        # Define the port on which you want to connect
        self.port = 12345
        self.ip = ''
        self.localhost = '127.0.0.1'
        self.msg = ''
        self.IsRunning = False
        self.IsConnected = False
        self.IsConnecting = False
        self.IsSender = False
        self.max_connection_retries = 5
        self.command = None
        self._console = None

        self.c = None
        
        self.ChatIsRunning = False

    @property
    def console(self):
        return self._console
        
    @console.setter
    def console(self, value):
        self._console = value

    def connect(self, ip):
        """
        Connect client to target ip.
        """
        
        self.ip = ip
        self.client_thread = threading.Thread(target=self.run_client, args=(ip, self.port))
        self.client_thread.start()

    def stop(self):
        # Close everything that needs to be closed
        self._console.IsClient = False
        self.IsRunning = False

    def reconnect(self, ip):
        while not self.IsConnected:
            if not self.IsConnecting:
                self.connect(ip)

    def run_client(self, addr, port):
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if self.IsConnecting:
            return
        self.IsConnecting = True

        print(f"Connecting to local match...")
        try:
            self.c.connect((addr, port))
        except:
            print(f"Failed to connect to local match")
            self.IsConnecting = False
            return

        print(f"Connected to local match {addr}")
        self.IsConnecting = False
        self.IsConnected = True
        self._console.IsClient = True
        self._console._command_init_client()
        
        while self.IsConnected:
            try:
                reply = self.c.recv(maxBufferSize).decode('UTF-8').strip()

                if reply == 'ping':
                    self.c.send('pong'.encode())
                else:
                    self._console.run_command(reply.strip('ping'))
            except:
                print(f"Disconnected from the match.")
                self.c.close()
                self.IsConnected = False
                # self.reconnect(self.ip)

    def send(self, message):
        """
        Sends message to server.
        """

        if self.c == None:
            return
        
        msg = str(message)
        self.c.send(msg.encode())

    def receive(self, message):
        """
        Receives message.
        """

        self.msg = message
            