import time
from .constants import TIMER_DURATION

class Timer:

    def __init__(self, duration):
        self.duration = duration 
        self.starttime = 0 
        self.starttime_started = False
        self.currenttime = 0 
        self.endtime = 0
        self.remaining_time = 0
        self.is_running = False 

    def start_timer(self):
        if not self.starttime_started:
            self.starttime = time.time()
            self.starttime_started = True

        self.endtime = self.starttime + self.duration 
        self.is_running = True
        self.currenttime = time.time()

    def get_remaining_time(self):
        return self.remaining_time

    def stop(self):
        self.is_running = False

    def reset(self):
        self.remaining_time = 0
        self.is_running = True
        self.starttime = time.time()
        self.endtime = self.starttime + self.duration

turn_timer = Timer(TIMER_DURATION)

