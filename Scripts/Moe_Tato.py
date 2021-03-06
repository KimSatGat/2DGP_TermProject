import Game_FrameWork
import random
from pico2d import *
from Moe_Tato_Bullet import Moe_Tato_Bullet
from math import *

import Game_World

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5
IDLE, ATTACK, DEATH = range(3)

class IdleState:

    @staticmethod
    def enter(MoeTato, event):
        MoeTato.idle_time = get_time()

    @staticmethod
    def exit(MoeTato, event):
        pass

    @staticmethod
    def do(MoeTato):
        if get_time() - MoeTato.idle_time > 5:
            MoeTato.add_event(ATTACK)
        MoeTato.frame = (MoeTato.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % 7

    @staticmethod
    def draw(MoeTato):
        MoeTato.image.clip_draw(int(MoeTato.frame) * 530, 0, 530, 514, MoeTato.x, MoeTato.y)

class AttackState:

    @staticmethod
    def enter(MoeTato, event):
        MoeTato.image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\MoeTato\\Attack\\Attack-" + "1" + ".png")

    @staticmethod
    def exit(MoeTato, event):
        pass

    @staticmethod
    def do(MoeTato):
        if MoeTato.isDeath:
            MoeTato.add_event(DEATH)
            return
        MoeTato.frame = (MoeTato.frame + (FRAMES_PER_ACTION * 2) * ACTION_PER_TIME * Game_FrameWork.frame_time) % 17
        MoeTato.image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\MoeTato\\Attack\\Attack-" + str(int(MoeTato.frame)) + ".png")
        if int(MoeTato.frame) == 16 and MoeTato.isFire:
            MoeTato.fire_bullet(-200, -180)
            MoeTato.isFire = False
        if int(MoeTato.frame) < 5:
            MoeTato.isFire = True

    @staticmethod
    def draw(MoeTato):
        MoeTato.image.draw(MoeTato.x, MoeTato.y)

class DeathState:

    @staticmethod
    def enter(MoeTato, event):
        MoeTato.frame = 0
        MoeTato.image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\MoeTato\\Death.png")
        MoeTato.isDeathFrameIncrease = True

    @staticmethod
    def exit(MoeTato, event):
        pass

    @staticmethod
    def do(MoeTato):
        if MoeTato.isDeathFrameIncrease:
            MoeTato.frame  += (FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time * 3) % 9
            if MoeTato.frame >= 8:
                MoeTato.isDeathFrameIncrease = False
        else:
            MoeTato.frame -= (FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time * 3) % 9
            if MoeTato.frame <= 1:
                MoeTato.isDeathFrameIncrease = True

    @staticmethod
    def draw(MoeTato):
        MoeTato.image.clip_draw(int(MoeTato.frame) * 307, 0, 307, 438, MoeTato.x, MoeTato.y)

next_state_table = {
    IdleState: {ATTACK: AttackState, DEATH: DeathState},
    AttackState: {IDLE: IdleState, DEATH: DeathState}
}

class MoeTato:

    def __init__(self):
        self.x, self.y = 1600, 250
        self.image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\MoeTato\\Idle.png")
        self.frame = 0
        self.hp = 50
        self.idle_time = 5
        self.attack_time = 5
        self.isFire = True
        self.isDeath = False
        self.isDeathFrameIncrease = False
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def fire_bullet(self, offset_Position_X, offset_Position_Y):
        moetato_bullet = Moe_Tato_Bullet(self.x + offset_Position_X, self.y + offset_Position_Y, 15)
        Game_World.add_object(moetato_bullet, 1)

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

    def get_bb_body1(self):
        return self.x - 130, self.y - 250, self.x + 50, self.y - 50
    def get_bb_body2(self):
        return self.x - 90, self.y - 50, self.x + 50, self.y + 120
    def get_bb_hand(self):
        return self.x - 230, self.y - 150, self.x - 120, self.y - 100
