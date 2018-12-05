import Game_FrameWork
from pico2d import *
from Player_Bullet import Player_Bullet
import Game_World

jump_timer = None
hit_timer = None

# Player Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30cm
RUN_SPEED_KMPH = 40.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
JUMP_SPEED_PPS = RUN_SPEED_PPS / 2

# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

# Player Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, NONE, GROUND_Idle, Ground_Run, SPACE, X, HIT, DEATH, NONE = range(12)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_x): X
}

# Player States

class IdleState:

    @staticmethod
    def enter(player, event):
        player.isJump = False
        player.velocity = False
        player.frame = 0

    @staticmethod
    def exit(player, event):
        if event == X:
            player.fire_bullet(50 * player.dir, 0)

    @staticmethod
    def do(player):
        global hit_timer

        if player.isDeath:
            player.add_event(DEATH)
            return

        #무적
        if hit_timer != None:
            if get_time() - hit_timer > 2:
                player.isHit = False
                hit_timer = None

        if player.FrameIncrease:
            player.frame += (FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % 5
            if player.frame >= 4:
                player.FrameIncrease = False
        else:
            player.frame -= (FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % 5
            if player.frame <= 0:
                player.FrameIncrease = True

    @staticmethod
    def draw(player):
        if player.dir == 1:
                if hit_timer != None:
                    player.opacity = player.frame % 2
                    player.idle_image.opacify(clamp(0.1, player.opacity, 1))
                player.idle_image.clip_draw(int(player.frame) * 134, 0, 134, 161, player.x, player.y)
        else:
                if hit_timer != None:
                    player.opacity = player.frame % 2
                    player.idle_image.opacify(clamp(0.1, player.opacity, 1))
                player.idle_image.clip_draw(int(player.frame) * 133, 161, 133, 158, player.x, player.y)

class RunState:

    @staticmethod
    def enter(player, event):
        player.frame = 0
        player.isJump = False
        player.velocity = True
        if event == RIGHT_DOWN:
            player.dir = 1
        elif event == LEFT_DOWN:
            player.dir = -1

    @staticmethod
    def exit(player, event):
        if event == X:
            player.fire_bullet(80 * player.dir, -10)

    @staticmethod
    def do(player):
        global hit_timer

        if player.isDeath:
            player.add_event(DEATH)
            return

        #무적 시간
        if hit_timer != None:
            if get_time() - hit_timer > 2:
                player.isHit = False
                hit_timer = None
        if player.dir == 1:
            player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * ACTION_PER_TIME * Game_FrameWork.frame_time) % 16
        elif player.dir == -1:
            player.frame = (player.frame - (FRAMES_PER_ACTION * ACTION_PER_TIME * ACTION_PER_TIME * Game_FrameWork.frame_time)) % 16
        player.x += player.dir * RUN_SPEED_PPS * Game_FrameWork.frame_time
        player.x = clamp(25, player.x, 1900 - 25)

    @staticmethod
    def draw(player):
        if player.dir == 1:
            if hit_timer != None:
                player.opacity = player.frame % 2
                player.run_image.opacify(clamp(0.1, player.opacity, 1))
            player.run_image.clip_draw(int(player.frame) * 144, 0, 144, 162, player.x, player.y)
        else:
            if hit_timer != None:
                player.opacity = player.frame % 2
                player.run_image.opacify(clamp(0.1, player.opacity, 1))
            player.run_image.clip_draw(int(player.frame) * 144, 162, 144, 162, player.x, player.y)

class JumpState:

    @staticmethod
    def enter(player, event):
        player.frame = 0
        if event == RIGHT_DOWN:
            player.dir = 1
            player.velocity = True
        elif event == LEFT_DOWN:
            player.dir = -1
            player.velocity = True

    @staticmethod
    def exit(player, event):
        if event == X:
            player.fire_bullet(0, 0)

    @staticmethod
    def do(player):
        global  jump_timer, hit_timer
        if player.isDeath:
            player.add_event(DEATH)
            return
        #무적
        if hit_timer != None:
            if get_time() - hit_timer > 2:
                player.isHit = False
                hit_timer = None
        #점프
        if not player.isJump:
            player.isJump = True
            jump_timer = get_time()
        if get_time() - jump_timer < 0.3:
            player.y += JUMP_SPEED_PPS * 5 * Game_FrameWork.frame_time
        elif get_time() - jump_timer > 0.3:
            player.y -= JUMP_SPEED_PPS * 5 * Game_FrameWork.frame_time
            if player.y <= 90:
                player.y = 90
                player.isJump = False
                if player.velocity:
                    player.add_event(Ground_Run)
                else:
                    player.add_event(GROUND_Idle)

        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * ACTION_PER_TIME * Game_FrameWork.frame_time) % 8
        if player.velocity:
            player.x += player.dir * RUN_SPEED_PPS * Game_FrameWork.frame_time
        player.x = clamp(25, player.x, 1600 - 25)

    @staticmethod
    def draw(player):
        if player.dir == 1:
            player.jump_image.clip_draw(int(player.frame) * 88, 0, 88, 109, player.x, player.y)
        else:
            player.jump_image.clip_draw(int(player.frame) * 88, 109, 80, 109, player.x, player.y)

class HitState:

    @staticmethod
    def enter(player, event):
        player.frame = 0

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        global hit_timer
        if player.isDeath:
            player.add_event(DEATH)
            return
        if not player.isHit:
            player.isHit = True
            hit_timer = get_time()
        if get_time() - hit_timer > 0.2:
                if player.velocity:
                    player.add_event(Ground_Run)
                else:
                    player.add_event(GROUND_Idle)
        if player.y >= 90:
            player.y = 90
            player.isJump = False
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % 6

    @staticmethod
    def draw(player):
        if player.dir == 1:
            player.hit_image.clip_draw(int(player.frame) * 125, 0, 125, 221, player.x, player.y)
        else:
            player.hit_image.clip_draw(int(player.frame) * 125, 221, 125, 221, player.x, player.y)

class DeathState:

    @staticmethod
    def enter(player, event):
        player.frame = 0

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        if not player.isGameOver:
            player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME  * Game_FrameWork.frame_time) % 16
        if player.frame >= 15:
            player.isGameOver = True


    @staticmethod
    def draw(player):
        if not player.isGameOver:
            player.death_image.clip_draw(int(player.frame) * 172, 0, 172, 106, player.x, player.y)

next_state_table = {
    IdleState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, SPACE: JumpState, X: IdleState, HIT: HitState, DEATH: DeathState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, NONE: IdleState, SPACE: JumpState, X: RunState, HIT: HitState, DEATH: DeathState},
    JumpState: {RIGHT_UP: JumpState, LEFT_UP: JumpState, RIGHT_DOWN: JumpState, LEFT_DOWN: JumpState, GROUND_Idle : IdleState, Ground_Run : RunState, X: JumpState, HIT: HitState, DEATH: DeathState},
    HitState: {GROUND_Idle: IdleState, Ground_Run: RunState, DEATH: DeathState},
    DeathState: {NONE: DeathState}
}

class Player:

    def __init__(self):
        self.x, self.y = 400, 90
        self.idle_image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\Player\\Idle\\Player_Idle.png")
        self.run_image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\Player\\Run\\Player_Run.png")
        self.jump_image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\Player\\Jump\\Player_Jump.png")
        self.hit_image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\Player\\Hit\\Player_Hit.png")
        self.death_image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\Player\\Death\\Player_Death.png")
        self.dir = 1
        self.opacity = 1
        self.hp = 3
        self.FrameIncrease = True
        self.isJump = False
        self.isHit = False
        self.isDeath = False
        self.isGameOver = False
        self.ready_time = get_time()
        self.velocity = False
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def fire_bullet(self, offset_Position_X,offset_Position_Y):
        if self.dir != 0:
            player_bullet = Player_Bullet(self.x + offset_Position_X, self.y + offset_Position_Y, self.dir*10)
            Game_World.add_object(player_bullet, 1)

    def get_bb(self, offset_left, offset_bottom, offset_right, offset_top):
        return (self.x - offset_left), (self.y - offset_bottom), (self.x + offset_right), (self.y + offset_top)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if get_time() - self.ready_time < 4.5:
            return

        if len(self.event_que) > 0:
            event = self.event_que.pop()
            if (event in next_state_table[self.cur_state]) == False:
                return
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if get_time() - self.ready_time < 4.5:
            return
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def Hit(self):
        self.add_event(HIT)