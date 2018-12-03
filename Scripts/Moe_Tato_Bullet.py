from pico2d import *
import Game_World
import Game_FrameWork

# Player_Bullet Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Moe_Tato_Bullet:
    image = None
    weapon_sound = None
    explosion_sound = None

    def __init__(self,x,y,velocity):
        if Moe_Tato_Bullet.image == None:
            Moe_Tato_Bullet.image = load_image('C:\\GitHub\\2DGP_TermProject\\Resources\\MoeTato\\Bullet.png')
        if Moe_Tato_Bullet.weapon_sound == None:
            Moe_Tato_Bullet.weapon_sound = load_wav("C:\\GitHub\\2DGP_TermProject\\Resources\\Sound\\moetato_weapon.WAV")
        if Moe_Tato_Bullet.explosion_sound == None:
            Moe_Tato_Bullet.explosion_sound = load_wav("C:\\GitHub\\2DGP_TermProject\\Resources\\Sound\\moetato_weapon_explosion.WAV")
        self.x, self.y, self.velocity = x, y, velocity
        self.frame = 0
        self.damage = 1
        self.ExplosionTime = None
        self.isExplosion = False
        self.weapon_sound.set_volume(100)
        self.explosion_sound.set_volume(100)
        self.weapon_sound.play()

    def draw(self):
        if self.velocity == 0:
            self.image.clip_draw(int(self.frame) * 278, 0, 278, 253, self.x, self.y)
        else:
            self.image.clip_draw(int(self.frame) * 131, 0, 131, 139, self.x, self.y)
            draw_rectangle(*self.get_bb())

    def update(self):

        self.x -= self.velocity
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % 8

        if self.isExplosion:
            if self.ExplosionTime == None:
                self.ExplosionTime = get_time()
            if get_time() - self.ExplosionTime >= 0.2:
                Game_World.remove_object(self)
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % 8

        if self.x > 1900 - 25:
            Game_World.remove_object(self)

    def get_bb(self):
        return (self.x - 45), (self.y - 50), (self.x + 50), (self.y + 50)

    def explosion(self):
        self.isExplosion = True
        self.image = load_image('C:\\GitHub\\2DGP_TermProject\Resources\\MoeTato\\Bullet_Explosion.png')
        self.explosion_sound.play()
        self.velocity = 0