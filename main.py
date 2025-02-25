import pygame
from character import Character, NPC, Enemy
from items import items_list
from map_manager import Map
from Draw import change_theme
import Blackjack  

pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

inventory = {}
for key in items_list().keys():
    inventory[key] = 2
screen = pygame.display.set_mode((screen_width, screen_height))


military_paths = [R".\timefantasy_characters\timefantasy_characters\frames\military\military1_8",
                  R".\tf_svbattle\singleframes\military1\8"]
normal_chara_paths = [fR".\timefantasy_characters\timefantasy_characters\frames\chara\chara1_5",
                  fR".\tf_svbattle\singleframes\set1\5"]
# Create a player
player = Character(
    name="Hero",
    x=700,
    y=700,
    level=10,
    hp=100,
    mp=200,
    atk=40,
    dfn=20,
    spd=30,
    inventory=inventory,
    skills=["Strike", "Earth Smash", "Flame Slash", "Crystal Strike", "Frost Blade", "Explosive Arrow"],
    folder_paths=normal_chara_paths,
    scale_factor=1
)
player_party = [player]

# # Create NPCs.
# for town map
npc1 = NPC("Old Man", ["Hello, traveler! How's going. I hope you're fine.", "The village is to the north.", "Be careful on your journey."], 1000, 1000,
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

npcs2 = [NPC("Shopkeeper", ["Welcome to my shop!  I sell potions and weapons."], 260, 190,
           [R".\timefantasy_characters\timefantasy_characters\frames\npc\npc1_2"], items_list())]
friend = [NPC("Belle", ["Hello, Gabe!, Here is a recap of what has happened!", "I'm glad you came to visit me."], 625, 390,
              [R".\timefantasy_characters\timefantasy_characters\frames\chara\chara5_3"])]
## Create Enemies
enemy1 = Enemy(name="Phoenix", x=1515, y=1585, level=8, hp=80, mp=100, atk=20, dfn=20, spd=30, inventory={}, skills=["Strike", "Flame Slash", "Earth Smash"] ,exp_reward=5, loot=None, folder_paths=[
    R"Monsters\phoenix"
])
enemy1.sprite.set_animation("down_walk")
enemy2 = Enemy(name="Bat", x=1615, y=1885, level=8, hp=80, mp=40, atk=20, dfn=20, spd=30, inventory={}, exp_reward=5, loot=None, folder_paths=[
    R"Monsters\bat"
])
enemy2.sprite.set_animation("down_walk")
enemies = [enemy1, enemy2]

# Initialize each map
town_map = Map(screen, "Backgrounds\TownMap.png", player_party=player_party, npcs=npcs, map_scale_factor=2, bgm= "music\\NewTownTheme.mp3", allow_encounters=True, encounter_rate=0)
dungeon_map = Map(screen, ".\Backgrounds\Map-L.png", player_party=player_party, npcs=npcs1, enemies=enemies, map_scale_factor=0.3, bgm= "music\CaveTheme.mp3")
shop_map = Map(screen, ".\Backgrounds\shopmap.png", player_party=player_party, npcs=npcs2, map_scale_factor=2, bgm= "music\TownTheme.mp3")
Town_mapv1 = Map(screen, ".\Backgrounds\TownMapv1.png", player_party=player_party, map_scale_factor=3, layer_json_path="Backgrounds\TownMapV1\TownMapV1.json", bgm= "music\TownTheme.mp3")
townTest_map = Map(screen, ".\Backgrounds\TownMapTest.png", player_party=player_party, map_scale_factor=3, layer_json_path=None)
initial_village_map = Map(screen, ".\Backgrounds\map.png", player_party=player_party, map_scale_factor=3, layer_json_path=None)
playerhouse = Map(screen, ".\Backgrounds\playerhouse.png", player_party=player_party, map_scale_factor=3, layer_json_path="Backgrounds\PlayerHouse\PlayerHouse.json")
casino_map = Map(screen, ".\\Backgrounds\\casino.png", player_party=player_party, map_scale_factor=3, bgm="music\\TownTheme.mp3")
friendshouse = Map(screen, ".\\Backgrounds\\FriendsHouse.png", player_party=player_party, npcs=friend, map_scale_factor=3, layer_json_path="Backgrounds\FriendsHouse\FriendsHouse.json")


# Current map
current_map = town_map
#change_theme(R"music\NewTownTheme.mp3")

## Define transition zones
town_map.add_transition_zone(265, 505, 505, 645, dungeon_map, 965, 1585)
town_map.add_transition_zone(1360, 785, 1414, 830, shop_map, 280, 405)
shop_map.add_transition_zone(230, 445, 335, 447, town_map, 1385, 830)
town_map.add_transition_zone(425, 1070, 490, 1145, casino_map, 100, 100)
Town_mapv1.add_transition_zone(2020, 340, 2060, 400, playerhouse, 620, 575)
playerhouse.add_transition_zone(590, 600, 685, 653, Town_mapv1, 2030, 450)
friendshouse.add_transition_zone(590, 600, 685, 653, Town_mapv1, 1750, 440)
Town_mapv1.add_transition_zone(1730, 340, 1775, 380, friendshouse, 620, 575)
running = True
while running:
    screen.fill((0,0,0))
    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Player walk function
    player.walk(keys, current_map)

##########################################################
    # Update map position based on player movement
    transition_data = current_map.update_camera()
    # Check if the player is in a transition zone
    if transition_data:
        # Switch to the new map
        current_map = transition_data["map"]
        # Update player's position to the new entry point
        player.x = transition_data["player_x"]
        player.y = transition_data["player_y"]
        # Switch BGM
        #change_theme(current_map.bgm)
###########################################################

    # NEW: If the casino map is active and player presses "B", launch blackjack
    if current_map == casino_map and keys[pygame.K_b]:
        Blackjack.mainGame(player)  # Launch blackjack game

    # Draw the background map
    current_map.draw(screen, events)
    #print(player.x, player.y)

    pygame.display.flip()
    clock.tick(30)
pygame.quit()

