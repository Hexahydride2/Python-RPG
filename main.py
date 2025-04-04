from game_manager import GameManager
import pygame
from events import guild_scene, castle_entrance_denial_scene, lost_forest_entrance_denial_scene, the_arrogant_stranger_scene, introduction_to_saving_princess, the_princess_in_peril_scene, the_dilemma_of_king_scene, the_castle_3F_entrance_denial_scene, the_stone_cave_crisis_scene, meeting_the_king_scene
from utilities import change_theme
from character import Character


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
    
    # Draw the background map
    current_map.draw(screen, events)

    # Player walk function
    player_party.leader.walk(keys, current_map)

    # Update map based on player's current position and check for transitions
    player_x = player_party.leader.x
    player_y = player_party.leader.y
 
    transition_data = current_map.check_transition()
    
    if transition_data:
        print(transition_data)
        target_map_id = transition_data["map_id"]
        # Change the map only when the target map is different from the current map
        no_map_change = True
        if target_map_id != game_manager.current_map_id:
            current_map = game_manager.load_map(target_map_id, screen, player_party)
            player_party.leader.x = transition_data["player_x"]
            player_party.leader.y = transition_data["player_y"]
            no_map_change = False
   

        if target_map_id == "Guild" and events_progress["guild_scene"] == False:
            guild_scene(screen, player_party)
            player_party.leader.x = 2157
            player_party.leader.y = 1937
            events_progress["guild_scene"] = True

            is_Finn = False
            for member in player_party.members:
                if member.name == "Finn":
                    is_Finn = True
            if not is_Finn:
                Finn = Character(
                    name="Finn",
                    x=630,
                    y=200,
                    level=5,
                    hp=170,
                    mp=110,
                    atk=40,
                    dfn=20,
                    spd=30,
                    skills=["Strike", "Flame Slash"],
                    inventory={},
                    folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\chara\chara2_1", R"tf_svbattle\singleframes\set2\1"],
                    scale_factor=3
                    )
                player_party.add_member(Finn)    

        elif target_map_id == "Eryndor Castle" and events_progress["the_princess_in_peril_scene"] == False:
            castle_entrance_denial_scene(screen, player_party)
            current_map = game_manager.load_map("Eryndor", screen, player_party)
            player_party.leader.x = 1870
            player_party.leader.y = 340
            player_party.leader.current_direction = "down"
        elif target_map_id == "Lost Forest" and events_progress["guild_scene"] == False:
            lost_forest_entrance_denial_scene(screen, player_party)
            current_map = game_manager.load_map("Forest", screen, player_party)
            player_party.leader.x = 2690
            player_party.leader.y = 1450
            player_party.leader.current_direction = "left"
        elif target_map_id == "Eryndor" and player_party.guild_rank == "B" and events_progress["the_arrogant_stranger_scene"] == False:
            the_arrogant_stranger_scene(screen, player_party)
            player_party.leader.x = 997
            player_party.leader.y = 2917
            events_progress["the_arrogant_stranger_scene"] = True
        elif target_map_id == "Forest" and events_progress["the_arrogant_stranger_scene"] and events_progress["introduction_to_saving_princess"] == False:
            introduction_to_saving_princess(screen, player_party)
            events_progress["introduction_to_saving_princess"] = True
        elif target_map_id == "Lost Forest" and events_progress["introduction_to_saving_princess"] and events_progress["the_princess_in_peril_scene"] == False:
            scene_done = the_princess_in_peril_scene(screen, player_party)
            if scene_done:
                player_party.leader.current_direction = "right"
                player_party.leader.x = 550
                player_party.leader.y = 1650
                events_progress["the_princess_in_peril_scene"] = True
        elif target_map_id == "Eryndor Castle 3F" and events_progress["the_dilemma_of_king_scene"] == False:
            the_dilemma_of_king_scene(screen, player_party)
            current_map = game_manager.load_map("Eryndor Castle 1F", screen, player_party)
            player_party.leader.x = 1480
            player_party.leader.y = 1709
            player_party.leader.current_direction = "down"
            events_progress["the_dilemma_of_king_scene"] = True
        elif target_map_id == "Eryndor Castle 3F" and events_progress["the_stone_cave_crisis_scene"] == False:
            the_castle_3F_entrance_denial_scene(screen, player_party)
            current_map = game_manager.load_map("Eryndor Castle 1F", screen, player_party)
            player_party.leader.x = 1480
            player_party.leader.y = 1709
            player_party.leader.current_direction = "down"
        elif no_map_change and target_map_id == "stone_cave" and events_progress["the_dilemma_of_king_scene"] and events_progress["the_stone_cave_crisis_scene"] == False:
            scene_done = the_stone_cave_crisis_scene(screen, player_party)
            if scene_done:
                player_party.leader.current_direction = "left"
                player_party.leader.x = 550
                player_party.leader.y = 760
                events_progress["the_stone_cave_crisis_scene"] = True
        elif no_map_change and target_map_id == "Eryndor Castle 3F" and events_progress["the_stone_cave_crisis_scene"] and events_progress["meeting_the_king_scene"] == False:
            meeting_the_king_scene(screen, player_party)
            events_progress["meeting_the_king_scene"] = True
            player_party.leader.current_direction = "down"
            player_party.leader.x = 1480
            player_party.leader.y = 959

        # Switch BGM
        #change_theme(current_map.bgm)
    ###########################################################
    print(player_party.leader.x, player_party.leader.y)


    # save data in each frame
    game_manager.save_game(save_file, current_map.config_key, events_progress)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()