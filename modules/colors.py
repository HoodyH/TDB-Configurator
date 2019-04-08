from modules.graphics import *

def color(name):
    switcher = {
        "black": color_rgb(0, 0, 0),
        "dark_grey": color_rgb(56, 56, 56),
        "white": color_rgb(255, 255, 255),
        "orange": color_rgb(255, 138, 56)
    }
    return switcher.get(name, color_rgb(255, 255, 255))