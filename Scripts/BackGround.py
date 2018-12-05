from pico2d import *

survival_font = load_font('ENCR10B.TTF', 30)

class BackGround:
    isReady = False
    isStart = False
    def __init__(self):
        self.image = load_image('C:\\GitHub\\2DGP_TermProject\\Resources\\BackGround\\background.png')
        self.ready_image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\UI\\ready.png")
        self.start_image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\UI\\start.png")
        self.victory_image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\UI\\Knockout.png")
        self.game_over_image = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\UI\\game_over.png")
        self.ready_music = load_wav("C:\\GitHub\\2DGP_TermProject\\Resources\\Sound\\ready_music.wav")
        self.start_music = load_wav("C:\\GitHub\\2DGP_TermProject\\Resources\\Sound\\start_music.wav")
        self.victory_music = load_wav("C:\\GitHub\\2DGP_TermProject\\Resources\\Sound\\knockout.WAV")
        self.background_music = load_music("C:\\GitHub\\2DGP_TermProject\\Resources\\Sound\\Background_music.mp3")

        self.isGameOver = False
        self.isVictory = False
        self.isVictory_sound = False
        self.victory_music.set_volume(100)
        self.start_time = 0
        self.survival_time = 0

    def update(self):
        global isReady, isStart,ready_timer
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
                self.start_time = get_time()
                self.isStart = True
        if self.isVictory_sound:
            self.victory_music.play()
            self.isVictory_sound = False

    def draw(self):
        global isReady, isStart, ready_timer, survival_font
        self.image.draw(950, 400)
        if not self.isStart:
            self.ready_image.draw(950,400)
        if get_time() - ready_timer > 3 and get_time() - ready_timer < 4:
            self.start_image.draw(950,500)
        if self.isVictory:
            self.victory_image.draw(950,400)
        if self.isStart:
            self.survival_time = get_time() - self.start_time
            survival_font.draw(900, 700, 'Time: %.2f' % self.survival_time, (255, 255, 0))
        if self.isGameOver:
            self.game_over_image.draw(950, 400)