running = None
stack = None


def change_state(state):
    global stack
    if (len(stack) > 0):
        # execute the current state's exit function
        stack[-1].exit()
        # remove the current state
        stack.pop()
    stack.append(state)
    state.enter()

def push_state(state):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(state)
    state.enter()

def pop_state():
    global stack
    if (len(stack) > 0):
        # execute the current state's exit function
        stack[-1].exit()
        # remove the current state
        stack.pop()

    # execute resume function of the previous state
    if (len(stack) > 0):
        stack[-1].resume()

def quit():
    global running
    running = False

import time
frame_time = 0.0

def run(start_state):
    global running, stack
    running = True
    stack = [start_state]
    start_state.enter()
    global frame_time
    current_time = time.time()

    while (running):
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
        frame_time = time.time() - current_time
        current_time += frame_time

    # repeatedly delete the top of the stack
    while (len(stack) > 0):
        stack[-1].exit()
        stack.pop()

