import re
import math
import random

# To separate "walk1" into "walk" and "1",for example, 
def split_animation_name(name):
    
    match = re.match(r"(.+)\((\d+)\)$", name)  # Match any text followed by numbers at the end
    if match:
        return match.group(1), match.group(2)  # "walk", "1"
    return name, "1"  # Return original name if no match

# Function to check if player collides with NPC
def check_collision(player_x, player_y, npc_x, npc_y, threshold=60):
    distance = math.sqrt((player_x - npc_x) ** 2 + (player_y - npc_y) ** 2)
    return distance < threshold
