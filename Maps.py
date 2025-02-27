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


npcs = [npc1, npc2, guild_npc]

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
    exp_reward=5,
    loot=None,
    folder_paths=[R"Monsters\phoenix"]
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
    exp_reward=5,
    loot=None,
    folder_paths=[R"Monsters\slime"]
)
enemy2.sprite.set_animation("down_walk")

enemies = [enemy1, enemy2]

map_configs = {
    "town_map": {
        "map_image_path": "Backgrounds/TownMap.png",
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
        "transitions": []  
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
            {"zone": (1730, 340, 1775, 380), "target": "friendshouse", "player_x": 620, "player_y": 575}
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