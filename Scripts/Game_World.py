
# layer 0: Background Objects
# layer 1: Foreground Objects
# layer 2: Player Bullets
# layer 3: MoeTato Bullets
objects = [[],[],[],[]]

def add_object(o, layer):
    objects[layer].append(o)

def remove_object(o):
    for i in range(len(objects)):
        if o in objects[i]:
            objects[i].remove(o)
            del o

def clear():
    for o in all_objects():
        del o
    objects.clear()

def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o

def all_player_bullets():
    for o in objects[2]:
        yield o

def all_moetato_bullets():
    for o in objects[3]:
        yield o



