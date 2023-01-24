import pygame
from damath.constants import PLAYER_ONE, PLAYER_TWO
from damath.piece import Piece
from damath.timer import *
from objects import chips_surface
from options import *
from client import Client
from server import Server
import threading

client = Client()
server = Server()

class Console:

    def __init__(self) -> None:
        self.game = None
        self.server = None
        self.client = None
        self.IsServer = False
        self.IsClient = False
        self.IsRunning = False

        self.ip_address = ''
        self.command = ''
        self.message = ''

        self.IsOperator = False
        self.ShowFeedback = True

    def start(self):
        """
        Starts the console.
        """

        if self.IsRunning:
            return

        if enableDebugMode:
            print("[Debug]: Console started.")
        
        self.IsRunning = True
        self.console_thread = threading.Thread(target=self.read_user_input)  
        self.console_thread.start()

    def stop(self):
        """
        Stops the console.
        """

        self.IsRunning = False

    def listen(self, command):
        """
        Listen for commands.
        """

        if command == None:
            return

        print(f"[Debug]: Command: {command}")
        self.message = command

        if self.client != None:
            if self.IsServer:
                self.send(self.message, self.server)

        if self.client != None:
            if self.IsClient:
                self.send(self.message, self.client)

    def send(self, message, to):
        to.receive(message)

    def read_user_input(self):
        """
        Reads for user commands.
        """
        
        while self.IsRunning:
            self.command = input(f"> ")
            self.run_command(self.command)

        if enableDebugMode:
            print("[Debug]: Closed the console.")
        return

    def echo(self, *args):
        
        pass

    def run_command(self, command):
        command = command.strip("/")
        args = command.split()

        try:
            match args[0]:
                case "_lock":
                    self._command_lock()
                case "_flip":
                    self._command_flip()
                case "add":
                    try:
                        if args[1]:
                            if args[2]:
                                if args[3]:
                                    if args[4]:
                                        self.command_add((int(args[1]), int(args[2])), int(args[3]), int(args[4]))
                    except:
                        self.invalid_usage(args[0])
                case "connect" | "join":
                    try:
                        if args[1]:
                            self.command_connect(args[1])
                    except:
                        self.invalid_usage(args[0])
                case "ct":
                    self.command_change_turn()
                case "deop":
                    self.command_deop()
                case "exit":
                    self.command_exit()
                case "help":
                    try:
                        match args[1]:
                            case "add":
                                print("Usage: /add <col> <row> <player> <value>")
                                print("Adds a piece to the given board column and row arguments.")
                            case "connect":
                                print("Usage: /connect <ip>")
                                print("Connect to a local game.")
                            case "help":
                                self.command_help()
                            case "host":
                                print("Usage: /host")
                                print("Host a local game.")
                            case "match":
                                print("Usage: /match <classic|speed|checkers>")
                                print("Creates a match with mode.")
                            case "move":
                                print("Usage: /move <col> <row>")
                                print("Moves the selected piece to the given board column and row arguments.")
                                print("Use /select first before using")
                            case "remove":
                                print("Usage: /remove <col> <row>")
                                print("Removes a piece given board column and row arguments.")
                                print("Non-graveyard removal.")
                            case "restart":
                                print("Restarts the game.")
                            case "select":
                                print("Usage: /select <col> <row>")
                                print("Selects a cell given board column and row arguments.")
                            case "smove":
                                print("Usage: /smove <piece_col> <piece_row> <col> <row>")
                                print("Selects and immediately moves the piece to the given board column and row arguments.")
                    except:
                        self.command_help()
                case "host":
                    self.command_host()
                case "match":
                    try:
                        self.command_move((args[1]))
                    except:
                        self.invalid_usage(args[0])
                case "move" | "mov":
                    try:
                        self.command_move((int(args[1]), int(args[2])))
                    except:
                        self.invalid_usage(args[0])
                case "op":
                    self.command_op()
                case "remove" | "rm":
                    try:
                        self.command_remove((int(args[1]), int(args[2])))
                    except:
                        self.invalid_usage(args[0])
                case "restart":
                    self.command_restart()
                case "select" | "sel":
                    try:
                        self.command_select((int(args[1]), int(args[2])))
                    except:
                        self.invalid_usage(args[0])      
                case "selmove" | "smove" | "sm":
                    try:
                        if args[1]:
                            if args[2]:
                                if args[3]:
                                    if args[4]:
                                        self.command_selmove((int(args[1]), int(args[2])), (int(args[3]), int(args[4])))
                    except:
                        self.invalid_usage(args[0])             
                case "timerp":
                    self.command_timer()
                case _:
                    print("Invalid command, type /help for available commands")
        except:
            pass

    def invalid_usage(self, command):
        """
        Prompts proper command usage.
        """
        
        print(f"Improper command usage, type /help {command} for usage")

    # Commands list

    def _command_init_server(self):
        self.command_op()

    def _command_init_client(self):
        #self.command_match()
        
        self._command_flip()
        self._command_lock()


    def _command_lock(self):
        self.game.toggle_player_controls()

    def _command_flip(self):
        self.game.board.flip()

    def command_add(self, cell, player, value):
        if player == 1:
            color = PLAYER_ONE
        else:
            color = PLAYER_TWO

        piece = Piece(chips_surface, (cell[0], cell[1]), color, value)
        self.game.board.add_piece(piece)

    def command_change_turn(self):
        self.game.change_turn()

    def command_connect(self, address):
        if self.IsServer:
            self.server.stop()

        self.client = client
        self.client.console = self
        self.client.connect(address)

    def command_debug(self):
        self.ShowFeedback = not self.ShowFeedback

        if self.ShowFeedback:
            print("Toggled debug messages.")

    def command_deop(self):
        self.IsOperator = False
        
        if self.ShowFeedback:
            print("Removed console operator privileges.")

    def command_exit(self):
        self.stop()

    def command_host(self):
        if self.IsClient:
            self.client.stop()

        try:
            if self.server.IsRunning:
                print(f"Local server already hosted on {self.server.get_ip()}")
                return
        except:
            self.server = server
            self.server.console = self
            self.server.start()

            if self.ShowFeedback:
                print(f"Hosted local server on {self.server.get_ip()}")

    def command_match(self, mode):
        pass

    def command_move(self, destination):
        if not self.game.selected_piece:
            print("No piece selected. Select a piece with /select first")
            return

        if self.game.board.IsFlipped:
            destination_col, destination_row = self.game.board.to_raw(destination)
        else:
            destination_col, destination_row = self.game.board.get_col_row(destination)

        self.game.select_move((destination_col, destination_row))

    def command_op(self):
        self.IsOperator = True
        
        if self.ShowFeedback:
            print("Made this console an operator.")

    def command_help(self):
        print("List of available commands:")
        print("/connect     : connect to match")
        print("/ct          : changes turns")
        print("/deop        : remove operator privileges")
        print("/debug       : toggle debug messages")
        print("/help        : displays this")
        print("/host        : host local match")
        print("/match       : create a match")
        print("/move        : moves selected piece")
        print("/op          : make this console operator")
        print("/remove      : removes a piece")
        print("/restart     : restarts the match")
        print("/select      : selects a piece")
        print("/smove       : selects and moves a piece")
        print("/timer       : toggle timer")

    def command_remove(self, cell):
        self.game.board.remove(cell)

    def command_restart(self):
        pass

    def command_select(self, cell, Bypass=False):
        if self.game.board.IsFlipped:
            col, row = self.game.board.to_raw(cell)
        else:
            col, row = self.game.board.get_col_row(cell)

        if Bypass:
            self.game.select((col, row), Bypass)
        else:
            self.game.select((col, row), self.IsOperator)

    def command_selmove(self, cell, destination):
        """
        Selects and immediately moves the piece to destination cell.
        """
        
        if self.game == None:
            if self.ShowFeedback:
                print("No match started yet. Start a match with /match first")
            return
        
        self.game.toggle_indicators()
        if self.game.selected_piece:
            self.command_move(destination)  
            return
        self.command_select(cell, True)
        self.command_move(destination)
        self.game.toggle_indicators()

    def command_timer(self):
        turn_timer.toggle()