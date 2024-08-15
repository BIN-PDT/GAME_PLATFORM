from settings import *


class Timer:
    def __init__(self, duration, commnad=None, repeat=False, autostart=False):
        self.duration = duration
        self.is_active = False
        self.start_time = 0

        self.command = commnad
        self.repeat = repeat
        if autostart:
            self.activate()

    def __bool__(self):
        return self.is_active

    def activate(self):
        self.start_time = pygame.time.get_ticks()
        self.is_active = True

    def deactivate(self):
        self.start_time = 0
        self.is_active = False
        if self.repeat:
            self.activate()

    def update(self):
        if self.is_active:
            if pygame.time.get_ticks() - self.start_time >= self.duration:
                self.deactivate()
                if self.command:
                    self.command()
