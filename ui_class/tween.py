# tween - Python Tweening
"""
Implements tweening animations in Python.
"""

from pygame import transform
from ui_class.ease_funcs import *
from display_constants import FPS

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
        self.IsFinished = False
        self.step = 0
        self.values = []

        if pos[0] != object.x:
            self.anim_x = True
        if pos[1] != object.y:
            self.anim_y = True

        if time_in_seconds != 0:
            self.max_steps = FPS * time_in_seconds
        else:
            self.max_steps = 1

        for i in range(self.max_steps):
            self.values.append(self.ease_type(i/self.max_steps))
    
    def update(self):
        """
        Updates the animation. (only when playing) (only when
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

        if self.step >= self.max_steps:
            if self.loop == none:
                self.IsFinished = True
                self.IsPlaying = False
                return
            if self.loop == clamp:
                self.step = 0
            elif self.loop == ping_pong:
                self.IsReversed = True
                self.step = self.max_steps - 1
        elif self.step < 0:
            self.IsReversed = False
            self.step = 0

        if self.anim_x:
            offset_x = self.distance_x * (self.values[self.step])
            self.object.x = self.pos_x + offset_x
            
        if self.anim_y:
            offset_y = self.distance_y * (self.values[self.step])
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
        self.IsFinished = False
        pass

class Scale:
    """
    Scale animation.
    """
    def __init__(self, object, size=(), time_in_seconds=0, along_center=True, ease_type=linear, loop=none):
        self.object = object
        self.size_w = object.w
        self.size_h = object.h
        self.new_size = size
        self.distance_w = (object.w * size[0]) - object.w
        self.distance_h = (object.h * size[1]) - object.h
        self.time_in_seconds = time_in_seconds
        self.along_center = along_center
        self.pos_x = object.x
        self.pos_y = object.y
        self.ease_type = ease_type
        self.loop = loop
        self.anim_w = False
        self.anim_h = False
        self.IsPlaying = False
        self.IsReversed = False
        self.step = 0
        self.values = []
        
        if size[0] != 1:
            self.anim_w = True
        if size[1] != 1:
            self.anim_h = True

        if time_in_seconds != 0:
            self.max_steps = FPS * time_in_seconds
        else:
            self.max_steps = 1

        for i in range(self.max_steps):
            self.values.append(self.ease_type(i/self.max_steps))
            
    def update(self):
        """
        Updates the animation. (only when playing)
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
            self.object.anim_scale = True

        if self.step >= self.max_steps:
            if self.loop == none:
                self.IsFinished = True
                self.IsPlaying = False
                return
            if self.loop == clamp:
                self.step = 0
            elif self.loop == ping_pong:
                self.IsReversed = True
                self.step = self.max_steps - 1
        elif self.step < 0:
            self.IsReversed = False
            self.step = 0

        if self.anim_w:
            offset_x = self.distance_w * (self.values[self.step])
            self.object.w = self.size_w + offset_x
            if self.along_center:
                self.object.x = self.pos_x - offset_x/2
            
        if self.anim_h:
            offset_y = self.distance_h * (self.values[self.step])
            self.object.h = self.size_h + offset_y
            if self.along_center:
                self.object.y = self.pos_y - offset_y/2

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
            self.object.anim_scale = False
        return

    def reset(self):
        """
        Resets animation.
        """
        self.object.w = self.size_w
        self.object.h = self.size_h
        self.step = 0
        self.IsFinished = False
        self.IsPlaying = False
        self.object.anim_scale = False
        pass

class Rotate:
    """
    Rotate animation.
    """
    def __init__(self, object, angle, time_in_seconds=0, along_center=True, ease_type=linear, loop=none):
        self.object = object
        self.rotation = object.rotation
        self.distance = object.rotation + angle
        self.along_center = along_center
        self.pos_x = object.x
        self.pos_y = object.y
        self.time_in_seconds = time_in_seconds
        self.ease_type = ease_type
        self.loop = loop
        self.IsPlaying = False
        self.InFinished = False
        self.IsReversed = False
        self.step = 0
        self.values = []

        if time_in_seconds != 0:
            self.max_steps = FPS * time_in_seconds
        else:
            self.max_steps = 1

        for i in range(self.max_steps):
            self.values.append(self.ease_type(i/self.max_steps))
    
    def update(self):
        """
        Updates the animation. (only when playing)
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
            self.object.anim_rot = True

        if self.step >= self.max_steps:
            if self.loop == none:
                self.IsFinished = True
                self.IsPlaying = False
                return
            if self.loop == clamp:
                self.step = 0
            elif self.loop == ping_pong:
                self.IsReversed = True
                self.step = self.max_steps - 1
        elif self.step < 0:
            self.IsReversed = False
            self.step = 0

        offset = self.distance * (self.values[self.step])
        self.object.rotation = self.rotation + offset

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
            self.object.anim_rot = False
        return

    def reset(self):
        """
        Resets animation.
        """
        self.object.rotation = self.rotation
        self.step = 0
        self.IsFinished = False
        self.IsPlaying = False
        self.object.anim_rot = False

class Move_Rect:
    """
    Move animation for rects.
    """

    def __init__(self, rect, pos=(), time_in_seconds=0, ease_type=linear, loop=none):
        self.rect = rect
        self.pos_x = rect.x
        self.pos_y = rect.y
        self.new_pos = pos
        self.distance_x = pos[0] - rect.x
        self.distance_y = pos[1] - rect.y 
        self.time_in_seconds = time_in_seconds
        self.ease_type = ease_type
        self.loop = loop
        self.anim_x = False
        self.anim_y = False
        self.IsPlaying = False
        self.IsFinished = False
        self.IsReversed = False
        self.step = 0
        self.values = []

        if pos[0] != rect.x:
            self.anim_x = True
        if pos[1] != rect.y:
            self.anim_y = True

        if time_in_seconds != 0:
            self.max_steps = FPS * time_in_seconds
        else:
            self.max_steps = 1

        for i in range(self.max_steps):
            self.values.append(self.ease_type(i/self.max_steps))
    
    def update(self):
        """
        Updates the animation. (only when playing)
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

        if self.step >= self.max_steps:
            if self.loop == none:
                self.IsFinished = True
                return
            if self.loop == clamp:
                self.step = 0
            elif self.loop == ping_pong:
                self.IsReversed = True
                self.step = self.max_steps - 1
        elif self.step < 0:
            self.IsReversed = False
            self.step = 0

        if self.anim_x:
            offset_x = self.distance_x * (self.values[self.step])
            self.rect.x = self.pos_x + offset_x
            
        if self.anim_y:
            offset_y = self.distance_y * (self.values[self.step])
            self.rect.y = self.pos_y + offset_y

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

    def reset(self):
        """
        Resets animation.
        """
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        self.step = 0
        self.IsFinished = False

class Scale_Rect:
    """
    Scale animation for Rects.
    """
    def __init__(self, rect, size=(), time_in_seconds=0, along_center=True, ease_type=linear, loop=none):
        self.rect = rect
        self.size_w = rect.w
        self.size_h = rect.h
        self.distance_w =  (rect.w * size[0]) - rect.w
        self.distance_h = (rect.h * size[1]) - rect.h
        self.time_in_seconds = time_in_seconds
        self.along_center = along_center
        self.pos_x = rect.x
        self.pos_y = rect.y
        self.ease_type = ease_type
        self.loop = loop
        self.anim_w = False
        self.anim_h = False
        self.IsPlaying = False
        self.InFinished = False
        self.IsReversed = False
        self.step = 0
        self.values = []
        
        if size[0] != 1:
            self.anim_w = True
        if size[1] != 1:
            self.anim_h = True

        if time_in_seconds != 0:
            self.max_steps = FPS * time_in_seconds
        else:
            self.max_steps = 1

        for i in range(self.max_steps):
            self.values.append(self.ease_type(i/self.max_steps))
            
    def update(self):
        """
        Updates the animation. (only when playing)
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

        if self.step >= self.max_steps:
            if self.loop == none:
                self.IsFinished = True
                return
            if self.loop == clamp:
                self.step = 0
            elif self.loop == ping_pong:
                self.IsReversed = True
                self.step = self.max_steps - 1
        elif self.step < 0:
            self.IsReversed = False
            self.step = 0

        if self.anim_w:
            offset_w = self.distance_w * (self.values[self.step])
            self.rect.w = self.size_w + offset_w
            if self.along_center:
                self.rect.x = self.pos_x - offset_w/2
            
        if self.anim_h:
            offset_h = self.distance_h * (self.values[self.step])
            self.rect.h = self.size_h + offset_h
            if self.along_center:
                self.rect.y = self.pos_y - offset_h/2

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

    def reset(self):
        """
        Resets animation.
        """
        self.object.w = self.size_w
        self.object.h = self.size_h
        self.step = 0
        self.IsFinished = False