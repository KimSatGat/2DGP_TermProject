from pico2d import *
import Game_World
import Game_FrameWork


# Player_Bullet Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Player_Bullet:
    image = None
    weapon_sound = None
    explosion_sound = None
    def __init__(self,x,y,velocity):
        if Player_Bullet.image == None:
            Player_Bullet.image = load_image('C:\\GitHub\\2DGP_TermProject\\Resources\\Player\\Bullet\\Player_Bullet.png')
        if Player_Bullet.weapon_sound == None:
            Player_Bullet.weapon_sound = load_wav("C:\\GitHub\\2DGP_TermProject\\Resources\\Sound\\player_weapon.WAV")
        if Player_Bullet.explosion_sound == None:
            Player_Bullet.explosion_sound = load_wav("C:\\GitHub\\2DGP_TermProject\\Resources\\Sound\\player_weapon_explosion.WAV")
        self.x, self.y, self.velocity = x, y, velocity
        self.frame = 0
        self.damage = 10
        self.ExplosionTime = None
        self.isExplosion = False
        self.weapon_sound.set_volume(32)
        self.explosion_sound.set_volume(32)
        self.weapon_sound.play()

    def draw(self):
        if self.velocity > 0:
            self.image.clip_draw(int(self.frame) * 80, 51, 80, 51, self.x, self.y)

        elif self.velocity < 0:
            self.image.clip_draw(int(self.frame) * 80, 0, 80, 51, self.x, self.y)

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
        self.isExplosion = True
        self.image = load_image('C:\\GitHub\\2DGP_TermProject\\Resources\\Player\\Bullet\\Player_BulletExplosion.png')
        self.explosion_sound.play()
        self.velocity = 0