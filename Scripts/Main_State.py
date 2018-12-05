import random
import json
import os

from pico2d import *
import Game_FrameWork
import Game_World
import Rank_State
import Start_State

from Player import Player
from Player_Bullet import Player_Bullet
from Moe_Tato import MoeTato
from Moe_Tato_Bullet import Moe_Tato_Bullet
from BackGround import BackGround

name = "MainState"
player = None
moetato = None
invincibility_timer = None
isInvincibility = False
game_over_time = None
complete_time = None
rank = None

def enter():
    global player, moetato, background, rank
    player = Player()
    moetato = MoeTato()
    background = BackGround()
    Game_World.add_object(background, 0)
    Game_World.add_object(player, 1)
    Game_World.add_object(moetato, 1)

    with open('rank_data.json', 'rt') as f:
        rank = json.load(f)

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
    global  player, moetato, invincibility_timer, game_over_time, complete_time, background
    if game_over_time != None:
        if get_time() - game_over_time > 1.5:
            Game_FrameWork.change_state(Rank_State)
    if complete_time != None:
        if get_time() - complete_time > 1.5:
            Game_FrameWork.change_state(Rank_State)
    for game_object in Game_World.all_objects():
        game_object.update()
        if isinstance(game_object, Player_Bullet):
            if game_object.velocity > 0:
                if collide(game_object.get_bb_dir_right(), moetato.get_bb_hand()) or collide(game_object.get_bb_dir_right(),moetato.get_bb_body1()) or collide(game_object.get_bb_dir_right(), moetato.get_bb_body2()):
                    if not game_object.isExplosion:
                        moetato.hp = moetato.hp - 1
                        game_object.explosion()
                        if moetato.hp <= 0 and not moetato.isDeath and not player.isDeath:
                            moetato.isDeath = True
                            background.isVictory_sound = True
                            background.isVictory = True
                            rank.append(round(background.survival_time, 2))
                            rank.sort()
                            with open('rank_data.json', 'wt') as f:
                                json.dump(rank, f)
                            if complete_time == None:
                                complete_time = get_time()
            else:
                if collide(game_object.get_bb_dir_left(), moetato.get_bb_hand()) or collide(game_object.get_bb_dir_left(),moetato.get_bb_body1()) or collide(game_object.get_bb_dir_left(), moetato.get_bb_body2()):
                    if not game_object.isExplosion:
                        moetato.hp = moetato.hp - 1
                        game_object.explosion()
                        if moetato.hp <= 0:
                            moetato.isDeath = True
                            background.isVictory_sound = True
                            background.isVictory = True
                            rank.append(round(background.survival_time, 2))
                            rank.sort()
                            with open('rank_data.json', 'wt') as f:
                                json.dump(rank, f)
                            if complete_time == None:
                                complete_time = get_time()
        if isinstance(game_object, Moe_Tato_Bullet):
            if moetato.isDeath:
                Game_World.remove_object(game_object)
            if not player.isHit and collide(game_object.get_bb(), player.get_bb(55, 80, 60, 75)):
                if not game_object.isExplosion:
                    player.hp = player.hp - 1
                    if player.hp <= 0:
                        if game_over_time == None:
                            game_over_time = get_time()
                            player.isDeath = True
                            background.isGameOver = True
                    else:
                        invincibility_timer = get_time()
                        game_object.explosion()
                        player.Hit()


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