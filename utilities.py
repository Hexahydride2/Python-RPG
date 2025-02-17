import re
import math
import random
import pygame
from battle import Battle
from Draw import change_theme, revert_theme
from shop import Shop


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

def handle_npc_interaction(player, npcs, text_manager, screen, shop_active, current_npc):
    """Checks if the player is near an NPC and starts a conversation."""
    keys = pygame.key.get_pressed()

    # Open the shop is shop_active is True
    if shop_active:  
        # While shop is open, only allow shop interactions
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Close shop on ESC
                    shop_active = False
                    player.can_move = True
                else:
                    current_npc.shop.handle_event(event)  # Process shop input
        current_npc.shop.draw()  # Redraw shop screen
        return shop_active, current_npc # Prevent other interactions while in shop mode

    # Deal with the interaction with NPCs
    for npc in npcs:
        distance = ((player.x - npc.x) ** 2 + (player.y - npc.y) ** 2) ** 0.5  # Distance formula
        if distance < 60:  # Interaction range
            npc.draw_interaction_symbol(screen)  # Show interaction symbol
        
        # If the NPC is already talking, pressing Enter should go to next message
            if npc.talking:
                if keys[pygame.K_RETURN]:  # Press 'Enter' to continue dialogue
                    player.can_move = False
                    if text_manager.waiting_for_next:
                        text_manager.next_message()  # Go to next line
                        if not text_manager.messages:  # If no messages left, stop talking
                            npc.talking = False
                            player.can_move = True
                            
                            # Check if NPC is a shopkeeper and open the shop
                            if npc.shop_items:
                                player.can_move = False
                                shop_active = True
                                current_npc = npc
                                npc.shop = Shop(screen, player, npc.shop_items)
                                return shop_active, current_npc # Exit to prevent further interactions

                return shop_active, current_npc # Avoid multiple NPCs getting activated

            # Press 'E' to start the conversation
            if keys[pygame.K_e]:  
                player.can_move = False
                if not npc.talking:
                    npc.talking = True
                    npc.talk(text_manager, player, screen)
                    return shop_active, current_npc  # Exit to prevent multiple interactions

                break  # Stop checking other NPCs after talking to one
    return shop_active, current_npc


def move_to_battle(screen, player, enemies, current_enemy, battle_screen = False):
    if battle_screen and current_enemy:
        battle = Battle(screen, player, current_enemy["character"], background_image=".\craftpix-net-270096-free-forest-battle-backgrounds\PNG\game_background_4\game_background_4.png")
        change_theme("Music\BattleTheme.mp3")
        result = battle.run()
        if result == "win":
            enemies.remove(current_enemy)
            battle_screen = False  # Exit battle screen
            revert_theme()
        elif result == "lose":
            battle_screen = False  # Exit battle screen
            if player.current_direction == "right":
                player.x -= 60  # Move player away to prevent instant re-entry
            elif player.current_direction == "left":
                player.x += 60  # Move player away to prevent instant re-entry
            elif player.current_direction == "up":
                player.y += 60  # Move player away to prevent instant re-entry
            elif player.current_direction == "down":
                player.y -= 60  # Move player away to prevent instant re-entry
            revert_theme()
        elif result == "escape":
            battle_screen = False  # Exit battle screen
            if player.current_direction == "right":
                player.x -= 60  # Move player away to prevent instant re-entry
            elif player.current_direction == "left":
                player.x += 60  # Move player away to prevent instant re-entry
            elif player.current_direction == "up":
                player.y += 60  # Move player away to prevent instant re-entry
            elif player.current_direction == "down":
                player.y -= 60  # Move player away to prevent instant re-entry
            revert_theme()
    
    return enemies, battle_screen


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