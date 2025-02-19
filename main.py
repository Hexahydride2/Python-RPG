import pygame
from character import Character, NPC, Enemy
from items import items_list
from map_manager import Map
from Draw import initialize_main_menu, change_theme



pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

initialize_main_menu()
inventory = {}
for key in items_list().keys():
    inventory[key] = 2
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
change_theme(R"music\NewTownTheme.mp3")

# Create a player
player = Character(
    name="Hero",
    x=1100,
    y=1100,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory=inventory,
    folder_paths=[fR".\timefantasy_characters\timefantasy_characters\frames\chara\chara2_1",
                  fR".\tf_svbattle\singleframes\set2\1"]
)

# # Create NPCs.
# for town map
npc1 = NPC("Old Man", ["Hello, traveler!", "The village is to the north.", "Be careful on your journey."], 1000, 1000,
           [R".\timefantasy_characters\timefantasy_characters\frames\npc\npc1_1"])
npc2 = NPC("Shopkeeper", ["Welcome to my shop!  I sell potions and weapons."], 1200, 1200,
           [R".\timefantasy_characters\timefantasy_characters\frames\npc\npc1_2"], items_list())
npcs = [npc1, npc2]

# for dungeon map
npc3 = NPC("Bold Man", ["Hello, traveler!", "The village is to the north.", "Be careful on your journey."], 1000, 1000,
           [R".\timefantasy_characters\timefantasy_characters\frames\npc\npc3_1"])
npc4 = NPC("LOOOOOL", ["Welcome to my shop!  I sell potions and weapons."], 1335, 1585,
           [R".\timefantasy_characters\timefantasy_characters\frames\npc\npc3_2"], items_list())
npcs1 = [npc3, npc4]

## Create Enemies
enemy1 = Enemy(name="Orc", x=1515, y=1585, level=8, hp=80, mp=40, atk=20, dfn=20, spd=30, inventory={}, exp_reward=5, loot=None, folder_paths=[
    R".\timefantasy_characters\timefantasy_characters\frames\chara\chara5_8",
    R".\tf_svbattle\singleframes\set5\8"
])
enemies = [enemy1]

# Initialize each map
town_map = Map(screen, ".\Backgrounds\TownMap.png", npcs=npcs, map_scale_factor=2, theme = "music\\NewTownTheme.mp3")
dungeon_map = Map(screen, ".\Backgrounds\Map-L.png", npcs=npcs1, enemies=enemies, map_scale_factor=0.3, theme = "music\CaveTheme.mp3")
shop_map = Map(screen, ".\Backgrounds\shopmap.png", npcs=npcs, map_scale_factor=2, theme = "music\TownTheme.mp3")

# Current map
current_map = town_map

## Define transition zones
town_map.add_transition_zone(265, 505, 505, 645, dungeon_map, 965, 1585)
town_map.add_transition_zone(1360, 785, 1414, 830, shop_map, 280, 405)
shop_map.add_transition_zone(230, 445, 335, 447, town_map, 1385, 830)

running = True
while running:
    screen.fill((0,0,0))
    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Player walk function
    player.move(keys, current_map)

##########################################################
    # Update map position based on player movement
    transition_data = current_map.update_camera(player)
    # Check if the player is in a transition zone
    if transition_data:
        # Switch to the new map
        change_theme(transition_data["map"].theme)
        current_map = transition_data["map"]
        # Update player's position to the new entry point
        player.x = transition_data["player_x"]
        player.y = transition_data["player_y"]
###########################################################

    # Draw the background map
    current_map.draw(screen, player, events)
    print(player.x, player.y)

    pygame.display.flip()
    clock.tick(30)
pygame.quit()

