import pygame
from text_manager import TextManager
from shop import Shop
from battle import Battle
from menu import Menu
from utilities import add_menu, change_theme, revert_theme
import numpy as np
import json
from character import Enemy
import random
from Maps import map_configs
from adventure_guild import AdventurerGuild

class Map:
    def __init__(self, screen, map_image_path, player_party, npcs=[], enemies=[], map_scale_factor=None, bgm=None, layer_json_path=False, allow_encounters=False, random_encounter_enemies=["Slime"], encounter_rate=0, transitions=None, battle_background_image=".\craftpix-net-270096-free-forest-battle-backgrounds\PNG\game_background_4\game_background_4.png"):
        # Screen dimensions
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

        # Load the map image
        self.map_image = pygame.image.load(map_image_path)
        self.battle_background_image = battle_background_image

        # Player and NPCs and Enemies data
        self.player_party = player_party
        self.party_members = self.player_party.members
        self.player = self.party_members[0]
        self.npcs = npcs
        self.enemies = enemies

        self.allow_encounters = allow_encounters # Toggle encounters
        self.encounter_rate = encounter_rate  # Probability per step (e.g., 0.05 = 5%)
        self.random_encounter_battle = False
        self.transitions = {}  # or a list
        if transitions:
            for trans in transitions:
                zone = trans["zone"]
                self.transitions[zone] = {
                    "map_id": trans["target"],
                    "player_x": trans["player_x"],
                    "player_y": trans["player_y"]
                }
        if map_scale_factor:
            self.map_image = pygame.transform.scale(self.map_image, (self.map_image.get_width()*map_scale_factor, self.map_image.get_height()*map_scale_factor))

        self.map_width = self.map_image.get_width()
        self.map_height = self.map_image.get_height()
        print("mapsize", self.map_width, self.map_height)

        # Camera position (top-left corner of the visible area)
        self.camera_x = 0
        self.camera_y = 0

        # BGM
        self.bgm = bgm
    

        self.shop_active = False
        self.current_npc = None

        self.guild_active = False
        self.adventure_guild = None

        self.battle_screen = False
        self.current_enemies = []

        self.text_manager = TextManager(screen)
        self.menu = Menu(self.screen, self.player_party)

        if layer_json_path:
            self.positions = self.parse_json_data(layer_json_path)
        else:
            self.positions = np.zeros((self.map_width, self.map_height))
        
        self.random_encounter_enemies = random_encounter_enemies
        

    def handle_random_encounter(self, player):
        """Triggers a random enemy encounter based on player's movement."""
        if self.allow_encounters and random.random() < self.encounter_rate:
            # Create a random enemy
            enemy_num = random.randint(1, 2)
            # enemy_list = ["Bat", "Bee", "Scorpion", "Slime", "Mouse", "Spider", "Snake(Green)", "Snake(Pink)"]
            for i in range(enemy_num):
                enemy_name = random.choice(self.random_encounter_enemies)
                enemy = Enemy(
                    name=enemy_name,
                    x = player.x,
                    y = player.y,
                    level=random.randint(1, 5),
                    hp=random.randint(20, 40),
                    mp=50,
                    atk=random.randint(10, 15),
                    dfn=random.randint(10, 11),
                    spd=random.randint(10, 11),
                    inventory={},
                    folder_paths=[
                        Rf"Monsters\{enemy_name}",
                    ]
                )
                self.current_enemies.append(enemy)
            self.battle_screen = True
            self.random_encounter_battle = True
            

    def parse_json_data(self, layer_json_path):
        with open(layer_json_path, 'r') as file:
            data = json.load(file)
       
        Positions = []
        total_x = data["map_width"]
        total_y = data["map_height"]
        Positions = np.zeros((total_x, total_y))
        for layer in data["layers"]:
            if layer["name"] == "Layer 2":
                for pos in layer["positions"]:
                    x = pos["x"]
                    y = pos["y"]
                    Positions[x][y] = 1
        for layer in data["layers"]:
            if layer["name"] == "Layer 3":
                for pos in layer["positions"]:
                    x = pos["x"]
                    y = pos["y"]
                    Positions[x][y] = 0
        scale =  self.map_width // total_x
        Positions = np.repeat(np.repeat(Positions, scale, axis=1), scale, axis=0)
        return Positions
    

    def draw(self, screen, events):
        """
        Draw the map and the player on the screen.
        The player is always centered, and the map moves accordingly.
        """
        # Calculate the offset for the map based on the camera position
        offset_x = -self.camera_x
        offset_y = -self.camera_y
        
        self.handle_npc_interaction(events)
        self.move_to_battle()
        
        if not self.shop_active:
            # Draw the map
            screen.blit(self.map_image, (offset_x, offset_y))
            self.draw_characters()
            add_menu(self.menu, events)
        
        if self.guild_active:
            self.adventure_guild.draw()
            
        self.text_manager.update()
        self.text_manager.draw()


    def draw_characters(self):
        # Sort characters by Y-coordinate (for proper layering)
        characters = [self.player] + self.npcs + self.enemies
        characters.sort(key=lambda char: char.draw_y)

        # Update Enemies coordinate
        if self.enemies != []:
            for enemy in self.enemies:
                enemy.draw_x = enemy.x - self.camera_x - (enemy.sprite.sprite_shape[enemy.sprite.current_animation]["width"] * enemy.sprite.scale_factor) // 2
                enemy.draw_y = enemy.y - self.camera_y - (enemy.sprite.sprite_shape[enemy.sprite.current_animation]["height"] * enemy.sprite.scale_factor) // 2
                
                # Calculate the distance between player and a Enemy for battle screen transition
                distance = ((self.player.draw_x - enemy.draw_x) ** 2 + (self.player.draw_y - enemy.draw_y) ** 2) ** 0.5  # Distance formula
                if distance < 200:  # Interaction range
                    self.battle_screen = True
                    self.current_enemies = [enemy]

        # Update the player coordinate
        self.player.draw_x = self.player.x - self.camera_x - (self.player.sprite.sprite_shape[self.player.sprite.current_animation]["width"] * self.player.sprite.scale_factor) // 2
        self.player.draw_y = self.player.y - self.camera_y - (self.player.sprite.sprite_shape[self.player.sprite.current_animation]["height"] * self.player.sprite.scale_factor) // 2

        # Update NPCs coordinates
        if self.npcs != []:
            for npc in self.npcs:
                npc.draw_x = npc.x - self.camera_x - (npc.sprite.sprite_shape[npc.sprite.current_animation]["width"] * npc.sprite.scale_factor) // 2
                npc.draw_y = npc.y - self.camera_y - (npc.sprite.sprite_shape[npc.sprite.current_animation]["height"] * npc.sprite.scale_factor) // 2
             
                # Calculate the distance between player and a npc for the interaction symbol display
                distance = ((self.player.draw_x - npc.draw_x) ** 2 + (self.player.draw_y - npc.draw_y) ** 2) ** 0.5  # Distance formula
                if distance < 130:  # Interaction range
                    npc.draw_interaction_symbol(self.screen)  # Show interaction symbol

        # Draw all the characters in order
        for char in characters:
            char.sprite.update_frame()
            char.sprite.draw(self.screen, char.draw_x, char.draw_y)
        

    def update_camera(self):
        """
        Update the camera position to keep the player centered.
        """
        # Calculate the desired camera position to center the player
        desired_camera_x = self.player.x - self.screen_width // 2
        desired_camera_y = self.player.y - self.screen_height // 2

        # Clamp the camera position to the map boundaries
        self.camera_x = max(0, min(desired_camera_x, self.map_width - self.screen_width))
        self.camera_y = max(0, min(desired_camera_y, self.map_height - self.screen_height))
        
        return None # No transition
    
    def clamp_player_position(self):
        """
        Clamp the player's position to ensure they don't move outside the map boundaries.
        """
        # Clamp player's X position
        self.player.x = max(0, min(self.player.x, self.map_width - self.player.sprite.sprite_shape[self.player.sprite.current_animation]["width"]))
        # Clamp player's Y position
        self.player.y = max(0, min(self.player.y, self.map_height - self.player.sprite.sprite_shape[self.player.sprite.current_animation]["height"]))         


    def add_transition_zone(self, x1, y1, x2, y2, target_map_id, new_x, new_y):
        """
        Define a transition zone where the player moves to a new map.
        Instead of passing a map object, we pass a map identifier.
        """
        self.transitions[(x1, y1, x2, y2)] = {"map_id": target_map_id, "player_x": new_x, "player_y": new_y}

    def check_transition(self):
        """
        Check if the player is in a transition zone.
        """
        # If the player party was defeated
        no_alive = True
        for player in self.player_party.members:
            if player.hp > 0:
                no_alive = False
        if no_alive:
            data = {
                "map_id": "inn_1F",
                "player_x": 680,
                "player_y": 490
                }
            for player in self.player_party.members:
                player.hp = player.max_hp
                player.mp = player.max_mp
            return data
        
        for (x1, y1, x2, y2), data in self.transitions.items():
            if x1 <= self.player.x <= x2 and y1 <= self.player.y <= y2:
                return data  # Return transition detail
        
        return None
    
    def handle_npc_interaction(self, events):
        """Checks if the player is near an NPC and starts a conversation."""
        keys = pygame.key.get_pressed()

        # Open the shop is shop_active is True
        if self.shop_active:  
            # While shop is open, only allow shop interactions
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Close shop on ESC
                        self.shop_active = False
                        self.player.can_move = True
                    else:
                        self.current_npc.shop.handle_event(event)  # Process shop input
            self.current_npc.shop.draw()  # Redraw shop screen
            return  # Prevent other interactions while in shop mode

        elif self.guild_active:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if not self.adventure_guild.selecting_quests and not self.adventure_guild.viewing_active_quests and not self.adventure_guild.viewing_complete_quests and event.key == pygame.K_ESCAPE:  # Close guild on ESC
                        self.guild_active = False
                        self.player.can_move = True
                    else:
                        self.adventure_guild.handle_input(event)
            

        # Deal with the interaction with NPCs
        for npc in self.npcs:
            distance = ((self.player.draw_x - npc.draw_x) ** 2 + (self.player.draw_y - npc.draw_y) ** 2) ** 0.5  # Distance formula
            if distance < 130:  # Interaction range
                # This line is not working and I dont know why so I added this in the map.py
                npc.draw_interaction_symbol(self.screen)  # Show interaction symbol

            # If the NPC is already talking, pressing Enter should go to next message
                if npc.talking:
                    if keys[pygame.K_RETURN]:  # Press 'Enter' to continue dialogue
                        self.player.can_move = False
                        if self.text_manager.waiting_for_next:
                            self.text_manager.next_message()  # Go to next line
                            if not self.text_manager.messages:  # If no messages left, stop talking
                                npc.talking = False
                                self.player.can_move = True

                                # Check if NPC is a shopkeeper and open the shop
                                if npc.shop_items:
                                    self.player.can_move = False
                                    self.shop_active = True
                                    self.current_npc = npc
                                    npc.shop = Shop(self.screen, self.player, npc.shop_items)
                                    return  # Exit to prevent further interactions

                                elif npc.guild:
                                    self.player.can_move = False
                                    self.guild_active = True
                                    self.current_npc = npc
                                    self.adventure_guild = AdventurerGuild(self.screen, self.player_party)
                                
                                elif npc.inn == True:
                                    for player in self.player_party.members:
                                        player.hp = player.max_hp
                                        player.mp = player.max_mp
                                    heal_sound = pygame.mixer.Sound(R"Sound_Effects\8_Buffs_Heals_SFX\heal.wav")  
                                    heal_sound.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
                                    heal_sound.play()


                    return  # Avoid multiple NPCs getting activated
             
                # Press 'E' to start the conversation
                if keys[pygame.K_e]:  
                    self.player.can_move = False
                    if not npc.talking:
                        npc.talking = True
                        npc.talk(self.text_manager, self.player, self.screen)
                        if npc.name == "Belle":
                            npc.has_talked = True
                        return   # Exit to prevent multiple interactions

                    break  # Stop checking other NPCs after talking to one
                
        return 
        

    def handle_shop_events(self, event):
        """Handle events when the shop is open."""
        if self.shop_active and self.current_npc and self.current_npc.shop:
            self.current_npc.shop.handle_event(event)


    def move_to_battle(self):
        if self.battle_screen and self.current_enemies:
            battle = Battle(self.screen, self.party_members, self.current_enemies, self.battle_background_image)
           
            result = battle.run()
            #revert_theme()
            # When the battle was the random encounter
            if self.random_encounter_battle:
                self.random_encounter_battle = False
                if result == "Victory":

                    # Check quest acheivement
                    if self.player_party.current_quests:
                        for quest in self.player_party.current_quests:
                            target = quest["objective"]["target"]
                            for enemy in self.current_enemies:
                                if target == enemy.name:
                                    quest["objective"]["count"] -= 1
                elif result == "Defeat":
                    pass

                elif result == "Escape":
                    pass


            else:
                if result == "Victory":
                    self.enemies.remove(self.current_enemies[0])
                    self.battle_screen = False  # Exit battle 

                    # Check quest acheivement
                    if self.player_party.current_quests:
                        for quest in self.player_party.current_quests:
                            target = quest["objective"]["target"]
                            for enemy in self.current_enemies:
                                if target == enemy.name:
                                    quest["objective"]["count"] -= 1

                elif result == "Defeat":
                    if self.player.current_direction == "right":
                        self.player.x -= 90  # Move player away to prevent instant re-entry
                    elif self.player.current_direction == "left":
                        self.player.x += 90  # Move player away to prevent instant re-entry
                    elif self.player.current_direction == "up":
                        self.player.y += 90  # Move player away to prevent instant re-entry
                    elif self.player.current_direction == "down":
                        self.player.y -= 90  # Move player away to prevent instant re-entry
               

                elif result == "Escape":
                    if self.player.current_direction == "right":
                        self.player.x -= 90  # Move player away to prevent instant re-entry
                    elif self.player.current_direction == "left":
                        self.player.x += 90  # Move player away to prevent instant re-entry
                    elif self.player.current_direction == "up":
                        self.player.y += 90  # Move player away to prevent instant re-entry
                    elif self.player.current_direction == "down":
                        self.player.y -= 90  # Move player away to prevent instant re-entry
            
            self.battle_screen = False  # Exit battle screen
            self.current_enemies = []

