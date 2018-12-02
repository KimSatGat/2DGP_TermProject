from pico2d import *

class BackGround:
    def __init__(self):
        self.image = load_image('C:\\GitHub\\2DGP_TermProject\\Resources\\BackGround\\background.png')
        self.background_music = load_music("C:\\GitHub\\2DGP_TermProject\\Resources\\Sound\\Background_music.mp3")
        self.background_music.set_volume(64)
        self.background_music.repeat_play()

    def update(self):
        pass

    def draw(self):
        self.image.draw(950, 400)
