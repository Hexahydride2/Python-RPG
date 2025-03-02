from game_manager import GameManager
import pygame


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))  # Set screen size
clock = pygame.time.Clock()

# Create GameManager instance
game_manager = GameManager(screen)

# "New Game" or "Continue"
save_file = game_manager.run()

# Load the save data
player_party, saved_map_id = game_manager.load_game(save_file=save_file)

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
        # Switch BGM
        #change_theme(current_map.bgm)
    ###########################################################

    # Draw the background map
    current_map.draw(screen, events)
    print(player_party.leader.x, player_party.leader.y)


    # save data in each frame
    game_manager.save_game(R"SaveData\test.json", current_map.config_key)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()