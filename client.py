# Import socket module
import socket
from _thread import *
import threading  

# Create a socket object
     
class Client:

    def __init__(self) -> None:
        # Define the port on which you want to connect
        self.port = 12345
        self.ip = ''
        self.localhost = '127.0.0.1'
        self.msg = ''
        self.IsConnected = False
        self.IsSender = False 
        
        self.ChatIsRunning = False
        self.chat_thread = threading.Thread(target=self.chat)

    def connect(self, ip):
        self.ip = ip
        self.client_thread = threading.Thread(target=self.run_client, args=(ip, self.port))
        self.client_thread.start()

        if not self.IsConnected:
            print(f"Attempting to reconnect to {ip}...")
            self.connect(ip)

    def run_client(self, addr, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"\nConnecting to local server {addr}...")

        try:
            s.connect((addr, port))
        except:
            print(f"Failed to connect to {addr}")
            return

        print(f"Connected to local server {addr}")
        self.IsConnected = True
        self.HasDisconnected = True
        
        if not self.ChatIsRunning:
            self.chat_thread.start()

        while self.IsConnected:
            try:
                #print("Receiving")
                reply = s.recv(1024).decode('UTF-8').strip()

                if msg != '':
                    s.send(msg.encode())
                    msg = ''
                elif reply == 'ping':
                    #print("Received Ping")
                    s.send('pong'.encode())
                else:
                    print(f"{addr}: {reply}")
                    self.IsSender = True
            except:
                print("\nYou disconnected from the host.")
                s.close()
                self.IsConnected = False
                self.connect(self.ip)

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
            