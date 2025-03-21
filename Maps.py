from items import items_list
from character import NPC, Enemy

npc1 = NPC(
    "Old Man",
    ["Hello, traveler! How's going. I hope you're fine.", "The village is to the north.", "Be careful on your journey."],
    1000,
    1000,
    [R".\timefantasy_characters\timefantasy_characters\frames\npc\npc1_1"]
)
npc2 = NPC(
    "Shopkeeper",
    ["Welcome to my shop!  I sell potions and weapons."],
    1200,
    1200,
    [R".\timefantasy_characters\timefantasy_characters\frames\npc\npc1_2"],
    items_list()
)


guild_npc = NPC(
    "Reception girl",
    ["Welcome to the Adventurer's Guild! How can I assist you today?"],
    1300,
    1300,
    [R"timefantasy_characters\timefantasy_characters\frames\npc\npc2_1"],
    guild=True
)


npcs = [npc1, npc2]

npc3 = NPC(
    "Bold Man",
    ["Hello, traveler!", "The village is to the north.", "Be careful on your journey."],
    1000,
    1000,
    [R".\timefantasy_characters\timefantasy_characters\frames\npc\npc3_1"]
)
npc4 = NPC(
    "LOOOOOL",
    ["Welcome to my shop!  I sell potions and weapons."],
    1335,
    1585,
    [R".\timefantasy_characters\timefantasy_characters\frames\npc\npc3_2"],
    items_list()
)
npcs1 = [npc3, npc4]

npcs2 = [
    NPC(
        "Shopkeeper",
        ["Welcome to my shop!  I sell potions and weapons."],
        260,
        190,
        [R".\timefantasy_characters\timefantasy_characters\frames\npc\npc1_2"],
        items_list()
    )
]
friend = [
    NPC(
        "Belle",
        ["Hello, Gabe!, Here is a recap of what has happened!", "I'm glad you came to visit me."],
        625,
        390,
        [R".\timefantasy_characters\timefantasy_characters\frames\chara\chara5_3"]
    )
]

enemy1 = Enemy(
    name="Phoenix",
    x=1515,
    y=1585,
    level=8,
    hp=200,
    mp=100,
    atk=30,
    dfn=20,
    spd=30,
    inventory={},
    skills=["Strike", "Flame Slash", "Earth Smash"],
    folder_paths=[R"Monsters\Phoenix"]
)
enemy1.sprite.set_animation("down_walk")

enemy2 = Enemy(
    name="Slime",
    x=1615,
    y=1885,
    level=8,
    hp=80,
    mp=40,
    atk=20,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=[R"Monsters\Slime"]
)
enemy2.sprite.set_animation("down_walk")

enemies = [enemy1, enemy2]

################## Stone Cave ##################
StoneCaveEnemy = Enemy(
    name="Phoenix",
    x=3310,
    y=610,
    level=15,
    hp=300,
    mp=100,
    atk=30,
    dfn=29,
    spd=30,
    inventory={},
    skills=["Strike", "Flame Slash", "Earth Smash"],
    folder_paths=[R"Monsters\Phoenix"]
)
StoneCaveEnemy.sprite.set_animation("down_walk")

StoneCaveEnemylist = [StoneCaveEnemy]
##################################################


###### Initial Village #######

###### Forest ######

####################

###### Lost Forest #######
forest_npc1 = NPC(
    "Forest Ranger",
    ["Only registered guild adventurers are allowed beyond this point—come back once you've joined the guild."],
    2730,
    1650,
    [R"timefantasy_characters\timefantasy_characters\frames\npc\npc3_2"],    
)
forest_npc1.sprite.set_animation("up_stand")

forest_npcs = [forest_npc1]
##########################

###### Castle Town ######
castle_town_npc1 = NPC(
    "Old man",
    ["Welcome to Castle Town Eryndor, travelers! The heart of the kingdom and home to adventurers, merchants, and dreamers alike!"],
    2030,
    3307,
    [R"timefantasy_characters\timefantasy_characters\frames\npc\npc1_5"],
)

castle_town_npc2 = NPC(
    "Jason",
    ["You there! You look like you've got adventure in your eyes. If you're looking to make a name for yourself, head to the Adventurer's Guild. They'll set you on the right path."],
    1700,
    3017,
    [R"timefantasy_characters\timefantasy_characters\frames\npc\npc1_6"],
)
castle_town_npc3 = NPC(
    "Kaylan",
    ["Hey there, you can head to the Inn to rest and heal up from your travels. The Innkeeper is a good friend of mine."],
    1787,
    2157,
    [R"timefantasy_characters\timefantasy_characters\frames\npc\npc1_6"],
)

castle_town_gate_guard1 = NPC(
    "Gate Guard",
    ["The castle is restricted to authorized personnel only. Move along unless you have official business."],
    1710,
    289,
    [R"timefantasy_characters\timefantasy_characters\frames\military\military1_6"]
)

castle_town_gate_guard2 = NPC(
    "Gate Guard",
    ["State your business. The castle is off-limits to unauthorized personnel."],
    2039,
    289,
    [R"timefantasy_characters\timefantasy_characters\frames\military\military1_6"]
)

castle_town_npc1.sprite.set_animation("left_stand")
castle_town_npc2.sprite.set_animation("right_stand")
castle_town_npc3.sprite.set_animation("down_stand")
castle_town_ncps = [castle_town_npc1, castle_town_npc2, castle_town_gate_guard1, castle_town_gate_guard2, castle_town_npc3]
###### Castle 1F ######

###### Castle 3F ######

###### Guild ######
reception_npc = NPC(
    "Reception girl",
    ["Welcome to the Adventurer's Guild! How can I assist you today?"],
    2157,
    1827,
    [R"timefantasy_characters\timefantasy_characters\frames\npc\npc2_1"],
    guild=True
)

guild_npc = [reception_npc]

#####################

###### Item Shop ######
shop_keeper = NPC(
    "Shopkeeper",
    ["Welcome to my shop!  I sell potions and weapons."],
    970,
    600,
    [R".\timefantasy_characters\timefantasy_characters\frames\npc\npc1_2"],
    items_list()
)

itemshop_npcs = [shop_keeper]

##########################

##### Inn 1F ######
inn_owner = NPC(
    "Inn Owner",
    ["Welcome to my Inn! We've got warm beds, hot meals, and the best ale in town. Your HP and MP have been fully restored!"],
    1120,
    819,
    [R".\timefantasy_characters\timefantasy_characters\frames\npc\npc1_5"],
    inn=True
)

inn_1f_npcs = [inn_owner]

###############################################
map_configs = {
    "Map002": {
        "map_image_path": R"Backgrounds/Map002.png",
        "npcs": npcs,
        "map_scale_factor": 3,
        "bgm": R"music\NewTownTheme.mp3",
        "allow_encounters": True,
        "encounter_rate": 0,
        "layer_json_path": R"Backgrounds/Map002.json",
        "transitions": [
        ]
    },
    "forest" : {
        "map_image_path": R"Backgrounds/forest.png",
        "npcs": forest_npcs,
        "map_scale_factor": 4,
        "bgm": R"music\NewTownTheme.mp3",
        "allow_encounters": True,
        "encounter_rate": 0.001,
        "layer_json_path": R"Backgrounds/forest/forest.json",
        "transitions": [
            {"zone": (1175, 2749, 1425, 2820), "target": "Town_mapv1", "player_x": 3550, "player_y": 1150},
            {"zone": (1170, 35, 1420, 40), "target": "castle_town", "player_x": 1860, "player_y": 3619},
            {"zone": (2840, 1340, 2870, 1600), "target": "lost_forest", "player_x": 80, "player_y": 1650}
        ]
    },
    "lost_forest": {
        "map_image_path": R"Backgrounds/lost_forest.png",
        "npcs": [],
        "map_scale_factor": 4,
        "bgm": R"music\NewTownTheme.mp3",
        "allow_encounters": True,
        "encounter_rate": 0.000,
        "layer_json_path": R"Backgrounds/lost_forest/lost_forest.json",
        "transitions": [
            {"zone": (0, 1510, 40, 1780), "target": "forest", "player_x": 2800, "player_y": 1450},
            {"zone": (2140, 2180, 2200, 2260), "target": "stone_cave", "player_x": 1480, "player_y": 2680}
        ]
    },
    "stone_cave": {
        "map_image_path": R"Backgrounds/stone_cave.png",
        "npcs": [],
        'enemies': StoneCaveEnemylist,
        "map_scale_factor": 4,
        "bgm": R"music\NewTownTheme.mp3",
        "allow_encounters": True,
        "encounter_rate": 0.00,
        "layer_json_path": R"Backgrounds/stone_cave/stone_cave.json",
        "transitions": [
            {"zone": (1440, 2740, 1540, 2830), "target": "lost_forest", "player_x": 2160, "player_y": 2290},
        ]
    },
    "castle_town": {
        "map_image_path": R"Backgrounds/castle_town.png",
        "npcs": castle_town_ncps,
        "map_scale_factor": 4,
        "bgm": R"music\NewTownTheme.mp3",
        "allow_encounters": True,
        "encounter_rate": 0,
        "layer_json_path": R"Backgrounds/castle_town/castle_town.json",
        "transitions": [
            {"zone": (1750, 3749, 1990, 3800), "target": "forest", "player_x": 1280, "player_y": 200},
            {"zone": (1770, 0, 2000, 95), "target": "castle", "player_x": 2060, "player_y": 3960},
            {"zone": (980, 2789, 1030, 2829), "target": "guild", "player_x": 1467, "player_y": 2637},
            {"zone": (2510, 1900, 2570, 1970), "target": "item_shop", "player_x": 750, "player_y": 1080},
            {"zone": (867, 1687, 957, 1787), "target": "inn_1F", "player_x": 1040, "player_y": 1360}
        ]
    },
    "castle": {
        "map_image_path": R"Backgrounds/castle.png",
        "npcs": [],
        "map_scale_factor": 4,
        "bgm": R"music\NewTownTheme.mp3",
        "allow_encounters": True,
        "encounter_rate": 0,
        "layer_json_path": R"Backgrounds/castle/castle.json",
        "transitions": [
            {"zone": (1860, 4000, 2250, 4080), "target": "castle_town", "player_x": 1870, "player_y": 229},
            {"zone": (2040, 1820, 2100, 1870), "target": "castle_1F", "player_x": 1970, "player_y": 3599},
        ]
    },
    "castle_1F": {
        "map_image_path": R"Backgrounds/castle1F.png",
        "npcs": [],
        "map_scale_factor": 4,
        "bgm": R"music\NewTownTheme.mp3",
        "allow_encounters": True,
        "encounter_rate": 0,
        "layer_json_path": R"Backgrounds/castle1F/castle1F.json",
        "transitions": [
            {"zone": (1840, 3679, 2080, 3800), "target": "castle", "player_x": 2070, "player_y": 1929},
            {"zone": (1850, 1939, 2090, 2039), "target": "castle_3F", "player_x": 1970, "player_y": 2069},
            
        ]
    },
    "castle_3F": {
        "map_image_path": R"Backgrounds/castle3F.png",
        "npcs": [],
        "map_scale_factor": 4,
        "bgm": R"music\NewTownTheme.mp3",
        "allow_encounters": True,
        "encounter_rate": 0,
        "layer_json_path": "Backgrounds/castle3F/castle3F.json",
        "transitions": [
            {"zone": (1860, 2149, 2080, 2249), "target": "castle_1F", "player_x": 1970, "player_y": 2069},
        ]
    },
    "guild": {
        "map_image_path": R"Backgrounds/guild.png",
        "npcs": guild_npc,
        "map_scale_factor": 3,
        "bgm": R"music\NewTownTheme.mp3",
        "allow_encounters": True,
        "encounter_rate": 0,
        "layer_json_path": R"Backgrounds/guild/guild.json",
        "transitions": [
            {"zone": (1327, 2727, 1627, 2827), "target": "castle_town", "player_x": 997, "player_y": 2857},
        ]
    },
    "item_shop": {
        "map_image_path": R"Backgrounds/itemshop.png",
        "npcs": itemshop_npcs,
        "map_scale_factor": 3,
        "bgm": R"music\NewTownTheme.mp3",
        "allow_encounters": True,
        "encounter_rate": 0,
        "layer_json_path": R"Backgrounds/itemshop/itemshop.json",
        "transitions": [
            {"zone": (720, 1120, 790, 1170), "target": "castle_town", "player_x": 2547, "player_y": 1997},
        ]
    },
    "inn_1F": {
        "map_image_path": R"Backgrounds/inn_1F.png",
        "npcs": inn_1f_npcs,
        "map_scale_factor": 3,
        "bgm": R"music\NewTownTheme.mp3",
        "allow_encounters": True,
        "encounter_rate": 0,
        "layer_json_path": R"Backgrounds/inn1F/inn1F.json",
        "transitions": [
            {"zone": (1010, 1420, 1070, 1460), "target": "castle_town", "player_x": 917, "player_y": 1817},
        ]
    },

    "town_map": {
        "map_image_path": R"Backgrounds/TownMap.png",
        "npcs": npcs,
        "enemies": enemies,
        "map_scale_factor": 2,
        "bgm": R"music\NewTownTheme.mp3",
        "allow_encounters": True,
        "encounter_rate": 0,
        "layer_json_path": None,
        "transitions": [
            {"zone": (265, 505, 505, 645), "target": "dungeon_map", "player_x": 965, "player_y": 1585},
            {"zone": (1360, 785, 1414, 830), "target": "shop_map", "player_x": 280, "player_y": 405},
            {"zone": (425, 1070, 490, 1145), "target": "casino_map", "player_x": 100, "player_y": 100}
        ]
    },

    "dungeon_map": {
        "map_image_path": R".\Backgrounds\Map-L.png",
        "npcs": npcs1,
        "enemies": enemies,
        "map_scale_factor": 0.3,
        "bgm": R"music\CaveTheme.mp3",
        "allow_encounters": False,
        "encounter_rate": 0,
        "layer_json_path": None,
        "transitions": []  
    },
    "shop_map": {
        "map_image_path": R".\Backgrounds\shopmap.png",
        "npcs": npcs2,
        "enemies": [],
        "map_scale_factor": 2,
        "bgm": R"music\TownTheme.mp3",
        "allow_encounters": False,
        "encounter_rate": 0,
        "layer_json_path": None,
        "transitions": [{"zone": (230, 425, 340, 475), "target": "town_map", "player_x": 1370, "player_y": 950} ]  
    },
    "Town_mapv1": {
        "map_image_path": R".\Backgrounds\TownMapv1.png",
        "npcs": [],
        "enemies": [],
        "map_scale_factor": 3,
        "bgm": R"music\TownTheme.mp3",
        "allow_encounters": False,
        "encounter_rate": 0,
        "layer_json_path": R"Backgrounds\TownMapV1\TownMapV1.json",
        "transitions": [
            {"zone": (2020, 340, 2060, 400), "target": "playerhouse", "player_x": 620, "player_y": 575},
            {"zone": (1730, 340, 1775, 380), "target": "friendshouse", "player_x": 620, "player_y": 575},
            {"zone": (3600, 1090, 3640, 1200), "target": "forest", "player_x": 1275, "player_y": 2649},
        ]
    },
    "townTest_map": {
        "map_image_path": R".\Backgrounds\TownMapTest.png",
        "npcs": [],
        "enemies": [],
        "map_scale_factor": 3,
        "bgm": None,
        "allow_encounters": False,
        "encounter_rate": 0,
        "layer_json_path": None,
    },
    "initial_village_map": {
        "map_image_path": R".\Backgrounds\map.png",
        "npcs": [],
        "enemies": [],
        "map_scale_factor": 3,
        "bgm": None,
        "allow_encounters": False,
        "encounter_rate": 0,
        "layer_json_path": None,
    },
    "playerhouse": {
        "map_image_path": R".\Backgrounds\playerhouse.png",
        "npcs": [],
        "enemies": [],
        "map_scale_factor": 3,
        "bgm": None,
        "allow_encounters": False,
        "encounter_rate": 0,
        "layer_json_path": R"Backgrounds\PlayerHouse\PlayerHouse.json",
        "transitions": [
            {"zone": (590, 600, 685, 653), "target": "Town_mapv1", "player_x": 2030, "player_y": 450}
        ]
    },
    "casino_map": {
        "map_image_path": R".\Backgrounds\casino.png",
        "npcs": [],
        "enemies": [],
        "map_scale_factor": 3,
        "bgm": R"music\TownTheme.mp3",
        "allow_encounters": False,
        "encounter_rate": 0,
        "layer_json_path": None,
        "transitions": []
    },
    "friendshouse": {
        "map_image_path": R".\Backgrounds\FriendsHouse.png",
        "npcs": friend,
        "enemies": [],
        "map_scale_factor": 3,
        "bgm": None,
        "allow_encounters": False,
        "encounter_rate": 0,
        "layer_json_path": R"Backgrounds\FriendsHouse\FriendsHouse.json",
        "transitions": [
            {"zone": (590, 600, 685, 653), "target": "Town_mapv1", "player_x": 1750, "player_y": 440}
        ]
    }
}