from pygame import event

class EventLoop:

    def __init__(self):
        self.event_list = []

    def get_event(self):
        """
        Only one function should call this method, 
        and the other function who also needs the event list 
        should just get the event_list attribute
        """
        self.event_list = event.get()
        return self.event_list
        
event_loop = EventLoop()