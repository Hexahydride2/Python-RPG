import pygame
from character import Character, Enemy, Party, NPC
from scene import Scene

def opening_scene(screen, player_party):
    scene_done = False
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
    opening_scene.run()

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
    opening_scene2.run()

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
    opening_scene3.run()

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
    opening_scene4.run()

    # Check if the player party is alive (This must be after battle scene)
    if opening_scene4.player_party:
        no_alive = True
        for member in opening_scene4.player_party.members:
            print(member.name, member.hp)
            if member.hp > 0:
                no_alive = False
        if no_alive:
            return scene_done


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
        {"type": "talk", "character": Liora, "message": f"Thank you, {name}. I'll be in your care."}
    ]
    opening_scene5 = Scene(screen, [player, Liora, Garic], opening_scene5_actions, top_left_x=500, top_left_y=100, scale_factor=3, background_image="Backgrounds\TownMapV1.png")
    opening_scene5.run()

    scene_done = True
    return scene_done

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

    Finn = Character(
    name="Finn",
    x=630,
    y=200,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\chara\chara2_1"],
    scale_factor=3
    )

    scene5_actions = [
        {"type": "animation", "character": Finn, "pose": "up_stand"},
        {"type": "move", "character": player, "direction": "right", "distance": 380},
        {"type": "move", "character": player, "direction": "up", "distance": 300},
        {"type": "move", "character": Finn, "direction": "right", "distance": 180},
        {"type": "move", "character": Finn, "direction": "down", "distance": 100},
        {"type": "animation", "character": Finn, "pose": "left_stand"},
        {"type": "move", "character": player, "direction": "up", "distance": 100},
        {"type": "talk", "character": player, "message": 'Excuse me, do you know anything about a place called Canada?'},
        {"type": "talk", "character": Mira, "message": "Hmm, never heard of it. But if anyone would know, it's the king! Of course, you can't just waltz into the castle. You'll need to be an A-rank adventurer to get an audience."},
        {"type": "talk", "character": player, "message": "How do I become an A-rank adventurer?"},
        {"type": "talk", "character": Mira, "message": "Oh, you're not registered yet? Let me fix that for you."},
        {"type": "move", "character": Mira, "direction": "right", "distance": 100},
        {"type": "animation", "character": Mira, "pose": "up_stand"},
        {"type": "wait", "duration": 100},
        {"type": "move", "character": Mira, "direction": "left", "distance": 100},
        {"type": "animation", "character": Mira, "pose": "down_stand"},
        {"type": "talk", "character": Mira, "message": "There! You're now an official adventurer. But listen, you can't go it alone since adventuring is dangerous, and teamwork is key. In fact..."},
        {"type": "move", "character": Mira, "direction": "right", "distance": 160},
        {"type": "animation", "character": Mira, "pose": "down_stand"},
        {"type": "animation", "character": Finn, "pose": "up_stand"},
        {"type": "move", "character": Mira, "direction": "left", "distance": 160},
        {"type": "animation", "character": Mira, "pose": "down_stand"},
        {"type": "wait", "duration": 200},
        {"type": "move", "character": Finn, "direction": "up", "distance": 100},
        {"type": "move", "character": Finn, "direction": "left", "distance": 100},
        {"type": "talk", "character": Mira, "message":f"This is Finn. He just signed up too and doesn't have a party yet. Finn, meet {name}. You two should team up!"},
        {"type": "animation", "character": player, "pose": "right_stand"},
        {"type": "talk", "character": Finn, "message": f"Hey, {name}, I'm new to this too, but I'm ready to learn. What do you say we watch each other's backs?"},
        {"type": "talk", "character": player, "message": f"Alright, Finn. Let's give it a shot. Better to have someone to rely on than go solo."},
        {"type": "talk", "character": None, "message": "Finn joined in your party!"},
        {"type": "animation", "character": player, "pose": "up_stand"},
        {"type": "animation", "character": Finn, "pose": "up_stand"},
        {"type": "talk", "character": Mira, "message": "Great! Now you're both set. Start taking quests and work your way up! And remember, teamwork makes the dream work! But don't get ahead of yourself—aim to become a B-rank party first. It's a big step, but it'll open up more opportunities for you."},
        {"type": "talk", "character": player, "message": "A B-rank party? What does that mean?"},
        {"type": "talk", "character": Mira, "message": "Well, adventurers are ranked individually, but parties are ranked too! To become a B-rank party, you'll need to complete enough quests and prove your teamwork. It's not just about strength—it's about trust and coordination. Once you're B-rank, you'll have access to better quests and resources. And who knows? Maybe one day you'll even reach A-rank!"},
        {"type": "talk", "character": player, "message": f"({name} sighs but accepts his new role.)"},
        {"type": "talk", "character": Mira, "message": f"Good luck, {name}! Oh, and don't forget to check the quest board over there. Start small, and you'll be B-rank in no time!"},
    ]
    scene5 = Scene(screen, [player, Mira, Finn], scene5_actions, scale_factor=3, background_image=R"Backgrounds/guild.png", top_left_x=1500, top_left_y=1700)

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

def the_arrogant_stranger_scene(screen, player_party):
    name = player_party.leader.name
    folder_paths = player_party.leader.folder_paths

    player = Character(
    name=name,
    x=580,
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

    Darius = Character(
    name="???",
    x=1300,
    y=600,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\chara\chara2_4"],
    scale_factor=3
    )

    scene1_actions = [
        {"type": "move", "character": player, "direction": "down", "distance": 50},
        {"type": "move", "character": Darius, "direction": "left", "distance": 720},
        {"type": "move", "character": Darius, "direction": "up", "distance": 150},
        {"type": "talk", "character": Darius, "message": "Watch where you're going, rookie."},
        {"type": "move", "character": player, "direction": "left", "distance": 50},
        {"type": "animation", "character": player, "pose": "right_stand"},
        {"type": "move", "character": Darius, "direction": "up", "distance": 150},
    ]

    scene1 = Scene(screen, [player, Darius], scene1_actions, scale_factor=4, top_left_x=400, top_left_y=2500, background_image=R"Backgrounds\castle_town.png")

    scene2_actions = [
        {"type": "animation", "character": player, "pose": "right_stand"},
        {"type": "move", "character": player, "direction": "right", "distance": 50},
        {"type": "animation", "character": player, "pose": "down_stand"},
        {"type": "talk", "character": player, "message": "Who does that guy think he is? He looks strong, though..."},
    ] 
    scene2 = Scene(screen, [player], scene2_actions, scale_factor=4, top_left_x=400, top_left_y=2500, background_image=R"Backgrounds\castle_town.png")

    scene1.run()
    scene2.run()

def introduction_to_saving_princess(screen, player_party):
    name = player_party.leader.name
    folder_paths = player_party.leader.folder_paths

    player = Character(
    name=name,
    x=610,
    y=150,
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

    Seraphina = Character(
    name="???",
    x=1300,
    y=600,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\chara\chara8_4"],
    scale_factor=3
    )
    scene1_actions = [
        {"type": "talk", "character": Seraphina, "message": "Help! Someone, please! HELP!"},
        {"type": "talk", "character": player, "message": "This is from the direction of the Lost Forest... Something's wrong. I need to check it out."},
    ]
    
    scene1 = Scene(screen,[player, Seraphina], scene1_actions, scale_factor=4, top_left_x=650, top_left_y=0, background_image=R"Backgrounds/forest.png")
    scene1.run()

def the_princess_in_peril_scene(screen, player_party):
    scene_done = False
    name = player_party.leader.name
    folder_paths = player_party.leader.folder_paths
    player = Character(
    name=name,
    x=30,
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

    Seraphina = Character(
    name="Seraphina",
    x=580,
    y=330,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\chara\chara8_4"],
    scale_factor=3
    )

    cultist1 = Enemy(
        name="Cultist A",
        x = 700,
        y = 350,
        folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\chara\chara5_8", R"tf_svbattle\singleframes\set5\8"],
        level=10,
        hp=400,
        mp=200,
        atk=30,
        dfn=15,
        spd=10
    )

    cultist2 = Enemy(
        name="Cultist B",
        x = 650,
        y = 250,
        folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\chara\chara5_8", R"tf_svbattle\singleframes\set5\8"],
        level=1,
        hp=400,
        mp=200,
        atk=30,
        dfn=15,
        spd=5
    )

    scene1_actions = [
        {"type": "animation", "character": player, "pose": "right_stand"},
        {"type": "animation", "character": Seraphina, "pose": "right_stand"},
        {"type": "animation", "character": cultist1, "pose": "idle2"},
        {"type": "animation", "character": cultist2, "pose": "idle2"},
        {"type": "talk", "character": cultist1, "message": "Don't resist, Our master, Malakar, demands your presence. You'll come with us, one way or another!"},
        {"type": "talk", "character": Seraphina, "message": "I'll never go with you! Whatever your demon master wants, he won't get it!"},
        {"type": "move", "character": player, "direction": "right", "distance": 500},
        {"type": "talk", "character": player, "message": "Leave her alone! Who are you, and what do you want with her?"},
        {"type": "move", "character": Seraphina, "direction": "left", "distance": 150},
        {"type": "animation", "character": Seraphina, "pose": "right_stand"},
        {"type": "talk", "character": cultist2, "message": "This doesn't concern you, fool. But if you interfere, you'll regret it!"},
        {"type": "battle", "player_party": player_party, "enemies":[cultist1, cultist2], "background_image": "craftpix-net-270096-free-forest-battle-backgrounds\PNG\game_background_4\game_background_4.png"},
        {"type": "animation", "character": cultist2, "pose": "dead"},
        {"type": "talk", "character": cultist1, "message": R"You've only delayed the inevitable... Malakar will rise, and the princess's blood will be the key..."},
        {"type": "animation", "character": cultist1, "pose": "dead"},
        {"type": "wait", "duration": 500},
    ]
    scene1 = Scene(screen, [player, Seraphina, cultist1, cultist2], scene1_actions, scale_factor=4, top_left_x=0, top_left_y=1300, background_image=R"Backgrounds/lost_forest.png")
    scene1.run()


    # Check if the player party is alive (This must be after battle scene)
    if scene1.player_party:
        no_alive = True
        for member in scene1.player_party.members:
            print(member.name, member.hp)
            if member.hp > 0:
                no_alive = False
        if no_alive:
            return scene_done
        

    scene2_actions = [
        {"type": "move", "character": Seraphina, "direction": "right", "distance": 200},
        {"type": "move", "character": Seraphina, "direction": "up", "distance": 50},
        {"type": "animation", "character": Seraphina, "pose": "left_stand"},
        {"type": "talk", "character": Seraphina, "message": R"Thank you for your help. I'm Seraphina, the princess of this kingdom. What's your name?"},
        {"type": "talk", "character": player, "message": fR"I'm {name}. I'm...new here."},
        {"type": "talk", "character": None, "message": f"({name} explains his situation and his desire to meet the king.)"},
        {"type": "talk", "character": Seraphina, "message": f"You saved my life. The least I can do is take you to meet my father. He'll want to thank you personally, and perhaps he can help you with your search for answers."},
    ]

    scene2 = Scene(screen, [player, Seraphina], scene2_actions, scale_factor=4, top_left_x=0, top_left_y=1300, background_image=R"Backgrounds/lost_forest.png")
    scene2.run()

    scene_done = True
    return scene_done


def the_dilemma_of_king_scene(screen, player_party):
    name = player_party.leader.name
    folder_paths = player_party.leader.folder_paths
    player = Character(
    name=name,
    x=575,
    y=350,
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

    Seraphina = Character(
    name="Seraphina",
    x=665,
    y=330,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\chara\chara8_4"],
    scale_factor=3
    )

    Roderick = Character(
    name="Captain Roderick",
    x=535,
    y=250,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\military\military1_5"],
    scale_factor=3
    )

    

    scene1_actions = [
        {"type": "animation", "character": player, "pose": "up_stand"},
        {"type": "animation", "character": Seraphina, "pose": "up_stand"},
        {"type": "move", "character": Roderick, "direction": "right", "distance": 85},
        {"type": "animation", "character": Roderick, "pose": "down_stand"},
        {"type": "talk", "character": Seraphina, "message": fR"Captain Roderick, I need to speak with my father immediately. This is {name}, the adventurer who saved me from the cultists. He needs the king's help."},
        {"type": "talk", "character": Roderick, "message": fR"Princess, I'm afraid the king is occupied. There's been an incident in the Lost Forest. A group of miners went missing in the Stone Cave, and the king is coordinating a rescue effort. He can't be disturbed right now."},
        {"type": "talk", "character": player, "message": fR"What happened in the Stone Cave?"},
        {"type": "talk", "character": Roderick, "message": fR"The cave is a vital source of ore for the kingdom, but recently, strange tremors have been reported. The miners who went in haven't returned, and scouts say the cave is now overrun with monsters. The king is trying to organize a team to investigate, but all our best adventurers are already occupied with other crises."},
        {"type": "talk", "character": Seraphina, "message": fR"{name}, this could be your chance to prove yourself. If you can solve this problem, my father will surely grant you an audience."},
        {"type": "talk", "character": player, "message": fR"I'll do it. I need to find answers about my world, and if helping your kingdom gets me closer to that, I'm in."},
        {"type": "talk", "character": Roderick, "message": fR"Very well. I'll inform the king of your intentions. Be careful, though. The Stone Cave is no place for the unprepared."},
        {"type": "animation", "character": player, "pose": "right_stand"},
        {"type": "animation", "character": Seraphina, "pose": "left_stand"},
        {"type": "talk", "character": Seraphina, "message":f"Good luck, {name}. I'll be waiting for your return."},
        {"type": "animation", "character": player, "pose": "up_stand"},
        {"type": "animation", "character": Seraphina, "pose": "up_stand"},
    ]

    scene1 = Scene(screen, [player, Seraphina, Roderick], scene1_actions, scale_factor=3, top_left_x=825, top_left_y=1350, background_image="Backgrounds/castle1F.png")

    scene1.run()

def the_castle_3F_entrance_denial_scene(screen, player_party):
    name = player_party.leader.name
    folder_paths = player_party.leader.folder_paths
    player = Character(
    name=name,
    x=625,
    y=250,
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

    Roderick = Character(
    name="Captain Roderick",
    x=535,
    y=250,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\military\military1_5"],
    scale_factor=3
    )
 

    scene1_actions = [
        {"type": "animation", "character": player, "pose": "up_stand"},
        {"type": "move", "character": Roderick, "direction": "right", "distance": 30},
        {"type": "animation", "character": player, "pose": "left_stand"},
        {"type": "talk", "character": Roderick, "message": fR"Be careful, the Stone Cave is in the Lost Forest."},
        {"type": "move", "character": Roderick, "direction": "left", "distance": 30},
        {"type": "animation", "character": Roderick, "pose": "down_stand"},
        {"type": "move", "character": player, "direction": "down", "distance": 50},
    ]

    scene1 = Scene(screen, [player, Roderick], scene1_actions, scale_factor=3, top_left_x=825, top_left_y=1350, background_image="Backgrounds/castle1F.png")

    scene1.run()

def the_stone_cave_crisis_scene(screen, player_party):
    scene_done = False

    name = player_party.leader.name
    folder_paths = player_party.leader.folder_paths
    player = Character(
    name=name,
    x=600,
    y=350,
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

    MinerA = Character(
    name="Miner A",
    x=1000,
    y=1000,
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
        {"type": "animation", "character": player, "pose": "left_stand"},
        {"type": "talk", "character": MinerA, "message": "Help! Someone, please! It's coming back!"},
        {"type": "move", "character": player, "direction": "left", "distance": 330},
        {"type": "move", "character": player, "direction": "up", "distance": 150},
        {"type": "move", "character": player, "direction": "left", "distance": 150},
        {"type": "move", "character": player, "direction": "up", "distance": 200},
    ]
    scene1 = Scene(screen, [player, MinerA], scene1_actions, scale_factor=3, top_left_x=400, top_left_y=750, background_image="Backgrounds/stone_cave.png")
    scene1.run()

    player = Character(
    name=name,
    x=520,
    y=330,
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

    MinerA = Character(
    name="Miner A",
    x=400,
    y=320,
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

    MinerB = Character(
    name="Miner B",
    x=450,
    y=250,
    level=10,
    hp=100,
    mp=50,
    atk=40,
    dfn=20,
    spd=30,
    inventory={},
    folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\npc\npc3_4"],
    scale_factor=3
    )

    Minotaur = Enemy(
        name="Minotaur",
        x = 700,
        y = 120,
        folder_paths=[R"Monsters\Minotaur"],
        level=15,
        hp=1050,
        mp=1000,
        atk=45,
        dfn=20,
        spd=5
    )

    Minotaur_after = Enemy(
        name="Minotaur",
        x = 700,
        y = 120,
        folder_paths=[R"Monsters\Minotaur"],
        level=15,
        hp=500,
        mp=1000,
        atk=60,
        dfn=20,
        spd=5
    )


    scene2_actions = [
        {"type": "animation", "character": player, "pose": "up_stand"},
        {"type": "animation", "character": Minotaur, "pose": "left_stand"},
        {"type": "animation", "character": MinerA, "pose": "right_stand"},
        {"type": "animation", "character": MinerB, "pose": "right_stand"},
        {"type": "talk", "character": player, "message": "Hold on! I'll get you out of here. What happened?"},
        {"type": "animation", "character": player, "pose": "left_stand"},
        {"type": "talk", "character": MinerB, "message": "It's the Minotaur! It's not like any beast I've ever seen—it's evil, pure evil! It attacked us without warning, smashed the supports, and brought down the ceiling. It's toying with us, like it enjoys our fear!"},
        {"type": "animation", "character": player, "pose": "up_stand"},
        {"type": "move", "character": Minotaur, "direction": "left", "distance": 200},
        {"type": "animation", "character": Minotaur, "pose": "down_stand"},
        {"type": "move", "character": MinerA, "direction": "left", "distance": 100},
        {"type": "move", "character": MinerB, "direction": "left", "distance": 100},
        {"type": "animation", "character": MinerA, "pose": "right_stand"},
        {"type": "animation", "character": MinerB, "pose": "right_stand"},
        {"type": "talk", "character": Minotaur, "message": "Another fool dares to enter my domain? How delightful. I was growing bored with these weaklings."},
        {"type": "talk", "character": player, "message": "Who are you? Why are you attacking these miners?"},
        {"type": "talk", "character": Minotaur, "message": "Why? Because I can. Because their screams amuse me. This cave is mine, and all who enter shall suffer my wrath!"},
        {"type": "talk", "character": MinerA, "message": "It's not just a beast... it's a monster. It thrives on pain and destruction. You have to stop it, or none of us will make it out alive!"},
        {"type": "talk", "character": player, "message": "I won't let you harm anyone else. If this cave is yours, then I'll take it from you."},
        {"type": "talk", "character": Minotaur, "message": "Bold words for a mere mortal. Very well, let's see if you can back them up. Come, little human—entertain me!"},
        {"type": "move", "character": Minotaur, "direction": "down", "distance": 30},
        {"type": "battle", "player_party": player_party, "enemies":[Minotaur], "background_image": "Backgrounds/cave_battle.png"},
        {"type": "talk", "character": Minotaur, "message": "Is that all you've got? Pathetic! I've crushed stronger foes than you!"},
        {"type": "move", "character": Minotaur, "direction": "down", "distance": 20},
        {"type": "battle", "player_party": player_party, "enemies":[Minotaur_after], "background_image": "Backgrounds/cave_battle.png"},
        {"type": "talk", "character": Minotaur_after, "message": "You...you think this changes anything? Even if you defeat me, the darkness in this world will never be extinguished. You're just delaying the inevitable."},
        {"type": "talk", "character": player, "message":"Maybe, but as long as there are people willing to fight, monsters like you will never win."},
        {"type": "animation", "character": Minotaur, "pose": "dead"},
        {"type": "move", "character": player, "direction": "up", "distance": 50},
        {"type": "animation", "character": player, "pose": "left_stand"},
        {"type": "talk", "character": MinerA, "message":"It's...it's over, You actually defeated it, I can't believe it."},
        {"type": "talk", "character": player, "message":"We need to get out of here. The cave might still be unstable."},
        {"type": "talk", "character": MinerB, "message":"Thank you, adventurer. You saved my life. But...do you think there are more creatures like that out there?"},
        {"type": "talk", "character": player, "message":"If there are, I'll be ready. Let's get you back to the village."},
        {"type": "move", "character": MinerB, "direction": "right", "distance": 110},
        {"type": "move", "character": MinerB, "direction": "down", "distance": 80},
        {"type": "move", "character": MinerB, "direction": "right", "distance": 70},
        {"type": "move", "character": MinerB, "direction": "down", "distance": 200},
        {"type": "move", "character": MinerB, "direction": "right", "distance": 130},
        {"type": "move", "character": MinerB, "direction": "down", "distance": 220},
        {"type": "move", "character": MinerA, "direction": "right", "distance": 220},
        {"type": "move", "character": MinerA, "direction": "down", "distance": 200},
        {"type": "move", "character": MinerA, "direction": "right", "distance": 150},
        {"type": "move", "character": MinerA, "direction": "down", "distance": 220},
    ]
    scene2 = Scene(screen, [player, MinerA, MinerB, Minotaur], scene2_actions, scale_factor=3, top_left_x=0, top_left_y=430, background_image="Backgrounds/stone_cave.png")
    scene2.run()

    # Check if the player party is alive (This must be after battle scene)
    if scene1.player_party:
        no_alive = True
        for member in scene1.player_party.members:
            print(member.name, member.hp)
            if member.hp > 0:
                no_alive = False
        if no_alive:
            return scene_done
    
    scene_done = True
    return scene_done

def meeting_the_king_scene(screen, player_party):
    name = player_party.leader.name
    folder_paths = player_party.leader.folder_paths

    player = NPC(
            name,
            [],
            610,
            720,
            folder_paths,
            scale_factor=1
            )
    
    King = NPC(
            "King Aldric",
            [],
            600,
            70,
            [R"timefantasy_characters\timefantasy_characters\frames\chara\chara8_3"],
            scale_factor=3
            )
    
    Seraphina = NPC(
            "Seraphina",
            [],
            600,
            250,
            [R"timefantasy_characters\timefantasy_characters\frames\chara\chara8_4"],
            scale_factor=3
            )
    Seraphina.sprite.set_animation("up_stand")
    
    guard1 = NPC(
            "Guard",
            [],
            480,
            150,
            [R"timefantasy_characters\timefantasy_characters\frames\military\military1_8"],
            scale_factor=3
            )
    
    guard2 = NPC(
            "Guard",
            [],
            740,
            150,
            [R"timefantasy_characters\timefantasy_characters\frames\military\military1_8"],
            scale_factor=3
            )
    
    guard3 = NPC(
            "Guard",
            [],
            350,
            110,
            [R"timefantasy_characters\timefantasy_characters\frames\military\military1_8"],
            scale_factor=3
            )
    
    guard4 = NPC(
            "Guard",
            [],
            870,
            110,
            [R"timefantasy_characters\timefantasy_characters\frames\military\military1_8"],
            scale_factor=3
            )
    
    guard5 = NPC(
            "Guard",
            [],
            470,
            400,
            [R"timefantasy_characters\timefantasy_characters\frames\military\military1_7"],
            scale_factor=3
            )
    guard5.sprite.set_animation("right_stand")
    
    guard6 = NPC(
            "Guard",
            [],
            760,
            400,
            [R"timefantasy_characters\timefantasy_characters\frames\military\military1_7"],
            scale_factor=3
            )
    guard6.sprite.set_animation("left_stand")
    
    guard7 = NPC(
            "Guard",
            [],
            470,
            550,
            [R"timefantasy_characters\timefantasy_characters\frames\military\military1_7"],
            scale_factor=3
            )
    guard7.sprite.set_animation("right_stand")
    
    guard8 = NPC(
            "Guard",
            [],
            760,
            550,
            [R"timefantasy_characters\timefantasy_characters\frames\military\military1_7"],
            scale_factor=3
            )
    guard8.sprite.set_animation("left_stand")
    
    scene1_actions = [
        {"type": "move", "character": player, "direction": "up", "distance": 330},
        {"type": "animation", "character": Seraphina, "pose": "down_stand"},
        {"type": "wait", "duration": 500},
        {"type": "move", "character": Seraphina, "direction": "right", "distance": 80},
        {"type": "animation", "character": Seraphina, "pose": "up_stand"},
        {"type": "move", "character": player, "direction": "up", "distance": 70},
        {"type": "move", "character": King, "direction": "down", "distance": 70},
        {"type": "talk", "character": King, "message": f"Seraphina, this must be the adventurer you spoke of. {name}, was it?"},
        {"type": "talk", "character": Seraphina, "message": f"Yes, Father. {name} not only saved me from the cultists but also rescued the miners from the Stone Cave. He's proven himself a true hero."},
        {"type": "talk", "character": King, "message": f"You have my gratitude, {name}. The Stone Cave is vital to our kingdom, and you've saved many lives today. Now, Seraphina mentioned you were looking for information about a place called 'Canada.'"},
        {"type": "talk", "character": player, "message": f"Yes, Your Majesty. I'm not from this world, and I need to find a way back—or at least understand how I got here."},
        {"type": "talk", "character": King, "message": f"Canada... I'm afraid I've never heard of it. However, many years ago, another adventurer asked about the same place. He was a skilled warrior, but I can't recall his name. If you're looking for answers, becoming an adventurer might be your best path. Our kingdom is in dire need of strong adventurers like you."},
        {"type": "talk", "character": player, "message": f"I'll do whatever it takes to find the truth. If helping your kingdom gets me closer to that, I'm in."},
        {"type": "talk", "character": King, "message": f"Then I wish you luck, {name}. You've already proven yourself a friend to this kingdom. If you ever need aid, don't hesitate to ask."},
        {"type": "wait", "duration": 500},
        {"type": "move", "character": player, "direction": "down", "distance": 200},
        {"type": "animation", "character": Seraphina, "pose": "down_stand"},
        {"type": "talk", "character": Seraphina, "message": f"{name}!"},
        {"type": "move", "character": Seraphina, "direction": "left", "distance": 80},
        {"type": "move", "character": Seraphina, "direction": "down", "distance": 150},
        {"type": "animation", "character": player, "pose": "up_stand"},
        {"type": "talk", "character": Seraphina, "message": f"Thank you for helping us, {name}. You've already made a difference in this kingdom."},
        {"type": "talk", "character": player, "message": f"I still have a long way to go. If I'm going to find out about Canada and that other adventurer, I'll need to get stronger."},
        {"type": "talk", "character": Seraphina, "message": f"Then let me help you. As a princess, I have access to resources and information. If you ever need anything, don't hesitate to ask."},
        {"type": "talk", "character": player, "message": f"Thank you, Seraphina. I think I've found my path. I'll live as an adventurer and uncover the truth about my world—and this one."}
    ]

    scene1 = Scene(screen, [player, King, Seraphina, guard1, guard2, guard3, guard4, guard5, guard6, guard7, guard8], scene1_actions, scale_factor=3, top_left_x=840, top_left_y=400, background_image="Backgrounds/castle3F.png")
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
        hp=1000,
        mp=500,
        atk=400,
        dfn=200,
        spd=30,
        inventory={},
        folder_paths=[R"timefantasy_characters\timefantasy_characters\frames\chara\chara1_1", R"tf_svbattle\singleframes\set1\1"],
        scale_factor=1
        )
    player_party = Party(player)
    meeting_the_king_scene(screen, player_party)



