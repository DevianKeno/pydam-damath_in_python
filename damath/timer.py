import time
from math import ceil
from .constants import TIMER_DURATION

class Timer:

    def __init__(self, duration):
        self.duration = duration 
        self.starttime = 0 
        self.starttime_started = False
        self.currenttime = 0
        self.endtime = 0
        self.remaining_time = duration
        self.is_running = False 
    
    def set_duration(self, duration):
        self.duration = duration

    def start_timer(self):
        if not self.starttime_started:
            self.starttime = time.time()
            self.starttime_started = True

        self.is_running = True
        
    def update(self):
        self.endtime = self.starttime + self.duration 
        self.currenttime = time.time()

    def get_remaining_time(self):
        return self.remaining_time

    def pause(self):
        self.is_running = False

    def resume(self):
        self.starttime += ((time.time() - self.starttime) - (self.duration - self.remaining_time))
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
        self.starttime = time.time()
        self.endtime = self.starttime + self.duration

turn_timer = Timer(TIMER_DURATION)

class GlobalTimer(Timer):

    def __init__(self, duration):
        Timer.__init__(self, duration)

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

global_timer = GlobalTimer(5)
