import pygame
from character import Character, Enemy, Party
from scene import Scene

def opening_scene(screen, player_party):
    name = player_party.leader.name
    folder_paths = player_party.leader.folder_paths

    player = Character(
    name=name,
    x=-500,
    y=-500,
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
        {"type": "talk", "character": player, "message": f'"I... I remember now. I died. It was so sudden—a train, screeching metal, and then...nothing. What is this place? And why am I here?"'},
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

def guild_scene(screen, player_party):
    name = player_party.leader.name
    folder_paths = player_party.leader.folder_paths

    player = Character(
    name=name,
    x=600,
    y=600,
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

    Mira = Character(
    name="Mira",
    x=500,
    y=200,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\npc\npc2_1"],
    scale_factor=3
    )

    Garret = Character(
    name="Garret",
    x=380,
    y=170,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\npc\npc3_2"],
    scale_factor=3
    )

    scene4_actions = [
        {"type": "animation", "character": Garret, "pose": "right_stand"},
        {"type": "animation", "character": player, "pose": "up_stand"},
        {"type": "move", "character": player, "direction": "up", "distance": 100},
        {"type": "wait", "duration": 100},
        {"type": "move", "character": Garret, "direction": "down", "distance": 100},
        {"type": "move", "character": Garret, "direction": "right", "distance": 220},
        {"type": "move", "character": Garret, "direction": "down", "distance": 130},
        {"type": "talk", "character": Garret, "message": f"Hey there, newcomer! You look like you're here to join the guild. Have you already signed up?"},
        {"type": "talk", "character": player, "message": f"No, not yet."},
        {"type": "talk", "character": Garret, "message": f"Ah, I thought so. Head over to the reception desk. Mira will get you sorted. She's the one with the stack of papers and the frazzled look."},
        {"type": "talk", "character": player, "message": f"Thank you! I'll ask her."},
        {"type": "move", "character": Garret, "direction": "left", "distance": 50},
        {"type": "animation", "character": Garret, "pose": "right_stand"},
        {"type": "move", "character": player, "direction": "up", "distance": 200},
        {"type": "move", "character": player, "direction": "right", "distance": 300},
    ]

    scene4 = Scene(screen, [player, Garret], scene4_actions, scale_factor=3, background_image=R"Backgrounds/guild.png", top_left_x=850, top_left_y=2000)

    player = Character(
    name=name,
    x=250,
    y=600,
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

    Mira = Character(
    name="Mira",
    x=630,
    y=85,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\npc\npc2_1"],
    scale_factor=3
    )

    scene5_actions = [
        {"type": "move", "character": player, "direction": "right", "distance": 380},
        {"type": "move", "character": player, "direction": "up", "distance": 400},
        {"type": "talk", "character": player, "message": 'Excuse me, do you know anything about a place called Canada?'},
        {"type": "talk", "character": Mira, "message": "Hmm, never heard of it. But if anyone would know, it's the king! Of course, you can't just waltz into the castle. You'll need to be an A-rank adventurer to get an audience."},
        {"type": "talk", "character": player, "message": "How do I become an A-rank adventurer?"},
        {"type": "talk", "character": Mira, "message": "Oh, you're not registered yet? Let me fix that for you."},
        {"type": "move", "character": Mira, "direction": "right", "distance": 100},
        {"type": "animation", "character": Mira, "pose": "up_stand"},
        {"type": "wait", "duration": 100},
        {"type": "move", "character": Mira, "direction": "left", "distance": 100},
        {"type": "animation", "character": Mira, "pose": "down_stand"},
        {"type": "talk", "character": Mira, "message": "There! You're now an official adventurer. Start taking quests and work your way up! But don't get ahead of yourself—aim to become a B-rank party first. It's a big step, but it'll open up more opportunities for you"},
        {"type": "talk", "character": player, "message": "A B-rank party? What does that mean?"},
        {"type": "talk", "character": Mira, "message": "Well, adventurers are ranked individually, but parties are ranked too! To become a B-rank party, you'll need to complete enough quests and prove your teamwork. It's not just about strength—it's about trust and coordination. Once you're B-rank, you'll have access to better quests and resources. And who knows? Maybe one day you'll even reach A-rank!"},
        {"type": "talk", "character": player, "message": f"({name} sighs but accepts his new role.)"},
        {"type": "talk", "character": Mira, "message": f"Good luck, Kael! Oh, and don't forget to check the quest board over there. Start small, and you'll be B-rank in no time!"},
    ]
    scene5 = Scene(screen, [player, Mira], scene5_actions, scale_factor=3, background_image=R"Backgrounds/guild.png", top_left_x=1500, top_left_y=1700)

    scene4.run()
    scene5.run()
    

def castle_entrance_denial_scene(screen, player_party):
    name = player_party.leader.name
    folder_paths = player_party.leader.folder_paths

    player = Character(
    name=name,
    x=600,
    y=20,
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

    gate_guard_1 = Character(
    name="Gate Guard1",
    x=435,
    y=240,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\military\military1_6"],
    scale_factor=3
    )

    gate_guard_2 = Character(
    name="Gate Guard2",
    x=760,
    y=240,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\military\military1_6"],
    scale_factor=3
    )
    scene1_actions = [
        {"type": "animation", "character": player, "pose": "up_stand"},
        {"type": "move", "character": player, "direction": "up", "distance": 20},
        {"type": "move", "character": gate_guard_1, "direction": "right", "distance": 161},
        {"type": "animation", "character": gate_guard_1, "pose": "up_stand"},
        {"type": "talk", "character": gate_guard_1, "message": "Halt! Only those with legitimate permission, such as A-rank adventurers, may enter the castle. Come back when you've proven your worth."},
        {"type": "move", "character": player, "direction": "down", "distance": 150},
        {"type": "move", "character": gate_guard_1, "direction": "left", "distance": 161},
        {"type": "animation", "character": gate_guard_1, "pose": "down_stand"},
        {"type": "move", "character": player, "direction": "down", "distance": 140},
    ]

    scene1 = Scene(screen, [player, gate_guard_1, gate_guard_2], scene1_actions, scale_factor=4, top_left_x=1250, top_left_y=0, background_image=R"Backgrounds/castle_town.png")
    scene1.run()

def lost_forest_entrance_denial_scene(screen, player_party):
    name = player_party.leader.name
    folder_paths = player_party.leader.folder_paths

    player = Character(
    name=name,
    x=1200,
    y=320,
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

    forest_ranger = Character(
    name="Forest Ranger",
    x=1100,
    y=530,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\npc\npc3_2"],
    scale_factor=3
    )

    scene1_actions = [
        {"type": "animation", "character": player, "pose": "right_stand"},
        {"type": "animation", "character": forest_ranger, "pose": "up_stand"},
        {"type": "move", "character": forest_ranger, "direction": "up", "distance": 200},
        {"type": "animation", "character": forest_ranger, "pose": "right_stand"},
        {"type": "animation", "character": player, "pose": "left_stand"},
        {"type": "talk", "character": forest_ranger, "message": "Only registered guild adventurers are allowed beyond this point—come back once you've joined the guild."},
        {"type": "move", "character": forest_ranger, "direction": "down", "distance": 200},
        {"type": "animation", "character": forest_ranger, "pose": "up_stand"},
        {"type": "move", "character": player, "direction": "left", "distance": 130},
    ]

    scene1 = Scene(screen, [player, forest_ranger], scene1_actions, scale_factor=4, top_left_x=1600, top_left_y=1087, background_image=R"Backgrounds/forest.png")
    scene1.run()

##########################################3

if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))  # Set screen size
    clock = pygame.time.Clock()
    player = Character(
        name="Reiya",
        x=720,
        y=300,
        level=10,
        hp=100,
        mp=50,
        atk=40,
        dfn=20,
        spd=30,
        inventory={},
        folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\chara\chara1_1"],
        scale_factor=1
        )
    player_party = Party(player)
    lost_forest_entrance_denial_scene(screen, player_party)



