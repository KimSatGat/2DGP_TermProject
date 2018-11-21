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
        MoeTato.frame = (MoeTato.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % 7

    @staticmethod
    def draw(MoeTato):
        MoeTato.image.clip_draw(int(MoeTato.frame) * 530, 0, 530, 514, MoeTato.x, MoeTato.y)

class MoeTato:

    def __init__(self):
        self.x, self.y = 1600, 250
        self.image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\MoeTato\\Idle.png")
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def fire_ball(self):
        pass

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb_body1())
        draw_rectangle(*self.get_bb_body2())
        draw_rectangle(*self.get_bb_hand())

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def get_bb_body1(self):
        return self.x - 130, self.y - 250, self.x + 50, self.y - 50
    def get_bb_body2(self):
        return self.x - 90, self.y - 50, self.x + 50, self.y + 120
    def get_bb_hand(self):
        return self.x - 230, self.y - 150, self.x - 120, self.y - 100
