from pico2d import *
import Game_World
import Game_FrameWork


# Player_Bullet Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Moe_Tato_Bullet:
    image = None

    def __init__(self,x,y,velocity):
        if Moe_Tato_Bullet.image == None:
            Moe_Tato_Bullet.image = load_image('C:\\GitHub\\2DGP_TermProject\\Resources\\MoeTato\\Bullet.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.frame = 0
        self.damage = 10
        self.ExplosionTime = None
        self.isExplosion = False

    def draw(self):
        self.image.clip_draw(int(self.frame) * 131, 0, 131, 139, self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x -= self.velocity
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % 8
        if self.x > 1900 - 25:
            Game_World.remove_object(self)

    def get_bb(self):
        return (self.x - 50), (self.y - 50), (self.x + 50), (self.y + 50)

    def explosion(self):
        self.image = load_image('C:\\GitHub\\2DGP_TermProject\Resources\\MoeTato\\Projectile1-Pop.png')
        self.isExplosion = True
        self.velocity = 0