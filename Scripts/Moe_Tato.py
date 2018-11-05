import Game_FrameWork
import random
from pico2d import *
from math import *

import Game_World


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

class IdleState:

    @staticmethod
    def enter(MoeTato, event):
        pass

    @staticmethod
    def exit(MoeTato, event):
        pass

    @staticmethod
    def do(MoeTato):
        MoeTato.frame = (MoeTato.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % 9

    @staticmethod
    def draw(MoeTato):
        MoeTato.image.clip_draw(int(MoeTato.frame) * 463, 0, 463, 383, MoeTato.x, MoeTato.y)

class MoeTato:

    def __init__(self):
        self.x, self.y = 1600, 200
        self.image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\MoeTato\\Idle\\Idle-Sheet.png")
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def fire_ball(self):
        pass
        #ball = Ball(self.x, self.y, self.dir*3)
        #Game_World.add_object(ball, 1)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        print(self.cur_state, self.image)
    def draw(self):
        self.cur_state.draw(self)
#        self.font.draw(self.x - 60, self.y + 50, '(Time: %3.2f)' % get_time(), (255, 255, 0))

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)