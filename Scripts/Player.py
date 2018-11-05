import Game_FrameWork
import random
from pico2d import *
from math import *
#from ball import Ball

import Game_World

#timer = get_time()

# Player Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

# Player Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP,  SPACE = range(5)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}


# Player States

class IdleState:

    @staticmethod
    def enter(player, event):
        player.image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\Player\\Idle\\Player_Idle.png")
        if event == RIGHT_DOWN:
            player.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            player.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            player.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            player.velocity += RUN_SPEED_PPS


    @staticmethod
    def exit(player, event):
        if event == SPACE:
            player.fire_ball()
        pass

    @staticmethod
    def do(player):
        global timer
        timer = get_time()
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % 5

    @staticmethod
    def draw(player):
        if player.dir == 1:
            player.image.clip_draw(int(player.frame) * 98, 0, 98, 155, player.x, player.y)
        else:
            player.image.clip_draw(int(player.frame) * 98, 155, 98, 155, player.x, player.y)


class RunState:


    @staticmethod
    def enter(player, event):
        player.image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\Player\\Run\\Player_Run2.png")

        if event == RIGHT_DOWN:
            player.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            player.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            player.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            player.velocity += RUN_SPEED_PPS
        player.dir = clamp(-1, player.velocity, 1)

    @staticmethod
    def exit(player, event):
        if event == SPACE:
            player.fire_ball()

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * ACTION_PER_TIME * Game_FrameWork.frame_time) % 16
        player.x += player.velocity * Game_FrameWork.frame_time
        player.x = clamp(25, player.x, 1600 - 25)

    @staticmethod
    def draw(player):

        if player.dir == 1:
            player.image.clip_draw(int(player.frame) * 175, 0, 175, 162, player.x, player.y)
        else:
            player.image.clip_draw(int(player.frame) * 175, 162, 175, 162, player.x, player.y)



next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,  SPACE: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, SPACE: RunState}
}

class Player:

    def __init__(self):
        self.x, self.y = 1900 // 2, 90
        self.image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\Player\\Idle\\Player_RightIdle.png")
#        self.font = load_font('ENCR10B.TTF', 32)
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def fire_ball(self):
        ball = Ball(self.x, self.y, self.dir*3)
        Game_World.add_object(ball, 1)

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
#        self.font.draw(self.x - 60, self.y + 50, '(Time: %3.2f)' % get_time(), (255, 255, 0))

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)