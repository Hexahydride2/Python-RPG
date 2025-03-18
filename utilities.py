import re
import math
import random
import pygame



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

def create_enemies(num_enemies, player_x, player_y, x_id, y_id, WIDTH, HEIGHT):
    from character import Character
    enemies = []
    min_distance_from_player = 60  # Minimum distance between player and enemy
    min_distance_between_enemies = 80  # Minimum distance between enemies

    while len(enemies) < num_enemies:
        enemy_x = random.randint(50, WIDTH - 50)
        enemy_y = random.randint(50, HEIGHT - 50)
        
        # Ensure enemy is at least 60 pixels away from the player
        distance_to_player = math.sqrt((enemy_x - player_x) ** 2 + (enemy_y - player_y) ** 2)
        if distance_to_player < min_distance_from_player:
            continue  # Skip this position and try again
        
        # Ensure enemy does not overlap with other enemies
        too_close = False
        for enemy in enemies:
            distance_to_enemy = math.sqrt((enemy_x - enemy["x"]) ** 2 + (enemy_y - enemy["y"]) ** 2)
            if distance_to_enemy < min_distance_between_enemies:
                too_close = True
                break  # No need to check further

        if too_close:
            continue  # Skip this position and try again

        # Create new enemy if all conditions are met
        new_enemy = Character(name="Orc",
                              x=enemy_x,
                              y=enemy_y,
                              level=random.randint(3, 7),
                              hp=random.randint(30, 60),
                              mp=random.randint(50, 100),
                              atk=random.randint(30, 50),
                              dfn=random.randint(5, 15),
                              spd=random.randint(5, 15),
                              inventory={},
                              folder_paths=[fR".\timefantasy_characters\timefantasy_characters\frames\chara\chara{x_id}_{y_id}", fR".\tf_svbattle\singleframes\set{x_id}\{y_id}"]
                              )
        new_enemy.sprite.set_animation(state='Idle')
        enemies.append({"character": new_enemy, "x": enemy_x, "y": enemy_y})
    return enemies


def add_menu(menu, events):
    """Create and manage the Menu instance within a single function."""
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:  # Open/close menu with "M"
                menu.toggle()
            else:
                menu.handle_input(event)

    menu.draw()  # Draw the menu if active

class MusicManager:
    def __init__(self):
        self.current_theme = None
        self.previous_theme = None

    def change_theme(self, theme_file):
        self.previous_theme = self.current_theme
        self.current_theme = theme_file
        pygame.mixer.music.stop()
        pygame.mixer.music.load(theme_file)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    def revert_theme(self):
        if self.previous_theme:
            self.change_theme(self.previous_theme)
        else:
            pygame.mixer.music.stop()

music_manager = MusicManager()

def change_theme(theme_file):
    music_manager.change_theme(theme_file)

def revert_theme():
    music_manager.revert_theme()