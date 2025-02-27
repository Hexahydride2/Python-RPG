import pygame
from character import Party
from map_manager import load_map  # Loads maps from configuration in Maps.py
import Blackjack  
from game_manager import GameManager

pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

game_manager = GameManager(screen)
player_party = game_manager.load_game(save_file="JsonData\data1.json")

# Load initial map
current_map = load_map("town_map", screen, player_party)

running = True
while running:
    screen.fill((0,0,0))
    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Player walk function
    player_party.leader.walk(keys, current_map)

    # Update map based on player's current position and check for transitions
    player_x = player_party.leader.x
    player_y = player_party.leader.y
    transition_data = current_map.check_transition()
    if transition_data:
        target_map_id = transition_data["map_id"]
        current_map = load_map(target_map_id, screen, player_party.members)
        player_party.leader.x = transition_data["player_x"]
        player_party.leader.y = transition_data["player_y"]
        # Switch BGM
        #change_theme(current_map.bgm)
###########################################################

    # NEW: For the casino map, if "B" is pressed, launch Blackjack
    # if current_map.config_key == "casino_map" and keys[pygame.K_b]:
    #     Blackjack.mainGame(player_party.leader)

    # Draw the background map
    current_map.draw(screen, events)
    #print(player.x, player.y)

    # save data in each frame
    game_manager.save_game("JsonData\data1.json")
    pygame.display.flip()
    clock.tick(30)

pygame.quit()

