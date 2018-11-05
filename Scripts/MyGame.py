import Game_FrameWork
import pico2d
pico2d.open_canvas(1600, 600)

import Main_State


Game_FrameWork.run(Main_State)
pico2d.close_canvas()