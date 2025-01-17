import pygame
from damath.constants import PLAYER_ONE, PLAYER_TWO
from damath.game import Match
from damath.piece import Piece
from damath.ruleset import *
from damath.timer import *
from objects import chips_surface
from options import *
from client import Client
from server import Server
from player import Player
import threading

client = Client()
server = Server()

class DeveloperConsole:

    def __init__(self) -> None:
        self._main = None
        self._game = None
        self._server = None
        self._client = None
        self.Player = None

        self.IsServer = False
        self.IsClient = False
        self.IsRunning = False
        self.IsPaused = False

        self.ip_address = ''
        self.command = ''
        self.message = ''

        self.IsOperator = False
        self.ShowFeedback = True
        self.ShowConsoleGUI = False

    @property
    def Main(self):
        return self._main

    @Main.setter
    def Main(self, value):
        self._main = value

    @property
    def Game(self):
        return self._game

    @Game.setter
    def Game(self, value: Match):
        self._game = value

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, value: Server):
        self._server = value

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value: Client):
        self._client = value


    """
    Console private methods.
    """
    def _invalid_usage(self, command):
        """
        Prompts proper command usage.
        """
        print(f"Improper command usage, type /help {command} for usage")


    """
    Console public methods.
    """
    def start(self):
        """
        Starts the console.
        """
        if self.IsRunning:
            return
        self.IsRunning = True

        if enableDebugMode:
            print("[Debug]: Console started.")
        print("Type /help for a list of available commands")
        
        self.console_thread = threading.Thread(target=self.read, daemon=True)  
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
        if command == None or command == '':
            return
        if enableDebugMode:
            print(f"[Debug]: Command: {command}")

        self.message = command

        if self._server != None:
            if self.IsServer:
                self._server.send(self.message)
        if self._client != None:
            if self.IsClient:
                self._client.send(self.message)

    def send(self, message=''):
        """
        Send something to the connection.
        """
        if self._server != None:
            if self.IsServer:
                self._server.send(message)
        if self._client != None:
            if self.IsClient:
                self._client.send(message)

    def read(self):
        """
        Reads for user commands.
        """
        while self.IsRunning:
            if self.IsPaused:
                continue
            self.command = input(f"")
            self.run_command(self.command)

        if enableDebugMode:
            print("[Debug]: Closed the console.")
        return

    def pause(self, value: bool=None):
        """
        Pauses user input reading. Toggles with no argument.
        """
        if value != None:
            self.IsPaused = value
            return
        self.IsPaused = not self.IsPaused

    def run_command(self, command):
        command_raw = command
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
                        self._invalid_usage(args[0])
                case "chat":
                    try:
                        if args[1]:
                            if args[1] == "$$$in":
                                self._command_chat_in(command_raw)
                                return
                            match args[0]:
                                case "chat":
                                    self.command_chat(command_raw)
                    except:
                        self._invalid_usage(args[0])
                case "cheats":
                    self.command_cheats();
                case "connect" | "join":
                    try:
                        if args[1]:
                            try:
                                if args[2]:
                                    self.command_connect(args[1], args[2])
                            except:
                                self.command_connect(args[1])
                    except:
                        self._invalid_usage(args[0])
                case "ct":
                    self.command_change_turn()
                case "deop":
                    self.command_deop()
                case "draw":
                    try:
                        if args[1]:
                            match args[1]:
                                case "yes":
                                    self._command_drawyes()
                                case "no":
                                    self._command_drawno()
                    except:
                        self.command_draw()
                case "exit":
                    self.command_exit()
                case "forfeit" | "ff":
                    try:
                        if args[1]:
                            match args[1]:
                                case "yes":
                                    self._command_ffyes()
                                case "no":
                                    self._command_ffno()
                    except:
                        self.command_forfeit()
                case "help":
                    try:
                        match args[1]:
                            case "1":
                                print("List of available commands:")
                                print("Page 1/2 | /help <page>")
                                print("/connect     : connect to match")
                                print("/chat        : send message to player")
                                print("/ct          : changes turns")
                                print("/deop        : remove operator privileges")
                                print("/debug       : toggle debug messages")
                                print("/draw        : offer draw")
                                print("/forfeit     : resign from match")
                                print("/help        : displays this")
                                print("/host        : host local match")
                                print("/match       : create a match")
                            case "2":
                                print("List of available commands:")
                                print("Page 2/2 | /help <page>")
                                print("/move        : moves selected piece")
                                print("/op          : make this console operator")
                                print("/remove      : removes a piece")
                                print("/restart     : restarts the match")
                                print("/rules       : adjust match rules")
                                print("/select      : selects a piece")
                                print("/smove       : selects and moves a piece")
                                print("/timer       : toggle timer")
                                print("/toggle      : toggle certain rules")
                            case "add":
                                print("Usage: /add <col> <row> <player:1|2> <value>")
                                print("Adds a piece to the given board column and row arguments.")
                            case "connect":
                                print("Usage: /connect <ip> [name]")
                                print("Connect to a local game.")
                            case "chat":
                                print("Usage: /chat <message>")
                                print("Sends a message to the other player.")
                            case "help":
                                self.command_help()
                            case "host":
                                print("Usage: /host")
                                print("Host local match.")
                            case "match":
                                print("Usage: /match <create|start> <classic|speed|checkers>")
                                print("Creates a match with specified mode.")
                            case "move":
                                print("Usage: /move <col> <row>")
                                print("Moves the selected piece to the given board column and row arguments.")
                                print("Use /select first before using")
                            case "remove":
                                print("Usage: /remove <col> <row>")
                                print("Removes a piece given board column and row arguments.")
                                print("Non-graveyard removal.")
                            case "rules":
                                print("Usage: /rules <get|set>")
                                print("Gets or sets the match's rulestring.")
                            case "restart":
                                print("Restarts the game.")
                            case "select":
                                print("Usage: /select <col> <row>")
                                print("Selects a cell given board column and row arguments.")
                            case "smove":
                                print("Usage: /smove <piece_col> <piece_row> <col> <row>")
                                print("Selects and immediately moves the piece to the given board column and row arguments.")
                            case "toggle":
                                print("Usage: /toggle <actions|cheats>")
                                print("Toggle actions or cheats.")
                    except:
                        self.command_help()
                case "host":
                    self.command_host()
                case "match":
                    try:
                        if args[1]:
                            match args[1]:
                                case "create":
                                    if args[2]:
                                            self.command_match(args[2])
                                case "start":
                                    self._command_match_start()
                                case _:
                                    self._invalid_usage(args[0])
                    except:
                        self._invalid_usage(args[0])
                case "move" | "mov":
                    try:
                        self.command_move((int(args[1]), int(args[2])))
                    except:
                        self._invalid_usage(args[0])
                case "op":
                    self.command_op()
                case "remove" | "rm":
                    try:
                        self.command_remove((int(args[1]), int(args[2])))
                    except:
                        self._invalid_usage(args[0])
                case "restart":
                    self.command_restart()
                case "rules":
                    try:
                        if args[1]:
                            match args[1]:
                                case "get":
                                    print(Rules.get_rulestr())
                                case "set":
                                    if args[2]:
                                        Rules.set_rulestr(args[2])
                    except:
                        self._invalid_usage(args[0])  
                case "select" | "sel":
                    try:
                        self.command_select((int(args[1]), int(args[2])))
                    except:
                        self._invalid_usage(args[0])      
                case "selmove" | "smove" | "sm":
                    try:
                        if args[1]:
                            if args[2]:
                                if args[3]:
                                    if args[4]:
                                        self.command_selmove((int(args[1]), int(args[2])), (int(args[3]), int(args[4])))
                    except:
                        self._invalid_usage(args[0])
                case "timer":
                    self.command_timer()
                case "toggle":
                    try:
                        if args[1]:
                            self.command_toggle(args[1])
                    except:
                        self._invalid_usage(args[0])
                case _:
                    print("Invalid command, type /help for available commands")
        except:
            pass

    def get_match_rule(self, match: Match=None) -> Ruleset:
        if match != None:
            try:
                return match.Rules
            except:
                print("Match has no ruleset.")
                return
        else:
            try:
                return self._main.Match.Rules
            except:
                print("Failed to get match ruleset.")
                return

    def get_match_rulestr(self, match: Match=None, IsCommand: bool=False) -> str:
        if match != None:
            if match.Rules != None:
                try:
                    rulestr = match.Rules.get_rulestr()
                    if IsCommand:
                        return "setrulestr {}".format(rulestr)
                    return rulestr
                except:
                    print("Match has no ruleset.")
                    return
        else:
            try:
                return self._main.Match.Rules.get_rulestr()
            except:
                print("Failed to get match rulestr.")
                return

    def set_match_rule(self, ruleset: Ruleset):
        try:
            self._main.Match.Rules = ruleset
        except:
            print("Failed to set ruleset.")

    def set_match_rulestr(self, rulestr: str):
        rulestr = rulestr[11:]
        try:
            self._main.Match.Rules.set_rulestr(rulestr)
        except:
            print("Failed to set rulestr.")

    def init_server(self):
        if not self.IsServer:
            return

        Rules.toggle_multiplayer()
        self._command_match_start()
            
    def init_client(self):
        if not self.IsClient:
            return
        if self._main.Match == None:
            self._main.create_match('classic')

        Rules.toggle_multiplayer()
        self._command_match_start()
        # self._command_flip()
        # self._command_lock()


    """
    Internal commands.
    """
    def _command_drawyes(self):
        #TODO
        pass

    def _command_drawno(self):
        #TODO:
        pass

    def _command_lock(self):
        self._game.toggle_player_controls()

    def _command_match_start(self):
        if self._main.Match.IsRunning:
            print("A match is already running.")
            return
        if self._main.Match == None:
            print("No match created yet. Create one with /match create <mode>")
            return
        self._main.Queue.put(self._main.add_match())

    def _command_ffyes(self):
        #TODO
        print("player forfeited")

    def _command_ffno(self):
        #TODO
        print("player didn't forfeit")
        
    def _command_flip(self):
        self._main.Match.Board.flip()

    def _command_chat_in(self, message):
        message = message[11:]

        if self.IsServer:
            print("<Client> {}".format(message))

        if self.IsClient:
            print("<Server> {}".format(message))

    """
    Commands list.
    """
    def command_add(self, cell, player, value):
        if player == 1:
            color = PLAYER_ONE
        else:
            color = PLAYER_TWO

        piece = Piece(chips_surface, (cell[0], cell[1]), color, value)
        self._game.Board.add_piece(piece)

    def command_chat(self, message):
        message = message[5:]

        if self.IsServer:
            self._server.send("chat $$$in {}".format(message))

        if self.IsClient:
            self._client.send("chat $$$in {}".format(message))

    def command_change_turn(self):
        self._game.change_turn()

    def command_cheats(self):
        if self.ShowFeedback:
            print("Toggled cheats.")
        self._main.Match.Rules.toggle_cheats()    

    def command_connect(self, address, name='Player'):
        if self.IsServer:
            self._server.stop()

        self._client = client
        self._client.console = self
        self._client.connect(address)

    def command_debug(self):
        self.ShowFeedback = not self.ShowFeedback

        if self.ShowFeedback:
            print("Toggled debug messages.")

    def command_deop(self):
        self.IsOperator = False
        
        if self.ShowFeedback:
            print("Removed console operator privileges.")

    def command_draw(self):
        if not self._main.Match.IsRunning:
            print("There's not a match running.")
            return

        print("Are you sure you want to offer a draw?")
        print("Type /draw <yes|no>")

    def command_exit(self):
        self.stop()

    def command_forfeit(self):
        if not self._main.Match.IsRunning:
            print("There's not a match running.")
            return

        print("Are you sure you want to forfeit?")
        print("Type /forfeit <yes|no>")

    def command_host(self):
        if not self._main.Match:
            print("Create a match first with /match create <mode>.")
            return
        if self.IsClient:
            self._client.stop()

        try:
            if self._server.IsRunning:
                print(f"Local match already hosted on {self._server.get_port()}")
                return
        except:
            self._server = server
            self._server.console = self
            self._server.start()

            if self.ShowFeedback:
                print(f"Hosted local match on {self._server.get_port()}")
                print(f"Join with /connect <your_local_ip>")

    def command_match(self, mode):
        #TODO: Can create a new match while one is still running
        if self._main.Match != None:
            if self._main.Match.IsRunning:
                print("A match is already running.")
                return
        
        try:
            self._main.create_match(mode)
            print(f"Match created. Start with /match start")
        except:
            print(f"Failed to created match.")
            
    def command_move(self, destination):
        if not self._main.Match.IsRunning:
            print("There's not a match running.")
            return
        if not self._game.selected_piece:
            print("No piece selected. Select a piece with /select first")
            return

        if self._game.Board.IsFlipped:
            destination_col, destination_row = self._game.Board.to_raw(destination)
        else:
            destination_col, destination_row = self._game.Board.get_col_row(destination)

        self._game.select_move((destination_col, destination_row))

    def command_op(self):
        self.IsOperator = True
        
        if self.ShowFeedback:
            print("Made this console an operator.")

    def command_help(self):
        print("List of available commands:")
        print("Page 1/2 | /help <page>")
        print("/connect     : connect to match")
        print("/chat        : send message to player")
        print("/ct          : changes turns")
        print("/deop        : remove operator privileges")
        print("/debug       : toggle debug messages")
        print("/draw        : offer draw")
        print("/forfeit     : resign from match")
        print("/help        : displays this")

    def command_remove(self, cell):
        self._game.Board.remove(cell)

    def command_restart(self):
        pass

    def command_select(self, cell, Bypass=False):
        if not self._main.Match.IsRunning:
            print("There's not a match running.")
            return

        if self._game.Board.IsFlipped:
            col, row = self._game.Board.to_raw(cell)
        else:
            col, row = self._game.Board.get_col_row(cell)

        if Bypass:
            self._game.select((col, row), Bypass)
        else:
            self._game.select((col, row), self.IsOperator)

    def command_selmove(self, cell, destination):
        """
        Selects and immediately moves the piece to destination cell.
        """

        if not self._main.Match.IsRunning:
            print("There's not a match running.")
            return
        
        self._game.toggle_indicators()
        if self._game.selected_piece:
            self.command_move(destination)  
            return
        self.command_select(cell, True)
        self.command_move(destination)
        self._game.toggle_indicators()

    def command_timer(self):
        turn_timer.toggle()

    def command_toggle(self, rule: str):
        match rule:
            case "actions":
                Rules.toggle_actions()
            case "cheats":
                Rules.toggle_cheats()
        
        if self.ShowFeedback:
            print(f"Toggled {rule}.")