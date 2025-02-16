import pygame
import random
import math
from character import Character
from utilities import check_collision
from battle import Battle


# Function to create multiple enemies
def create_enemies(num_enemies, player_x, player_y, x_id, y_id, WIDTH, HEIGHT):
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
                              level=random.randint(3, 7),
                              hp=random.randint(30, 60),
                              mp=random.randint(5, 20),
                              atk=random.randint(10, 20),
                              dfn=random.randint(5, 15),
                              spd=random.randint(5, 15),
                              inventory={},
                              folder_paths=[fR".\timefantasy_characters\timefantasy_characters\frames\chara\chara{x_id}_{y_id}", fR".\tf_svbattle\singleframes\set{x_id}\{y_id}"]
                              )
        new_enemy.sprite.set_animation(state='Idle')
        enemies.append({"character": new_enemy, "x": enemy_x, "y": enemy_y})
    return enemies



pygame.init()
# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Character Animation")

clock = pygame.time.Clock()
E = []
for x in range(2, 6):
    for y in range(1, 9):
        enemies = create_enemies(1, 0, 0, x, y, WIDTH, HEIGHT)
        E.append(enemies)


running = True
while running:
    screen.fill((255, 255, 255))  # Clear screen

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw enemies
    for enemies in E:
        for enemy in enemies:
            enemy["character"].sprite.update_frame()
            enemy["character"].sprite.draw(screen, enemy["x"], enemy["y"])
    
    pygame.display.update()
    clock.tick(30)  # Control animation speed (10 FPS)

pygame.quit()