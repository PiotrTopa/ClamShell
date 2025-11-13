from openscad import *
import json
import os 
import sys
from collections.abc import Mapping

BORDER = 5
BASE = 15
MX_WIDTH = 14
MX_HEIGHT = 14

def read_layout(path: str):
    with open(path) as f:
        layout = json.load(f)
    keys = [] 
    max_width = 0.0
    max_height = 0.0
    x = 0.0
    y = 0.0
    max_line_key_height = 1.0
    current_key_width = 1.0
    current_key_height = 1.0
    for row in layout:
        for item in row:
            if isinstance(item, Mapping):
                if 'w' in item:
                    current_key_width = item['w']
                if 'x' in item:
                    x += item['x']
            
            if isinstance(item, str):
                key = {
                    "x": x,
                    "y": y,
                    "width": current_key_width,
                    "height": current_key_height,
                    "labels": item
                }
                x += current_key_width
                max_line_key_height = max(max_line_key_height, current_key_height)
                current_key_width = 1.0
                current_key_height = 1.0
                keys.append(key)   
        y += max_line_key_height
        x = 0.0
        max_lin_key_height = 0.0
    return keys
            
layout = read_layout('D:\\Projects\\ClamShell\\keyboard\\layout\\keyboard-layout.json')

keyboard_width = 0.0
keyboard_height = 0.0
for key in layout:
    keyboard_width = max(keyboard_width, key["x"] + key["width"])
    keyboard_height = max(keyboard_height, key["y"] + key["height"])

plate = cube([(BASE * keyboard_width) + (2 * BORDER), (BASE * keyboard_height) + (2 * BORDER), 1], center=True)

start_x = -1 * (BASE * keyboard_width) / 2
start_y = 1 * (BASE * keyboard_height) / 2

for key in layout:
    key_x = BASE * key["x"]
    key_y = BASE * key["y"]
    key_center_x = BASE * (key["width"] / 2)
    key_center_y = BASE * (key["height"] / 2)
    plate -= cube([MX_WIDTH, MX_HEIGHT, 10], center=True) + [start_x + key_x + key_center_x, start_y - key_y - key_center_y, 0]
    
plate.show()