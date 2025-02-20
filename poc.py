import json
import numpy as np

path = ".\Backgrounds\TownMapTest.json"

with open(path, 'r') as file:
    data = json.load(file)


Positions = []
total_x = data["map_width"]
total_y = data["map_height"]
scale_factor = 2

Positions = np.zeros((total_x, total_y))


for layer in data["layers"]:
    if layer["name"] == "Top":
        for pos in layer["positions"]:
            x = pos["x"]
            y = pos["y"]
            Positions[x][y] = 1

print(Positions)
Positions = np.tile(Positions, (scale_factor, scale_factor))
print(Positions)