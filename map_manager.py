import pygame
from text_manager import TextManager
from shop import Shop
from battle import Battle
from Draw import change_theme, revert_theme
from menu import Menu
from utilities import add_menu
import numpy as np
import json
from character import Enemy
import random


class Map:
    def __init__(self, screen, map_image_path, player, npcs=[], enemies=[], map_scale_factor=None, bgm=None, layer_json_path=False, allow_encounters=False, encounter_rate=0.01):
        # Screen dimensions
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

        # Load the map image
        self.map_image = pygame.image.load(map_image_path)

        # Player and NPCs and Enemies data
        self.player = player
        self.npcs = npcs
        self.enemies = enemies

        self.allow_encounters = allow_encounters # Toggle encounters
        self.encounter_rate = encounter_rate  # Probability per step (e.g., 0.05 = 5%)
        self.random_encounter_battle = False

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

        # Dictionary to store transition areas and target maps
        self.transitions = {}  # Format: {(x1, y1, x2, y2): {"map": target_map, "player_x": new_x, "player_y": new_y}}

        self.shop_active = False
        self.current_npc = None

        self.battle_screen = False
        self.current_enemy = None

        self.text_manager = TextManager(screen)
        self.menu = Menu(self.screen, self.player)

        if layer_json_path:
            self.positions = self.parse_json_data(layer_json_path)
        else:
            self.positions = np.zeros((self.map_width, self.map_height))
        

    def handle_random_encounter(self, player):
        """Triggers a random enemy encounter based on player's movement."""
        if self.allow_encounters and random.random() < self.encounter_rate:
            # Create a random enemy
            self.current_enemy = Enemy(
                name="Goblin",
                x = player.x,
                y = player.y,
                level=random.randint(1, 5),
                hp=random.randint(20, 50),
                mp=50,
                atk=random.randint(5, 10),
                dfn=random.randint(2, 5),
                spd=random.randint(3, 6),
                exp_reward=random.randint(10, 20),
                inventory={},
                loot=None,
                folder_paths=[
                    R".\timefantasy_characters\timefantasy_characters\frames\chara\chara4_5",
                    R".\tf_svbattle\singleframes\set4\5"
                ]
            )
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
                    Positions[x][y] = 1
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
        
        self.current_enemy
        self.handle_npc_interaction(events)
        self.move_to_battle()
    
        
        if not self.shop_active:
            # Draw the map
            screen.blit(self.map_image, (offset_x, offset_y))
            self.draw_characters()
            add_menu(self.menu, events)
            
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
                if distance < 70:  # Interaction range
                    self.battle_screen = True
                    self.current_enemy = enemy

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
                if distance < 60:  # Interaction range
                    npc.draw_interaction_symbol(self.screen)  # Show interaction symbol

        # Draw all the characters in order
        for char in characters:
            char.sprite.update_frame()
            char.sprite.draw(self.screen, char.draw_x, char.draw_y)
        

    def update_camera(self):
        """
        Update the camera position to keep the player centered.
        """
        # Check if the player should transition to another map
        transition_data = self.check_transition()
        if transition_data:
            return transition_data  # Return new map details to switch

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


    def add_transition_zone(self, x1, y1, x2, y2, target_map, new_x, new_y):
        """
        Define a transition zone where the player moves to a new map.
        """
        self.transitions[(x1, y1, x2, y2)] = {"map": target_map, "player_x": new_x, "player_y": new_y}

    def check_transition(self):
        """
        Check if the player is in a transition zone.
        """
        for (x1, y1, x2, y2), data in self.transitions.items():
            if x1 <= self.player.x <= x2 and y1 <= self.player.y <= y2:
                return data  # Return transition details
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

        # Deal with the interaction with NPCs
        for npc in self.npcs:
            distance = ((self.player.draw_x - npc.draw_x) ** 2 + (self.player.draw_y - npc.draw_y) ** 2) ** 0.5  # Distance formula
            if distance < 70:  # Interaction range
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
                    return  # Avoid multiple NPCs getting activated
             
                # Press 'E' to start the conversation
                if keys[pygame.K_e]:  
                    self.player.can_move = False
                    if not npc.talking:
                        npc.talking = True
                        npc.talk(self.text_manager, self.player, self.screen)
                        return   # Exit to prevent multiple interactions

                    break  # Stop checking other NPCs after talking to one
        return 
        

    def handle_shop_events(self, event):
        """Handle events when the shop is open."""
        if self.shop_active and self.current_npc and self.current_npc.shop:
            self.current_npc.shop.handle_event(event)


    def move_to_battle(self):
        if self.battle_screen and self.current_enemy:
            battle = Battle(self.screen, self.player, self.current_enemy, background_image=".\craftpix-net-270096-free-forest-battle-backgrounds\PNG\game_background_4\game_background_4.png")
            #change_theme("Music\BattleTheme.mp3")
            result = battle.run()

            # When the battle was the random encounter
            if self.random_encounter_battle:
                    self.random_encounter_battle = False
                    self.current_enemy = None

            if result == "win":
                if self.current_enemy:
                    self.enemies.remove(self.current_enemy)
                self.battle_screen = False  # Exit battle screen
                #revert_theme()
            elif result == "lose":
                self.battle_screen = False  # Exit battle screen
                if self.player.current_direction == "right":
                    self.player.x -= 60  # Move player away to prevent instant re-entry
                elif self.player.current_direction == "left":
                    self.player.x += 60  # Move player away to prevent instant re-entry
                elif self.player.current_direction == "up":
                    self.player.y += 60  # Move player away to prevent instant re-entry
                elif self.player.current_direction == "down":
                    self.player.y -= 60  # Move player away to prevent instant re-entry
                #revert_theme()
            elif result == "escape":

                self.battle_screen = False  # Exit battle screen
                if self.player.current_direction == "right":
                    self.player.x -= 60  # Move player away to prevent instant re-entry
                elif self.player.current_direction == "left":
                    self.player.x += 60  # Move player away to prevent instant re-entry
                elif self.player.current_direction == "up":
                    self.player.y += 60  # Move player away to prevent instant re-entry
                elif self.player.current_direction == "down":
                    self.player.y -= 60  # Move player away to prevent instant re-entry
                #revert_theme()
