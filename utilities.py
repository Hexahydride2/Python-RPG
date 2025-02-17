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

def handle_npc_interaction(player_x, player_y, npcs, text_manager, screen):
    """Checks if the player is near an NPC and starts a conversation."""
    keys = pygame.key.get_pressed()

    for npc in npcs:
        distance = ((player_x - npc.x) ** 2 + (player_y - npc.y) ** 2) ** 0.5  # Distance formula
        if distance < 60:  # Interaction range
            npc.draw_interaction_symbol(screen)  # Show interaction symbol
        
        # If the NPC is already talking, pressing Enter should go to next message
            if npc.talking:
                if keys[pygame.K_RETURN]:  # Press 'Enter' to continue dialogue
                    if text_manager.waiting_for_next:
                        text_manager.next_message()  # Go to next line
                        if not text_manager.messages:  # If no messages left, stop talking
                            npc.talking = False
                            
                print("Message Finished:", text_manager.message_finished)
                return  # Avoid multiple NPCs getting activated

            # Press 'E' to start the conversation
            if keys[pygame.K_e]:  
                if not npc.talking:
                    npc.talking = True
                    npc.talk(text_manager)
                break  # Stop checking other NPCs after talking to one
