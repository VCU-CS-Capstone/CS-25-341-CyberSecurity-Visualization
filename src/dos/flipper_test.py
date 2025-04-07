import time
import flipperzero

def draw_action():
    flipperzero.canvas_set_color(flipperzero.CANVAS_BLACK)
    flipperzero.canvas_set_text(40, 22, "Flipper Python")
    flipperzero.canvas_set_text(40, 44, "Hello World")
    flipperzero.canvas_update()

draw_action()

for _ in range(1, 5):
    time.sleep(1)