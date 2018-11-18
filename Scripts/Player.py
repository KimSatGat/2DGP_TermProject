import Game_FrameWork
import random
from pico2d import *
from math import *
from Player_Bullet import Player_Bullet

import Game_World

timer = get_time()
jump_timer = None


# Player Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

# Player Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, TOP_UP,TOP_DOWN, GROUND, SPACE, X = range(9)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_UP): TOP_UP,
    (SDL_KEYDOWN, SDLK_UP): TOP_DOWN,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_x): X
}


# Player States

class IdleState:

    @staticmethod
    def enter(player, event):
        player.image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\Player\\Idle\\Player_Idle.png")
        player.frame = 0
        if event == RIGHT_DOWN:
            player.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            player.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            player.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            player.velocity += RUN_SPEED_PPS
        elif event == TOP_DOWN:
            player.image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\Player\\Idle\\Player_Idle_Up.png")
            player.updown = 1
        elif event == TOP_UP:
            player.image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\Player\\Idle\\Player_Idle.png")
            player.updown = 0

    @staticmethod
    def exit(player, event):
        if event == X:
            player.fire_bullet()

    @staticmethod
    def do(player):
        if player.isIdleFrameIncrease:
            player.frame += (FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % 5
            if player.frame >= 4:
                player.isIdleFrameIncrease = False
        else:
            player.frame -= (FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % 5
            if player.frame <= 0:
                player.isIdleFrameIncrease = True


    @staticmethod
    def draw(player):
        if player.dir == 1:
            if player.updown == 1:
                player.image.clip_draw(int(player.frame) * 134, 0, 134, 161, player.x, player.y)
            else:
                player.image.clip_draw(int(player.frame) * 134, 0, 134, 161, player.x, player.y)
        else:
            if player.updown == 1:
                player.image.clip_draw(int(player.frame) * 134, 0, 134, 161, player.x, player.y)
            else:
                player.image.clip_draw(int(player.frame) * 133, 161, 133, 158, player.x, player.y)



class RunState:

    @staticmethod
    def enter(player, event):
        player.image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\Player\\Run\\Player_Run.png")

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
        if event == X:
            player.fire_bullet()

    @staticmethod
    def do(player):
        if player.dir == 1:
            player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * ACTION_PER_TIME * Game_FrameWork.frame_time) % 16
        else:
            player.frame = (player.frame - (FRAMES_PER_ACTION * ACTION_PER_TIME * ACTION_PER_TIME * Game_FrameWork.frame_time)) % 16
        player.x += player.velocity * Game_FrameWork.frame_time
        player.x = clamp(25, player.x, 1600 - 25)

    @staticmethod
    def draw(player):
        if player.dir == 1:
            player.image.clip_draw(int(player.frame) * 144, 0, 144, 162, player.x, player.y)
        else:
            player.image.clip_draw(int(player.frame) * 144, 162, 144, 162, player.x, player.y)


class JumpState:

    @staticmethod
    def enter(player, event):
        player.image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\Player\\Jump\\Player_Jump.png")
        global timer, jump_timer
        jump_timer = get_time()
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
            player.fire_bullet()

    @staticmethod
    def do(player):
        global timer, jump_timer
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * ACTION_PER_TIME * Game_FrameWork.frame_time) % 8

        player.x += player.velocity * Game_FrameWork.frame_time
        player.x = clamp(25, player.x, 1600 - 25)
        if get_time() - jump_timer < 1:
            player.y += RUN_SPEED_PPS * Game_FrameWork.frame_time
        elif get_time() - jump_timer > 1:
            player.y -= RUN_SPEED_PPS * Game_FrameWork.frame_time
            if player.y <= 90:
                player.y = 90
                player.add_event(GROUND)


    @staticmethod
    def draw(player):
        if player.dir == 1:
            player.image.clip_draw(int(player.frame) * 80, 109, 80, 109, player.x, player.y)
        else:
            player.image.clip_draw(int(player.frame) * 80, 0, 80, 109, player.x, player.y)



next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, TOP_UP: IdleState, TOP_DOWN: IdleState , SPACE: JumpState, GROUND: IdleState, X: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, TOP_UP: IdleState, TOP_DOWN: IdleState , SPACE: JumpState, GROUND: RunState, X: RunState},
    JumpState: {RIGHT_UP: JumpState, LEFT_UP: JumpState, LEFT_DOWN: JumpState, RIGHT_DOWN: JumpState, TOP_UP: JumpState, TOP_DOWN: JumpState , SPACE: JumpState, GROUND :RunState, X: JumpState},
}

class Player:

    def __init__(self):
        self.x, self.y = 1900 // 2, 90
        self.image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\Player\\Idle\\Player_Idle.png")
        self.dir = 1
        self.updown = 0
        self.isIdleFrameIncrease = True
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def fire_bullet(self):
        player_bullet = Player_Bullet(self.x, self.y, self.dir*10)
        Game_World.add_object(player_bullet, 1)

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

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)