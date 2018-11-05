import random
import json
import os

from pico2d import *
import Game_FrameWork
import Game_World

from Player import Player
#from grass import Grass



name = "MainState"

player = None

def enter():
    global player
    player = Player()
    #grass = Grass()
    #Game_World.add_object(grass, 0)
    Game_World.add_object(player, 1)


def exit():
    Game_World.clear()

def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_FrameWork.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                Game_FrameWork.quit()
        else:
            player.handle_event(event)


def update():
    for game_object in Game_World.all_objects():
        game_object.update()
    delay(0.01)


def draw():
    clear_canvas()
    for game_object in Game_World.all_objects():
        game_object.draw()
    update_canvas()






