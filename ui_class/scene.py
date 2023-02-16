import sys
import pygame
import time
from options import *
from event_loop import *
from display_constants import screen, FPS
from threading import *
from ui_class.cursor import Cursor
from ui_class.scene_constants import *

class Scene():
    """
    Represents a virtual scene, where game objects or interfaces are displayed upon.
    """

    clock = pygame.time.Clock()

    def __init__(self) -> None:
        self.name = 'empty_scene_name'
        self.description = """No description."""

        self.surface = screen
        self.IsLoaded = False
        self.IsEnabled = True
        self.IsOnTop = False
        self.Cursor = Cursor
        self.m_pos = ()
        self.events = ()

        self.scenes_on_top = []

    @property
    def Surface(self) -> pygame.Surface:
        return self.surface

    @Surface.setter
    def Surface(self, value: pygame.Surface):
        self.surface = value


    """
    Abstract methods.

    Override functions you need.
    """

    def on_entry(self):
        """
        This is called once before loading the scene.
        """
        pass

    def on_exit(self):
        """
        This is called once after the scene unloads.
        """
        pass

    def display(self):
        """
        This is the main drawing function and runs as long as the scene is loaded.
        
        This is already in a loop, thus a drawing loop inside is not needed, although can put one if needed.
        """
        pass
    
    def update(self):
        """
        This is called once every frame.
        """
        pass
    
    def late_update(self):
        """
        This is called once every frame after the scene has been rendered.

        Checking for events happens here.
        """
        pass


    """
    Private methods.
    """

    def _entry(func):
        def entry(self):
            if Options.enableDebugMode:
                print(f"[Debug] Entry execution by {self.name}")
            self.on_entry()
            func(self)
        return entry

    def _exit(self):
        self.on_exit()
        
    @_entry
    def _load(self):
        if Options.enableDebugMode:
            print(f"[Debug] Loading scene {self.name}") 

        self.IsLoaded = True
        while self.IsLoaded:
            self._update()
            self.display()

            if self.scenes_on_top != None:
                for scene in self.scenes_on_top:
                    scene.display()

            self._late_update()
            self.Cursor.draw()
            pygame.display.update()
            self.clock.tick(FPS)

    def _update(self):
        self.m_pos = pygame.mouse.get_pos()
        self.update()
    
    def _late_update(self):
        
        if not self.IsOnTop:
            self.events = event_loop.get_event()
        # self.events = pygame.event.get()
        self.late_update()

    def _load_on_top(self, scene):
        scene.display()


    """
    Public methods.
    """

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
        self._exit()

    def switch_to(self, scene, delay_in_seconds: int=0):
        """
        Switch to scene.
        """
        self.unload(self)
        time.sleep(delay_in_seconds)
        scene.load()

    def get_event(self):
        pass

    def load_on_top(self, scene):
        """
        Loads a scene on top of this scene.
        """
        scene.IsLoaded = True
        scene.on_entry()
        self.scenes_on_top.append(scene)

    def unload_on_top(self, scene):
        """
        Unloads the scene on top of this scene.
        """
        try:
            self.scenes_on_top.remove(scene)
            scene.IsLoaded = False
            scene.on_exit()
            scene.unload()
        except:
            pass

    def _execute(self, target, delay_in_seconds, *args):
        for i in range(delay_in_seconds):
            time.sleep(1)

        match target:
            case 0:
                self.on_entry()
                pass
            case 1:
                self.on_exit()
                pass
            case 2:
                self.update()
                pass
            case 3:
                self.load()
                pass
            case 4:
                self.unload()
                pass
            case 5:
                self.switch_to(args[0], args[1])
                pass
            case 6:
                self.get_event()
                pass
            case 7:
                self.load_on_top(args[0])
                pass
            case 8:
                self.unload_on_top(args[0])
            case 9:
                self.execute(args[0], args[1], args[2])

    def execute(self, target: int, delay_in_seconds=0, args=None):
        """
        Delays execution of internal method.
        """
        thread = Thread(target=self._execute, args=(target, delay_in_seconds, args))
        thread.start()

