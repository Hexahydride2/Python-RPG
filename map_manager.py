import pygame
from text_manager import TextManager
from shop import Shop
from battle import Battle
from Draw import change_theme, revert_theme
from menu import Menu
from utilities import add_menu


class Map:
    def __init__(self, screen, map_image_path, player=None, npcs=None, enemies=None, map_scale_factor=None, bgm=None):
        # Screen dimensions
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

        # Load the map image
        self.map_image = pygame.image.load(map_image_path)

        # Player and NPCs and Enemies data
        self.player = player
        self.npcs = npcs
        self.enemies = enemies

        if map_scale_factor:
            self.map_image = pygame.transform.scale(self.map_image, (self.map_image.get_width()*map_scale_factor, self.map_image.get_height()*map_scale_factor))

        self.map_width = self.map_image.get_width()
        self.map_height = self.map_image.get_height()

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
            


        self.text_manager.update()
        self.text_manager.draw()


    def draw_characters(self):
        # Draw the npcs on the screen
            if self.npcs:
                for npc in self.npcs:
                    npc.draw_x = npc.x - self.camera_x
                    npc.draw_y = npc.y - self.camera_y
                    npc.sprite.update_frame()
                    npc.sprite.draw(self.screen, npc.draw_x, npc.draw_y)

                    # Calculate the distance between player and a npc for the interaction symbol display
                    distance = ((self.player.draw_x - npc.draw_x) ** 2 + (self.player.draw_y - npc.draw_y) ** 2) ** 0.5  # Distance formula
                    if distance < 60:  # Interaction range
                        npc.draw_interaction_symbol(self.screen)  # Show interaction symbol        
            
            if self.enemies:
                for enemy in self.enemies:
                    enemy.draw_x = enemy.x - self.camera_x
                    enemy.draw_y = enemy.y - self.camera_y
                    enemy.sprite.update_frame()
                    enemy.sprite.draw(self.screen, enemy.draw_x, enemy.draw_y)

                    # Calculate the distance between player and a Enemy for battle screen transition
                    distance = ((self.player.draw_x - enemy.draw_x) ** 2 + (self.player.draw_y - enemy.draw_y) ** 2) ** 0.5  # Distance formula
                    if distance < 60:  # Interaction range
                        self.battle_screen = True
                        self.current_enemy = enemy

            # Draw the player at the center of the screen
            self.player.draw_x = self.player.x - self.camera_x - (self.player.sprite.sprite_shape[self.player.sprite.current_animation]["width"] * self.player.sprite.scale_factor) // 2
            self.player.draw_y = self.player.y - self.camera_y - (self.player.sprite.sprite_shape[self.player.sprite.current_animation]["height"] * self.player.sprite.scale_factor) // 2
            self.player.sprite.update_frame()
            self.player.sprite.draw(self.screen, self.player.draw_x, self.player.draw_y)

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
            if distance < 60:  # Interaction range
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
            if result == "win":
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
