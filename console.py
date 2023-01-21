import pygame
from damath.constants import PLAYER_ONE, PLAYER_TWO
from damath.piece import Piece
from objects import chips_surface
import threading

class Console:

    def __init__(self, game) -> None:
        self.game = game

        self.command = ""
        self.console_thread = None
        self.IsRunning = False
        self.IsReading = False

    def start(self):
        """
        Starts the console.
        """

        if self.IsRunning:
            return

        self.IsRunning = True
        self.console_thread = threading.Thread(target=self.read_user_input)  
        self.console_thread.start()

    def stop(self):
        """
        Stops the console.
        """

        self.IsRunning = False
        self.console_thread.join()

    def read_user_input(self):
        """
        Reads for user commands.
        """
        
        while self.IsRunning:
            self.command = input("> ")
            self.get_command(self.command)

    def get_command(self, command):
        command = command.strip("/")
        args = command.split()

        match args[0]:
            case "add":
                try:
                    if args[1]:
                        if args[2]:
                            if args[3]:
                                if args[4]:
                                    self.command_add((int(args[1]), int(args[2])), int(args[3]), int(args[4]))
                except:
                    self.invalid_usage(args[0])
            case "ct":
                self.command_change_turn()
            case "help":
                try:
                    match args[1]:
                        case "add":
                            print("Usage: /add col row player value")
                            print("Adds a piece to the given board column and row arguments.")
                        case "help":
                            self.command_help()
                        case "move":
                            print("Usage: /move col row")
                            print("Moves the selected piece to the given board column and row arguments.")
                            print("Use /select first before using")
                        case "remove":
                            print("Usage: /remove col row")
                            print("Removes a piece given board column and row arguments.")
                            print("Non-graveyard removal.")
                        case "restart":
                            print("Restarts the game.")
                        case "select":
                            print("Usage: /select col row")
                            print("Selects a cell given board column and row arguments.")
                except:
                    self.command_help()
            case "move":
                try:
                    self.command_move((int(args[1]), int(args[2])))
                except:
                    self.invalid_usage(args[0])
            case "remove":
                try:
                    self.command_remove((int(args[1]), int(args[2])))
                except:
                    self.invalid_usage(args[0])
            case "restart":
                self.command_restart()
            case "select":
                try:
                    self.command_select((int(args[1]), int(args[2])))
                except:
                    self.invalid_usage(args[0])                
            case _:
                print("Invalid command, type /help for available commands")

    def invalid_usage(self, command):
        """
        Prompt proper command usage.
        """
        
        print(f"Invalid usage, type /help {command} for usage")


    # Commands list

    def command_add(self, cell, player, value):
        if player == 1:
            color = PLAYER_ONE
        else:
            color = PLAYER_TWO

        piece = Piece(chips_surface, (cell[0], cell[1]), color, value)
        self.game.board.add_piece(piece)

    def command_change_turn(self):
        self.game.change_turn()

    def command_move(self, cell):
        if not self.game.selected_piece:
            print("No piece selected. Select a piece with /select first")
            return

        col, row = self.game.board.get_col_row(cell)
        self.game.select_move((col, row))

    def command_help(self):
        print("List of available commands:")
        print("/ct          : changes turns")
        print("/help        : displays this")
        print("/move        : moves selected piece")
        print("/remove      : removes a piece")
        print("/restart     : restarts the game")
        print("/select      : selects a piece")

    def command_remove(self, cell):
        self.game.board.remove(cell)

    def command_restart(self):
        pass

    def command_select(self, cell):
        col, row = self.game.board.get_col_row(cell)
        self.game.select((col, row))