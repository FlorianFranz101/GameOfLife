class Controls:
    base_tick_speed = 1
    speed = 5
    cellsx = 120
    cellsy = 90
    cellschanged = False
    is_paused = True
    def __init__(self):
        self.set_speed(self.speed)
    def set_speed(self,speed):
        if(speed == 0):
            return
        self.speed = speed
        self.ticktime = 1/(speed*self.base_tick_speed)