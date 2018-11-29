from pico2d import *
import Game_World
import Game_FrameWork


# Player_Bullet Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Player_Bullet:
    image = None

    def __init__(self,x,y,velocity):
        if Player_Bullet.image == None:
            Player_Bullet.image = load_image('C:\\GitHub\\2DGP_TermProject\\Resources\\Player\\Bullet\\Player_Bullet.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.frame = 0
        self.damage = 10
        self.ExplosionTime = None
        self.isExplosion = False

    def draw(self):
        if self.velocity > 0:
            self.image.clip_draw(int(self.frame) * 80, 51, 80, 51, self.x, self.y)
            draw_rectangle(*self.get_bb_dir_right())
        elif self.velocity < 0:
            self.image.clip_draw(int(self.frame) * 80, 0, 80, 51, self.x, self.y)
            draw_rectangle(*self.get_bb_dir_left())
        else:
            self.image.clip_draw(int(self.frame) * 64, 0, 64, 60, self.x, self.y)

    def update(self):
        self.x += self.velocity
        if self.isExplosion:
            if self.ExplosionTime == None:
                self.ExplosionTime = get_time()
            if get_time() - self.ExplosionTime >= 0.2:
                Game_World.remove_object(self)
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % 7
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % 4

        if self.x < 25 or self.x > 1900 - 25:
            Game_World.remove_object(self)

    def get_bb_dir_right(self):
        return (self.x - 30), (self.y - 30), (self.x + 35), (self.y + 30)
    def get_bb_dir_left(self):
        return (self.x - 40), (self.y - 30), (self.x + 30), (self.y + 30)

    def explosion(self):
        self.image = load_image('C:\\GitHub\\2DGP_TermProject\\Resources\\Player\\Bullet\\Player_BulletExplosion.png')
        self.isExplosion = True
        self.velocity = 0