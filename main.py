import pygame
import random
import math
from character import Character, NPC
from utilities import check_collision, handle_npc_interaction, move_to_battle, create_enemies
from battle import Battle
from text_manager import TextManager


# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Character Animation")

screen, combined_map_surface, combined_map_width, combined_map_height, player_x, player_y = initialize_town(
    CELL_WIDTH, CELL_HEIGHT, "Backgrounds\TownMap.png"
)
# screen, combined_map_surface, combined_map_width, combined_map_height, player_x, player_y = initialize_town(
#     CELL_WIDTH, CELL_HEIGHT, MAP_ROWS, MAP_COLS, "Map-L.png", "Map-R.png")


# Animation variables
clock = pygame.time.Clock()
frame = 0
player_x, player_y = 100, 300  # Position of the character


# Battle window settings
battle_screen = False  # Track whether battle is in progress
current_enemy = None

# Initialize TextManager
text_manager = TextManager(screen)


playerID_x, playerID_y = 2, 1

player = Character(
                   name="Hero",
                   x=player_x,
                   y=player_y,
                   level=10,
                   hp=100,
                   mp=50,
                   atk=30,
                   dfn=20,
                   spd=30,
                   inventory={"Potion": 2, "Mana Crystal": 3}, 
                   folder_paths=[fR".\timefantasy_characters\timefantasy_characters\frames\chara\chara{playerID_x}_{playerID_y}", fR".\tf_svbattle\singleframes\set{playerID_x}\{playerID_y}"]
                   )

# Create enemies in the random location
enemies = create_enemies(num_enemies=2, player_x=player.x, player_y=player.y, x_id=5, y_id=8, WIDTH=WIDTH, HEIGHT=HEIGHT)
for enemy in enemies:
    enemy["character"].sprite.set_animation("down_stand")

# Create NPCs
npc1 = NPC("Old Man", ["Hello, traveler!", "The village is to the north.", "Be careful on your journey."], 400, 300, [R".\timefantasy_characters\timefantasy_characters\frames\npc\npc1_1"])
npc2 = NPC("Merchant", ["Welcome to my shop. I sell potions and weapons."], 200, 350, [R".\timefantasy_characters\timefantasy_characters\frames\npc\npc1_2"])

npcs = [npc1, npc2]


# Player settings
# player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5
current_frame = 0
is_flipped = False  # Variable to track if sprite is flipped


# Generate enemies
enemies = create_enemies(25, player_x, player_y, combined_map_surface, combined_map_width, combined_map_height)  # Set the number of enemies

# Battle window settings
battle_screen = False  # Track whether battle is in progress
current_enemy = None

clock = pygame.time.Clock()

# Start in the town area:


# Main game loop
running = True
while running:
    screen.fill((255, 255, 255))  # Clear screen

    # Event handling
    keys = pygame.key.get_pressed()  # Get currently pressed keys

    # Walking movement
    player.move(keys)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Go to battle window
    if battle_screen and current_enemy:
        enemies, battle_screen = move_to_battle(screen, player, enemies, current_enemy, battle_screen)

    # Handle NPC interaction
    handle_npc_interaction(player, npcs, text_manager, screen)

    # Check for collisions with enemies
    for enemy in enemies:
        if check_collision(player.x, player.y, enemy["x"], enemy["y"]):
            battle_screen = True
            current_enemy = enemy  # Store current enemy for battle
            break  # Only trigger one battle at a time

    # Draw NPCs
    for npc in npcs:
        npc.draw(screen)

    # Draw enemies
    for enemy in enemies:
        enemy["character"].sprite.update_frame()
        enemy["character"].sprite.draw(screen, enemy["x"], enemy["y"])

    # Display player
    player.sprite.is_flipped = False
    player.sprite.update_frame()
    player.sprite.draw(screen, player.x, player.y)

    # Update and draw text
    text_manager.update()
    text_manager.draw()

    pygame.display.update()
    clock.tick(30)  # Control animation speed (10 FPS)

pygame.quit()
