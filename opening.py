import pygame
from character import Character, Enemy
from scene import Scene

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

military_paths = [R".\timefantasy_characters\timefantasy_characters\frames\military\military1_8",
                  R".\tf_svbattle\singleframes\military1\8"]

name = "Gabe"
# Create a player
player = Character(
    name=name,
    x=400,
    y=400,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=military_paths
)

npc_path = [R".\timefantasy_characters\timefantasy_characters\frames\chara\chara5_3"]
Lira = Character(
    name="Lira",
    x=300,
    y=400,
    folder_paths=npc_path
)

Elder_Thalos = Character(
    name="Elder Thalos",
    x=900,
    y=300,
    folder_paths=[R".\timefantasy_characters\timefantasy_characters\frames\npc\npc3_1"]
)

# Define actions for Scene 

opening_scene1_actions = [
    {"type": "animation", "character": player, "pose": "left_stand"},
    {"type": "animation", "character": Lira, "pose": "right_stand"},
    {"type": "wait", "duration": 500},
    {"type": "talk", "character": None, "message": "The story begins in Elmshade, a peaceful, secluded village nestled in a lush forest. The village is known for its towering elm trees, glowing fireflies at night, and a sense of timeless tranquility. However, strange occurrences have recently begun to unsettle the villagers—animals acting erratically, crops withering overnight, and whispers of shadowy figures in the woods."},
    {"type": "talk", "character": Lira, "message": fR"(smiling) You’re staring off into space again, {name}. What’s on your mind this time? Another grand adventure you’re dreaming up?"},
    {"type": "talk", "character": player, "message": "(sighs) It’s not just a dream, Lira. Something feels… off lately. The forest is too quiet, and the villagers are on edge. Even the animals seem scared."},
    {"type": "talk", "character": Lira, "message":'(playfully nudges him) You\'re overthinking it. Maybe they\'re just tired of you practicing your sword swings at dawn every morning.'},
    {"type": "talk", "character": player, "message": '(grins) Hey, someone’s got to keep this village safe. Besides, you’re one to talk—I’ve seen you sneaking off to practice your archery.'},
    {"type": "talk", "character": Lira, "message": '(laughs) Guilty as charged. But seriously, Kael, if something’s wrong, we’ll handle it together. Like always.'},
    {"type": "talk", "character": None, "message": 'Suddenly, a loud crash echoes from the edge of the village, followed by screams. The two jump to their feet.'},
    {"type": "animation", "character": player, "pose": "down_stand"},
    {"type": "animation", "character": Lira, "pose": "down_stand"},
    {"type": "wait", "duration": 1000},
    {"type": "animation", "character": player, "pose": "left_stand"},
    {"type": "animation", "character": Lira, "pose": "right_stand"},
    {"type": "talk", "character": player, "message": '(alert) What was that?!'},
    {"type": "talk", "character": Lira, "message": 'I don’t know, but it doesn’t sound good. Let’s go!'},
    {"type": "move", "character": player, "direction": "down", "distance": 300},
    {"type": "move", "character": Lira, "direction": "down", "distance": 300},
]

# Create Scene 1
opening_scene1 = Scene(screen, [player, Lira], opening_scene1_actions, top_left_x=1000, top_left_y=100, background_image=".\Backgrounds\map.png", scale_factor=3)

player = Character(
    name=name,
    x=400,
    y=-100,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=military_paths
)

Lira = Character(
    name="Lira",
    x=350,
    y=-100,
    folder_paths=[R".\timefantasy_characters\timefantasy_characters\frames\chara\chara5_3"]
)

## Create Enemies
enemy1 = Enemy(name="Orc", x=200, y=400, level=8, hp=80, mp=40, atk=20, dfn=20, spd=30, inventory={}, exp_reward=5, loot=None, folder_paths=[
    R".\timefantasy_characters\timefantasy_characters\frames\chara\chara5_8",
    R".\tf_svbattle\singleframes\set5\8"
])


opening_scene2_actions = [
    {"type": "animation", "character": enemy1, "pose": "right_stand"},
    {"type": "move", "character": player, "direction": "down", "distance": 500},
    {"type": "animation", "character": player, "pose": "left_stand"},
    {"type": "move", "character": Lira, "direction": "down", "distance": 460},
    {"type": "animation", "character": Lira, "pose": "left_stand"},
    {"type": "talk", "character": player, "message": 'Lira, cover me! I’ll take it head-on!'},
    {"type": "talk", "character": Lira, "message": 'Got it! Just don’t get yourself killed, hero!'},
    {"type": "battle", "player": player, "enemy": enemy1, "background_image": ".\craftpix-net-270096-free-forest-battle-backgrounds\PNG\game_background_4\game_background_4.png"},
    {"type": "animation", "character": player, "pose": "left_stand"},
    {"type": "move", "character": enemy1, "direction": "left", "distance": 700},
    {"type": "talk", "character": Lira, "message": '(breathing heavily) What… was that thing? I’ve never seen anything like it.'},
    {"type": "talk", "character": player, "message": '(staring at the fading mist) I don’t know, but it felt… unnatural. Like it wasn’t really alive.'},
    {"type": "move", "character": Elder_Thalos, "direction": "left", "distance": 500},
    {"type": "animation", "character": Elder_Thalos, "pose": "down_stand"},
    {"type": "animation", "character": player, "pose": "up_stand"},
    {"type": "animation", "character": Lira, "pose": "up_stand"},
    {"type": "talk", "character": Elder_Thalos, "message":f'{name}, Lira… this is worse than I feared. The darkness is returning, and it seems you two are already caught in its web.'},
    {"type": "talk", "character": player, "message":'What do you mean, Elder? What’s going on?'},
    {"type": "talk", "character": Elder_Thalos, "message": f'It’s time you learned the truth, {name}. About your father… and the destiny you were born to fulfill.'}
    
]

# Create scene2
opening_scene2 = Scene(screen, [player, Lira, enemy1, Elder_Thalos], opening_scene2_actions, top_left_x=700, top_left_y=800, background_image=".\Backgrounds\map.png", scale_factor=3)

# Run scenes sequentially
opening_scene1.run()
opening_scene2.run()


# Quit Pygame when all scenes are done
pygame.quit()
