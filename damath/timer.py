import time
from math import ceil
from .constants import TIMER_DURATION
from damath.ruleset import *

class Timer:

    def __init__(self, duration_in_seconds):
        self.duration = duration_in_seconds 
        self.start_time = 0 
        self.start_time_started = False
        self.currenttime = 0
        self.endtime = 0
        self.remaining_time = duration_in_seconds
        self.is_running = False 
    
    def set_duration(self, duration_in_seconds):
        self.duration = duration_in_seconds

    def start_timer(self):
        if not self.start_time_started:
            self.start_time = time.time()
            self.start_time_started = True

        self.is_running = True
        
    def update(self):
        self.endtime = self.start_time + self.duration 
        self.currenttime = time.time()

    def get_remaining_time(self):
        return self.remaining_time

    def pause(self):
        self.is_running = False

    def resume(self):
        self.start_time += ((time.time() - self.start_time) - (self.duration - self.remaining_time))
        self.is_running = True

    def toggle(self):
        if self.is_running:
            self.pause()
        else:
            self.resume()

    def stop(self):
        self.is_running = False

    def reset(self):
        self.remaining_time = self.duration
        self.is_running = True
        self.start_time = time.time()
        self.endtime = self.start_time + self.duration

class GlobalTimer(Timer):

    def __init__(self, duration_in_seconds):
        Timer.__init__(self, duration_in_seconds)

    def get_remaining_time(self) -> tuple:
        """
        Returns a tuple containing minutes and seconds
        """
        m, s = ceil(self.remaining_time//60), ceil(self.remaining_time%60)
        if s == 60: 
            s = 0
            m = ceil(self.remaining_time//60)+1
        return (m, s)

    #TODO: implement pause and resume and connect it to the turn timer (after fixing pause menu)

global_timer = GlobalTimer(Rules.timer_global)
turn_timer = Timer(Rules.timer_turn)
