from pico2d import *

class BackGround:
    def __init__(self):
        self.image = load_image('C:\\GitHub\\2DGP_TermProject\\Resources\\BackGround\\background.png')
        self.ready_music = load_wav("C:\\GitHub\\2DGP_TermProject\\Resources\\Sound\\ready_music.wav")
        self.start_music = load_wav("C:\\GitHub\\2DGP_TermProject\\Resources\\Sound\\start_music.wav")
        self.background_music = load_music("C:\\GitHub\\2DGP_TermProject\\Resources\\Sound\\Background_music.mp3")
        self.isReady = False
        self.isStart = False
        #self.start_music.set_volume(64)
        #self.start_music.play()

        #   self.background_music.set_volume(64)
        #self.background_music.repeat_play()

    def update(self):
        global ready_timer

        if not self.isReady:
            ready_timer = get_time()
            self.ready_music.set_volume(64)
            self.ready_music.play()
            self.isReady = True

        if get_time() - ready_timer > 3:
            if not self.isStart:
                self.start_music.set_volume(64)
                self.start_music.play()
                self.isStart = True


    def draw(self):
        self.image.draw(950, 400)
