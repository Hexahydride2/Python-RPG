from game_manager import GameManager
import pygame
from new_opening import guild_scene, castle_entrance_denial_scene, lost_forest_entrance_denial_scene, the_arrogant_stranger_scene, introduction_to_saving_princess



# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))  # Set screen size
clock = pygame.time.Clock()

# Create GameManager instance
game_manager = GameManager(screen)

# "New Game" or "Continue"
save_file = game_manager.run()

# Load the save data
player_party, saved_map_id, events_progress = game_manager.load_game(save_file=save_file)

# Load initial map from the saved map id
current_map = game_manager.load_map(saved_map_id, screen, player_party)

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
        current_map = game_manager.load_map(target_map_id, screen, player_party)
        player_party.leader.x = transition_data["player_x"]
        player_party.leader.y = transition_data["player_y"]

        if target_map_id == "guild" and events_progress["guild_scene"] == False:
            guild_scene(screen, player_party)
            player_party.leader.x = 2157
            player_party.leader.y = 1937
            events_progress["guild_scene"] = True
        elif target_map_id == "castle" and player_party.guild_rank == "C":
            castle_entrance_denial_scene(screen, player_party)
            current_map = game_manager.load_map("castle_town", screen, player_party)
            player_party.leader.x = 1870
            player_party.leader.y = 340
            player_party.leader.current_direction = "down"
        elif target_map_id == "lost_forest" and events_progress["guild_scene"] == False:
            lost_forest_entrance_denial_scene(screen, player_party)
            current_map = game_manager.load_map("forest", screen, player_party)
            player_party.leader.x = 2690
            player_party.leader.y = 1450
            player_party.leader.current_direction = "left"
        elif target_map_id == "castle_town" and player_party.guild_rank == "B" and events_progress["the_arrogant_stranger_scene"] == False:
            the_arrogant_stranger_scene(screen, player_party)
            player_party.leader.x = 997
            player_party.leader.y = 2917
            events_progress["the_arrogant_stranger_scene"] = True
        elif target_map_id == "forest" and events_progress["the_arrogant_stranger_scene"] and events_progress["introduction_to_saving_princess"] == False:
            introduction_to_saving_princess(screen, player_party)
            events_progress["introduction_to_saving_princess"] = True


        # Switch BGM
        #change_theme(current_map.bgm)
    ###########################################################

    # Draw the background map
    current_map.draw(screen, events)
    print(player_party.leader.x, player_party.leader.y)


    # save data in each frame
    game_manager.save_game(save_file, current_map.config_key, events_progress)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()