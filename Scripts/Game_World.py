
# layer 0: Background Objects
# layer 1: Foreground Objects
# layer 2: Player Bullets
objects = [[],[],[]]


def add_object(o, layer):
    objects[layer].append(o)


def remove_object(o):
    for i in range(0,2):
        if o in objects[i]:
            objects[i].remove(o)
            del o


def clear():
    for o in all_objects():
        del o
    objects.clear()


def all_objects():
    for i in range(2):
        for o in objects[i]:
            yield o

def all_bullets():
    for i in objects[2]:
        yield i


