import pygame
import random
import math
from character import Character, NPC
from utilities import check_collision, handle_npc_interaction, move_to_battle, create_enemies
from battle import Battle
from text_manager import TextManager
from Draw import initialize_town, initialize_screen, initialize_main_menu, update_camera_and_draw, check_map_transition, change_theme
import sys
from items import items_list


# Initialize Pygame
pygame.init()
# initialize_main_menu()

# Now spawn in the town.
CELL_WIDTH, CELL_HEIGHT = 800, 600
screen, combined_map_surface, combined_map_width, combined_map_height, player_x, player_y = initialize_town(
    CELL_WIDTH, CELL_HEIGHT, "Backgrounds/TownMap.png"
)

# Animation and game variables.
clock = pygame.time.Clock()
text_manager = TextManager(screen)
playerID_x, playerID_y = 5, 1

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
    folder_paths=[fR".\timefantasy_characters\timefantasy_characters\frames\chara\chara{playerID_x}_{playerID_y}",
                  fR".\tf_svbattle\singleframes\set{playerID_x}\{playerID_y}"]
)

# Create enemies in a random location (utilizing your create_enemies function).
enemies = create_enemies(num_enemies=10, player_x=player.x, player_y=player.y, x_id=5, y_id=8, WIDTH=CELL_WIDTH, HEIGHT=CELL_HEIGHT)
for enemy in enemies:
    enemy["character"].sprite.set_animation("down_stand")

# Create NPCs.
npc1 = NPC("Old Man", ["Hello, traveler!", "The village is to the north.", "Be careful on your journey."], 1024, 1900,
           [R".\timefantasy_characters\timefantasy_characters\frames\npc\npc1_1"])
npc2 = NPC("Shopkeeper", ["Welcome to my shop!  I sell potions and weapons."], 1024, 1700,
           [R".\timefantasy_characters\timefantasy_characters\frames\npc\npc1_2"], items_list())

npcs = [npc1, npc2]

# Player movement settings.
player_speed = 5
battle_screen = False  # Track battle state.
shop_active = False # Track shop state
current_enemy = None
current_npc = None

# Main game loop.
running = True
while running:
    
    screen.fill((255, 255, 255))  # Clear screen.

     # Go to battle window
    if battle_screen and current_enemy:
        enemies, battle_screen = move_to_battle(screen, player, enemies, current_enemy, battle_screen)

    # print(player.x, player.y)
    prev_x, prev_y = player.x, player.y
    keys = pygame.key.get_pressed()
    player.move(keys)  # Assumes your Character class has a move() method.
    # Draw NPCs
    prev_pos = (player.x, player.y)
    transition = check_map_transition(player, combined_map_surface, combined_map_width, combined_map_height, CELL_WIDTH, CELL_HEIGHT, prev_pos)
    if transition:
        screen, combined_map_surface, combined_map_width, combined_map_height, player.x, player.y = transition

    # Handle interactions with NPCs.
    camera_rect = update_camera_and_draw(player, player.x, player.y, screen, combined_map_surface,
                                           combined_map_width, combined_map_height, CELL_WIDTH, CELL_HEIGHT)
    # Draw enemies.
    for enemy in enemies:
        enemy["character"].sprite.update_frame()
        enemy_draw_x = enemy["x"] - camera_rect.x - (enemy["character"].sprite.sprite_shape[enemy["character"].sprite.current_animation]["width"] * enemy["character"].sprite.scale_factor) // 2
        enemy_draw_y = enemy["y"] - camera_rect.y - (enemy["character"].sprite.sprite_shape[enemy["character"].sprite.current_animation]["height"] * enemy["character"].sprite.scale_factor) // 2
        enemy["character"].sprite.draw(screen, enemy_draw_x, enemy_draw_y)
    
    for enemy in enemies:
        if check_collision(player.x, player.y, enemy["x"], enemy["y"]):
            print("Collision with enemy!")
            battle_screen = True
            current_enemy = enemy
            break


# After updating the camera_rect:
    for npc in npcs:
        npc.sprite.update_frame()
        # Draw NPC sprite relative to the camera.
        npc_draw_x = npc.x - camera_rect.x - (npc.sprite.sprite_shape[npc.sprite.current_animation]["width"] * npc.sprite.scale_factor) // 2
        npc_draw_y = npc.y - camera_rect.y - (npc.sprite.sprite_shape[npc.sprite.current_animation]["height"] * npc.sprite.scale_factor) // 2

        npc.sprite.draw(screen, npc_draw_x, npc_draw_y)

        # Calculate distance between player and NPC to check interaction range.
        distance = math.sqrt((player.x - npc.x) ** 2 + (player.y - npc.y) ** 2)
        if distance < 60:  # Interaction range
            # Calculate the NPC's on-screen position relative to the camera.
            relative_npc_x = npc.x - camera_rect.x
            relative_npc_y = npc.y - camera_rect.y
            
            # Adjust position for the icon (using NPC's sprite width if needed).
            icon_x = relative_npc_x + npc.sprite.sprite_shape[npc.sprite.current_animation]["width"] // 2 + 10
            icon_y = relative_npc_y - 50
            
            # Draw the interaction icon.
            screen.blit(npc.interaction_symbol, (icon_x, icon_y))
         

    
    player_draw_x = player.x - camera_rect.x - (player.sprite.sprite_shape[player.sprite.current_animation]["width"] * player.sprite.scale_factor) // 2
    player_draw_y = player.y - camera_rect.y - (player.sprite.sprite_shape[player.sprite.current_animation]["height"] * player.sprite.scale_factor) // 2
    player.sprite.update_frame()
    player.sprite.draw(screen, player_draw_x, player_draw_y)
    
    shop_active, current_npc = handle_npc_interaction(player, npcs, text_manager, screen, shop_active, current_npc)

    for npc in npcs:
        npc.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update and draw text overlays.
    text_manager.update()
    text_manager.draw()
    
    pygame.display.update()
    clock.tick(30)

pygame.quit()

