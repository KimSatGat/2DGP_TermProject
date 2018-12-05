import Game_FrameWork
from pico2d import *
import json

name = "RankState"

font = None
rank_font = None
final_rank = None

def enter():
    global font, rank_font
    global final_rank
    with open('rank_data.json', 'rt') as f:
        final_rank = json.load(f)
    rank_font = load_font('ENCR10B.TTF', 40)
    font = load_font('ENCR10B.TTF', 20)


def handle_events():
    events = pico2d.get_events()
    for event in events:
        if event.type == pico2d.SDL_QUIT:
            Game_FrameWork.quit()
        elif event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE:
            Game_FrameWork.quit()

def update():
    pass

def draw():
    global font, rank_font
    global final_rank
    pico2d.clear_canvas()
    rank_font.draw(600, 650, "RANK", (0, 0, 0))
    for a in range(0,5):
        font.draw(600, 600 - (a * 30),'#%d. ' % (a+1), (0, 0, 0))
        font.draw(660, 600 - (a * 30), '%.2f' % (final_rank[a]), (0, 0, 0))
    pico2d.update_canvas()

def exit():
    pass