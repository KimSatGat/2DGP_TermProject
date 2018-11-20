from pico2d import *
import Game_World
import Game_FrameWork

# Player_Bullet Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Player_Bullet:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Player_Bullet.image == None:
            Player_Bullet.image = load_image('C:\\GitHub\\2DGP_TermProject\\Resources\\Player\\Bullet\\Player_Bullet.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.frame = 0


    def draw(self):
        if self.velocity > 0:
            self.image.clip_draw(int(self.frame) * 80, 51, 80, 51, self.x, self.y)
            draw_rectangle(*self.get_bb(30, 30, 35, 30))
        else:
            self.image.clip_draw(int(self.frame) * 80, 0, 80, 51, self.x, self.y)
            draw_rectangle(*self.get_bb(40, 30, 30, 30))

    def update(self):
        self.x += self.velocity
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % 4

        if self.x < 25 or self.x > 1900 - 25:
            Game_World.remove_object(self)

    def get_bb(self, offset_left, offset_bottom, offset_right, offset_top):
        return (self.x - offset_left), (self.y - offset_bottom), (self.x + offset_right), (self.y + offset_top)