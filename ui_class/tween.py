# tween - Python Tweening
"""
Implements tweening animations in Python.
"""

from ui_class.ease_funcs import *

DEFAULT_FPS = 60

class Move:
    """
    Move animation.
    """

    def __init__(self, object, pos=(), time_in_seconds=0, ease_type=linear, loop=none):
        self.object = object
        self.pos_x = object.x
        self.pos_y = object.y
        self.new_pos = pos
        self.distance_x = pos[0] - object.x
        self.distance_y = pos[1] - object.y 
        self.time_in_seconds = time_in_seconds
        self.ease_type = ease_type
        self.loop = loop
        self.anim_x = False
        self.anim_y = False
        self.IsPlaying = False
        self.IsReversed = False

        if pos[0] != object.x and pos[0] != 0:
            self.anim_x = True
        if pos[1] != object.y and pos[1] != 0:
            self.anim_y = True

        self.step = 0
        if time_in_seconds != 0:
            self.max_steps = DEFAULT_FPS * time_in_seconds
        else:
            self.max_steps = 1
    
    def update(self):
        """
        Updates the animation.
        """
        if not self.IsPlaying:
            return
        self.play()
            
    def play(self):
        """
        Plays animation.
        """
        
        if not self.IsPlaying:
            self.IsPlaying = True

        if self.step > self.max_steps:
            if self.loop == none:
                return
            if self.loop == clamp:
                self.step = 0
            elif self.loop == ping_pong:
                self.IsReversed = True
                self.step = self.max_steps
        elif self.step < 0:
            self.IsReversed = False
            self.step = 0

        if self.anim_x:
            offset_x = self.distance_x * (self.ease_type(self.step/self.max_steps))
            self.object.x = self.pos_x + offset_x
            
        if self.anim_y:
            offset_y = self.distance_y * (self.ease_type(self.step/self.max_steps))
            self.object.y = self.pos_y + offset_y

        if self.IsReversed:
            self.step -= 1
        else:
            self.step += 1

    def pause(self):
        """
        Pauses animation.
        """

        if self.IsPlaying:
            self.IsPlaying = False
        return

    def reset(self):
        """
        Resets animation.
        """
        self.object.x = self.pos_x
        self.object.y = self.pos_y
        self.step = 0
        pass

class Scale:
    """
    Scale animation.
    """
    
    def update(self):
        """
        Updates the animation.
        """
        if not self.IsPlaying:
            return
        self.play()

    def __init__(self, object, size=(), time_in_seconds=0, along_center=True, ease_type=linear, loop=none):
        self.object = object
        self.size_w = object.w
        self.size_h = object.h
        self.new_size = size
        self.distance_w = object.w - (object.w * size[0])
        self.distance_h = object.h - (object.h * size[1])
        self.time_in_seconds = time_in_seconds
        self.along_center = along_center
        self.pos_x = object.x
        self.pos_y = object.y
        self.ease_type = ease_type
        self.loop = loop
        self.anim_x = False
        self.anim_y = False
        self.IsPlaying = False
        self.IsReversed = False
        
        if size[0] != object.x and size[0] != 1:
            self.anim_x = True
        if size[1] != object.y and size[1] != 1:
            self.anim_y = True

        self.step = 0
        if time_in_seconds != 0:
            self.max_steps = DEFAULT_FPS * time_in_seconds
        else:
            self.max_steps = 1

    def play(self):
        """
        Plays animation.
        """
        
        if not self.IsPlaying:
            self.IsPlaying = True

        if self.step > self.max_steps:
            if self.loop == none:
                return
            if self.loop == clamp:
                self.step = 0
            elif self.loop == ping_pong:
                self.IsReversed = True
                self.step = self.max_steps
        elif self.step < 0:
            self.IsReversed = False
            self.step = 0

        if self.anim_x:
            offset_x = self.distance_w * (self.ease_type(self.step/self.max_steps))
            self.object.w = self.size_w + offset_x
            if self.along_center:
                self.object.x = self.pos_x - offset_x/2
            
        if self.anim_y:
            offset_y = self.distance_h * (self.ease_type(self.step/self.max_steps))
            self.object.h = self.size_h + offset_y
            if self.along_center:
                self.object.y = self.pos_y - offset_y/2

        if self.IsReversed:
            self.step -= 1
        else:
            self.step += 1

class Move_to:
    """
    Move animation.
    """

    def __init__(self, object, pos=(), time_in_seconds=0, ease_type=linear, loop=none):
        self.object = object
        self.pos_x = object.x
        self.pos_y = object.y
        self.new_pos = pos
        self.distance_x = object.x - pos[0]
        self.distance_y = object.y - pos[1]
        self.time_in_seconds = time_in_seconds
        self.ease_type = ease_type
        self.loop = loop
        self.anim_x = False
        self.anim_y = False
        self.IsPlaying = False
        self.IsReversed = False

        if pos[0] != object.x and pos[0] != 0:
            self.anim_x = True
        if pos[1] != object.y and pos[1] != 0:
            self.anim_y = True

        self.step = 0
        if time_in_seconds != 0:
            self.max_steps = DEFAULT_FPS * time_in_seconds
        else:
            self.max_steps = 1
    
    def update(self):
        """
        Updates the animation.
        """
        if not self.IsPlaying:
            return
        self.play()
            
    def play(self):
        """
        Plays animation.
        """
        
        if not self.IsPlaying:
            self.IsPlaying = True

        if self.step > self.max_steps:
            if self.loop == none:
                return
            if self.loop == clamp:
                self.step = 0
            elif self.loop == ping_pong:
                self.IsReversed = True
                self.step = self.max_steps
        elif self.step < 0:
            self.IsReversed = False
            self.step = 0

        if self.anim_x:
            offset_x = self.distance_x * (self.ease_type(self.step/self.max_steps))
            self.object.x = self.pos_x - offset_x
            
        if self.anim_y:
            offset_y = self.distance_y * (self.ease_type(self.step/self.max_steps))
            self.object.y = self.pos_y - offset_y

        if self.IsReversed:
            self.step -= 1
        else:
            self.step += 1

    def pause(self):
        """
        Pauses animation.
        """

        if self.IsPlaying:
            self.IsPlaying = False
        return

    def reset(self):
        """
        Resets animation.
        """
        self.object.x = self.pos_x
        self.object.y = self.pos_y
        self.step = 0
        pass