"""
Server.
"""

from _thread import *
from options import maxBufferSize
import socket
import threading


class Server:

    def __init__(self):
        # reserve a port on your computer in our
        # case it is 12345 but it can be anything
        self._console = None
        self.port = 12345
        self.msg = ''
        self.reply = ''
        self.IsRunning = False
        self.IsConnected = False
        self.connected_clients_count = 0

        # Server and Client sockets
        self.s = None
        self.c = None

        self.ChatIsRunning = False

    @property
    def console(self):
        return self._console
        
    @console.setter
    def console(self, value):
        self._console = value

    def start(self):
        """
        Start the server.
        """
        
        if self.IsRunning:
            return
        self.IsRunning = True
        self._console.IsServer = True

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
        self._console.IsServer = False
        self.IsRunning = False

    def listen_for_connections(self, count):
        """
        Wait for connections
        """

        self.s.listen(count)
        print (f"Waiting for players... ({self.connected_clients_count + 1}/2)")

        c, addr = self.s.accept()
        print(f"Got connection from {addr}")
        self.connected_clients_count += 1
        print (f"Match starting... ({self.connected_clients_count + 1}/2)")
        self.IsConnected = True
        self.IsSender = True
        # self._console._command_match_start()
        return c, addr

    def run_server(self):
        # Listen for outside connections
        self.c, addr = self.listen_for_connections(1)
        self.ip = addr

        # Send first ping
        self.c.send('ping'.encode())

        while self.IsConnected:
            try:
                reply = self.c.recv(maxBufferSize).decode('UTF-8').strip()

                if reply == 'pong':
                    self.c.send('ping'.encode())
                else:
                    self._console.run_command(reply.strip('pong'))
            except:
                print(f"{addr} has disconnected.")
                self.connected_clients_count -= 1
                self.IsConnected = False
                self.c, addr = self.listen_for_connections(1)

    def send(self, message):
        """
        Sends message to connected clients.
        """

        if self.c == None:
            return

        msg = str(message)
        self.c.send(msg.encode())

    def receive(self):
        """
        Receives message.
        """
        
        return self.c.recv(maxBufferSize).decode('UTF-8').strip()

    def get_port(self):
        return self.ip