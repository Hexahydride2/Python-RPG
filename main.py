import pygame
import sys
import random
import math
from character import Character
from battle import check_collision, Battle


# Function to create multiple enemies
def create_enemies(num_enemies, player_x, player_y):
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
                              sprite_paths={
                                  "Walk": "./Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Orc/Orc/Orc-Walk.png",
                                  "Idle": "./Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Orc/Orc/Orc-Idle.png",
                                  "Attack01": "./Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Orc/Orc/Orc-Attack01.png",
                                  "Attack02": "./Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Orc/Orc/Orc-Attack02.png",
                                  "Hurt": "./Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Orc/Orc/Orc-Hurt.png",
                                  "Death": "./Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Orc/Orc/Orc-Death.png"
                              }, num_frames_dict=num_frames_dict)
        new_enemy.sprite.set_animation(state='Idle')
        enemies.append({"character": new_enemy, "x": enemy_x, "y": enemy_y})
    return enemies


# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dragon Quest-like RPG")
num_frames_dict = {'Attack01': 6, 'Attack02': 6, 'Attack03': 9, 'Death': 4, 'Hurt': 4, 'Idle': 6, 'Walk': 8}

# Load Player and NPC with Multiple Animations
player = Character(name="Hero",
                   level=10,
                   hp=100,
                   mp=50,
                   atk=30,
                   dfn=20,
                   spd=30,
                   inventory={"Potion": 2, "Mana Crystal": 3}, 
                   sprite_paths={
    "Walk": "./Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Soldier/Soldier/Soldier-Walk.png",
    "Idle": "./Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Soldier/Soldier/Soldier-Idle.png",
    "Attack01": "./Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Soldier/Soldier/Soldier-Attack01.png",
    "Attack02": "./Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Soldier/Soldier/Soldier-Attack02.png",
    "Attack03": "./Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Soldier/Soldier/Soldier-Attack03.png",
    "Hurt": "./Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Soldier/Soldier/Soldier-Hurt.png",
    "Death": "./Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Soldier/Soldier/Soldier-Death.png"
}, num_frames_dict=num_frames_dict)


# Player settings
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5
current_frame = 0
is_flipped = False  # Variable to track if sprite is flipped


# Generate enemies
enemies = create_enemies(5, player_x, player_y)  # Set the number of enemies

# Battle window settings
battle_screen = False  # Track whether battle is in progress
current_enemy = None

clock = pygame.time.Clock()



# Main game loop
running = True
last_direction = None  # Track the last direction the player moved in
while running:
    screen.fill((255, 255, 255))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if battle_screen and current_enemy:
        battle = Battle(screen, player, current_enemy["character"], background_image=".\craftpix-net-270096-free-forest-battle-backgrounds\PNG\game_background_4\game_background_4.png")
        result = battle.run()

        if result == "win":
            player.sprite.set_animation('Walk')
            enemies.remove(current_enemy)
            battle_screen = False  # Exit battle screen
            player_x += 60  # Move player away to prevent instant re-entry

        elif result == "lose":
            player.sprite.set_animation('Walk')
            current_enemy.sprite.set_animation('Idle')
            battle_screen = False  # Exit battle screen
            player_x += 60  # Move player away to prevent instant re-entry

        elif result == "escape":
            #player.sprite.set_animation('Walk')
            #current_enemy["character"].sprite.set_animation('Idle')
            battle_screen = False  # Exit battle screen
            player_x += 60  # Move player away to prevent instant re-entry


    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_y -= player_speed
        last_direction = 'UP'

    if keys[pygame.K_DOWN]:
        player_y += player_speed
        last_direction = 'DOWN'

    if keys[pygame.K_LEFT]:
        player_x -= player_speed
        if last_direction != 'LEFT':  # Only flip when changing direction
            player.sprite.is_flipped = True  # Flip the sprite when moving left
        last_direction = 'LEFT'

    if keys[pygame.K_RIGHT]:
        player_x += player_speed
        if last_direction != 'RIGHT':  # Only flip when changing direction
            player.sprite.is_flipped = False  # Reset the flip when moving right
        last_direction = 'RIGHT'

    print(player.sprite.animations)
    # Check for collisions with enemies
    for enemy in enemies:
        if check_collision(player_x, player_y, enemy["x"], enemy["y"]):
            battle_screen = True
            current_enemy = enemy  # Store current enemy for battle
            
            break  # Only trigger one battle at a time
    

    # Draw player
    player.sprite.update_frame()
    player.sprite.draw(screen, player_x, player_y)
    
    # Draw enemies
    for enemy in enemies:
        enemy["character"].sprite.update_frame()
        enemy["character"].sprite.draw(screen, enemy["x"], enemy["y"])
    
    pygame.display.update()
    clock.tick(30)  # Set FPS

# Quit Pygame
pygame.quit()
sys.exit()
