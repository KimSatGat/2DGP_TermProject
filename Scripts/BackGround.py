from pico2d import *

class BackGround:
    def __init__(self):
        self.image = load_image('C:\\GitHub\\2DGP_TermProject\\Resources\\BackGround\\background.png')
        self.ready_image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\UI\\ready.png")
        self.start_image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\UI\\start.png")
        self.ready_music = load_wav("C:\\GitHub\\2DGP_TermProject\\Resources\\Sound\\ready_music.wav")
        self.start_music = load_wav("C:\\GitHub\\2DGP_TermProject\\Resources\\Sound\\start_music.wav")
        self.background_music = load_music("C:\\GitHub\\2DGP_TermProject\\Resources\\Sound\\Background_music.mp3")
        self.isReady = False
        self.isStart = False



    def update(self):
        global ready_timer
        if not self.isReady:
            ready_timer = get_time()
            self.ready_music.set_volume(120)
            self.ready_music.play()
            self.background_music.set_volume(32)
            self.background_music.repeat_play()
            self.isReady = True
        if get_time() - ready_timer > 3:
            if not self.isStart:
                self.start_music.set_volume(120)
                self.start_music.play()
                self.isStart = True

    def draw(self):
        global ready_timer
        self.image.draw(950, 400)
        if not self.isStart:
            self.ready_image.draw(950,400)
        if get_time() - ready_timer > 3 and get_time() - ready_timer < 4:
            self.start_image.draw(950,500)
