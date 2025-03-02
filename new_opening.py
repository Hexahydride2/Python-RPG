import pygame
from character import Character, Enemy
from scene import Scene

def opening_scene(screen, player_party):
    name = player_party.leader.name

    folder_paths = player_party.leader.folder_paths
    Elysia = Character(
    name="Elysia",
    x=-500,
    y=-500,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=folder_paths
    )

    opening_scene1_actions = [
        {"type": "talk", "character": Elysia, "message": f"{name}, you have passed beyond the veil of life...but your story is not yet over. If you save this world, I may grant you a second chance. Do you accept this fate?"},
        {"type": "talk", "character": None, "message": f"{name} tries to speak, but no sound comes out."},
        {"type": "talk", "character": None, "message": "Darkness envelops you as you lose consciousness..."},
        {"type": "talk", "character": None, "message": "..."},
        {"type": "talk", "character": None, "message": "Hello, hello, can you hear me?"}
    ]

    opening_scene = Scene(screen, [Elysia], opening_scene1_actions)

    player = Character(
    name=name,
    x=720,
    y=300,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=folder_paths,
    scale_factor=1
    )

    Liora = Character(
    name="Liora",
    x=650,
    y=300,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\npc\npc2_6"],
    scale_factor=3
    )

    opening_scene2_actions = [
        {"type": "animation", "character": Liora, "pose": "right_stand"},
        {"type": "talk", "character": Liora, "message": "Oh, you're awake! I was so worried. My father and I found you in the forest, unconscious. What's your name?"},
        {"type": "animation", "character": player, "pose": "left_stand"},
        {"type": "talk", "character": player, "message": f"I'm...{name}. I'm from Canada. Where am I?"},
        {"type": "talk", "character": Liora, "message": "Canada? I've never heard of it. You're in Hearthaven Village. My father and I brought you here after we found you in the woods."}
    ]

    opening_scene2 = Scene(screen, [player, Liora], opening_scene2_actions, scale_factor=3, background_image=R"Backgrounds\Playerhouse.png")

    player = Character(
    name=name,
    x=720,
    y=300,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=folder_paths,
    scale_factor=1
    )

    Liora = Character(
    name="Liora",
    x=650,
    y=300,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\npc\npc2_6"],
    scale_factor=3
    )

    Garic = Character(
    name="Garic",
    x=600,
    y=550,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\npc\npc1_1"],
    scale_factor=3
    )

    opening_scene3_actions = [
        {"type": "animation", "character": Liora, "pose": "right_stand"},
        {"type": "animation", "character": player, "pose": "left_stand"},
        {"type": "move", "character": Garic, "direction": "up", "distance": 100},
        {"type": "talk", "character": Garic, "message": "Liora! Stay inside! There's a monster outside!"},
        {"type": "move", "character": Garic, "direction": "right", "distance": 120},
        {"type": "move", "character": Garic, "direction": "up", "distance": 50},
        {"type": "talk", "character": Garic, "message": "You! You've got a sword. Help me drive it away!"},
        {"type": "animation", "character": player, "pose": "down_stand"},
        {"type": "talk", "character": player, "message": "What? I've never fought before!"},
        {"type": "talk", "character": player, "message": "..."},
        {"type": "talk", "character": player, "message": '"Maybe this is what she meant by saving the world..."'},
        {"type": "talk", "character": player, "message": "OK...I will try."},
        {"type": "talk", "character": Garic, "message": "Thank you so much!"},
        {"type": "move", "character": Garic, "direction": "left", "distance": 50},
        {"type": "animation", "character": Garic, "pose": "right_stand"},
        {"type": "move", "character": player, "direction": "down", "distance": 170},
        {"type": "move", "character": player, "direction": "left", "distance": 100},
        {"type": "move", "character": player, "direction": "down", "distance": 100},
        {"type": "wait", "duration": 100},
    ]
    opening_scene3 = Scene(screen, [player, Liora, Garic], opening_scene3_actions, speed=5, scale_factor=3, background_image=R"Backgrounds\Playerhouse.png")

    player = Character(
    name=name,
    x=1000,
    y= 450,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=folder_paths,
    scale_factor=1
    )

    Slime = Enemy(
        name="Slime",
        x = 500,
        y = 350,
        folder_paths=[R"Monsters\Slime"],
        level=1,
        hp=70,
        mp=30,
        atk=10,
        dfn=5,
        spd=5
    )


    opening_scene4_actions = [
        {"type": "animation", "character": Slime, "pose": "left_walk"},
        {"type": "move", "character": player, 'direction': "left", "distance": 350},
        {"type": "talk", "character": player, "message": "I don't know what I'm doing, but I can't back down now. Let's do this!"},
        {"type": "battle", "player_party": player_party, "enemies":[Slime], "background_image": "craftpix-net-270096-free-forest-battle-backgrounds\PNG\game_background_4\game_background_4.png"},
    ]
    
    opening_scene4 = Scene(screen, [player, Slime], opening_scene4_actions, top_left_x=500, top_left_y=100, scale_factor=3, background_image="Backgrounds\TownMapV1.png")


    Liora = Character(
    name="Liora",
    x=1400,
    y=380,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\npc\npc2_6"],
    scale_factor=3
    )

    Garic = Character(
    name="Garic",
    x=1400,
    y=460,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\npc\npc1_1"],
    scale_factor=3
    )

    opening_scene5_actions = [
        {"type": "move", "character": Garic, "direction": "left", "distance": 680},
        {"type": "animation", "character": Garic, "pose": "left_stand"},
        {"type": "move", "character": Liora, "direction": "left", "distance": 680},
        {"type": "animation", "character": Liora, "pose": "left_stand"},
        {"type": "animation", "character": player, "pose": "right_stand"},
        {"type": "talk", "character": Garic, "message": "You handled yourself well out there. Listen, my daughter needs to go to the castle town, Eryndor, to fetch supplies. With monsters roaming about, it's too dangerous for her to go alone. Will you escort her?"},
        {"type": "talk", "character": player, "message": "I...I guess I don't have much of a choice."},
        {"type": "talk", "character": Garic, "message": "Good. And while you're there, you might find someone who knows about this 'Canada' of yours. The castle town is full of travelers and scholars."},
        {"type": "move", "character": Liora, "direction": "left", "distance": 50},
        {"type": "animation", "character": Liora, "pose": "down_stand"},
        {"type": "animation", "character": player, "pose": "up_stand"},
        {"type": "talk", "character": Liora, "message": "Thank you, Kael. I'll be in your care."}
    ]
    opening_scene5 = Scene(screen, [player, Liora, Garic], opening_scene5_actions, top_left_x=500, top_left_y=100, scale_factor=3, background_image="Backgrounds\TownMapV1.png")

    opening_scene.run()
    opening_scene2.run()
    opening_scene3.run()
    opening_scene4.run()
    opening_scene5.run()