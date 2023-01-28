import pygame
import time
from options import *


class Scene:

    def __init__(self) -> None:
        self.name = ''
        self.IsLoaded = False
        self.IsEnabled = True

    # Abstract
    def entry(self):
        """
        Do something before loading the scene.
        """
        if Options.enableDebugMode:
            print(f"[Debug] Entry execution by {self.name}")

        IsLoaded = True
        while IsLoaded:
            # Put elements here
            IsLoaded = False   # Set this after

    # Abstract
    def exit(self):
        """
        Do something after scene unloads.
        """
        if Options.enableDebugMode:
            print(f"[Debug] Exit execution by {self.name}")

        IsLoaded = True
        while IsLoaded:
            # Put elements here
            IsLoaded = False   # Set this after

    # Abstract
    def display(self):
        """
        Main display drawing loop.
        """
        # Put elements here


    # Public methods

    def load(self):
        """
        Load scene.
        """
        self._load()

    def unload(self):
        """
        Unload scene.
        """
        self.IsLoaded = False
        self.exit()

    def switch_to(self, scene, delay_in_seconds: int=0):
        """
        Switch to scene.
        """
        self.unload(self)
        time.sleep(delay_in_seconds)
        scene.load()
    
    def _entry(func):
        def on_entry(self):
            self.entry()
            func(self)
        return on_entry
        
    @_entry
    def _load(self):
        if Options.enableDebugMode:
            print(f"[Debug] Loading scene {self.name}") 

        self.IsLoaded = True
        while self.IsLoaded:
            self.display()

