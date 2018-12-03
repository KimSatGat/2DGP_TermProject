from pico2d import *
import Game_FrameWork
import Main_State

name = "Start_State"

menu = None

def enter():
    global menu
    menu = load_image("C:\\GitHub\\2DGP_TermProject\\Resources\\UI\\start_image.jpg")
    hide_cursor()
    hide_lattice()

def exit():
    global menu
    del menu

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_FrameWork.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            Game_FrameWork.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            Game_FrameWork.change_state(Main_State)

def draw():
    clear_canvas()
    menu.draw(get_canvas_width()//2, get_canvas_height()//2)
    update_canvas()

def update():
    pass