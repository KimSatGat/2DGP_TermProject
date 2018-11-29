import random
import json
import os

from pico2d import *
import Game_FrameWork
import Game_World


from Player import Player
from Moe_Tato import MoeTato
from BackGround import BackGround

name = "MainState"
player = None
moetato = None

def enter():
    global player, moetato
    player = Player()
    moetato = MoeTato()
    background = BackGround()
    Game_World.add_object(background, 0)
    Game_World.add_object(player, 1)
    Game_World.add_object(moetato, 1)

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
    global  player, moetato
    for game_object in Game_World.all_objects():
        game_object.update()

    #미사일 충돌 체크
    for bullets in Game_World.all_bullets():
        if bullets.velocity > 0:
            if collide(bullets.get_bb_dir_right(), moetato.get_bb_hand()) or  collide(bullets.get_bb_dir_right(), moetato.get_bb_body1()) or  collide(bullets.get_bb_dir_right(), moetato.get_bb_body2()):
                bullets.explosion()
        else:
            if collide(bullets.get_bb_dir_left(), moetato.get_bb_hand()) or  collide(bullets.get_bb_dir_left(), moetato.get_bb_body1()) or  collide(bullets.get_bb_dir_left(), moetato.get_bb_body2()):
                bullets.explosion()

def draw():
    clear_canvas()
    for game_object in Game_World.all_objects():
        game_object.draw()
    update_canvas()

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a
    left_b, bottom_b, right_b, top_b = b

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False

    return True