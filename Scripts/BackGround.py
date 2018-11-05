from pico2d import *

class BackGround:
    def __init__(self):
        self.image = load_image('C:\\GitHub\\2DGP_TermProject\\Resources\\BackGround\\background.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(950, 400)
