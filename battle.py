import pygame
import math
import pygame
import sys
from items import items_list

class Battle:
    def __init__(self, screen, player, enemy, background_image=None):
        self.screen = screen
        self.player = player
        self.enemy = enemy
        if background_image != None:
            self.background_image = pygame.image.load(background_image)  # Adjust the path as needed
            self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))
        else:
            self.background_image = background_image
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.turn_number = 1
        
        self.buttons = {  # Button positions and labels
            "Attack": pygame.Rect(50, 500, 100, 50),
            "Items": pygame.Rect(200, 500, 100, 50),
            "Status": pygame.Rect(350, 500, 100, 50),
            "Escape": pygame.Rect(500, 500, 100, 50),
        }

        # Items List
        self.All_Item_List = items_list()
    
        # Item button settings
        self.items_open = False  # Track if the item menu is open
        self.selected_item = None  # Store selected item
        self.item_window_rect = pygame.Rect(180, 180, 240, 200)  # Item window position
        self.item_close_button_rect = pygame.Rect(710, 350, 40, 30)  # Close button position

        # Status button settings
        self.status_open = False  # Track if the status window is open
        self.status_window_rect = pygame.Rect(180, 100, 300, 250)  # Position and size
        self.status_close_button_rect = pygame.Rect(450, 100, 30, 30)  # Close button
        
        # Tracks whose turn it is
        if self.player.spd >= self.enemy.spd:
           self.turn = "player"
           self.start = "player"
        else:
            self.turn = "enemy"
            self.start = "enemy"

        # Character positions
        self.player_x, self.player_y = 10, 100
        self.enemy_x, self.enemy_y = 300, 100
        self.player_hp_x, self.player_hp_y = 100, 70
        self.enemy_hp_x, self.enemy_hp_y = 500, 70

        # Set animation to idle
        self.player.sprite.set_animation('Idle')
        self.enemy.sprite.set_animation('Idle')

        # Scale sprites larger in battle
        self.original_scale = self.player.sprite.scale_factor
        self.player.sprite.rescale(5)
        self.enemy.sprite.rescale(5)

        # Attack Animation Timers
        self.attack_timer = 0
        self.hurt_timer = 0
        self.is_attacking = False
        self.is_hurt = False
        self.is_death = False

        # Battle message variables
        self.battle_message = ""    # Battle message (e.g., who attacked and damage)
        self.message_timer = 0
        self.MESSAGE_DURATION = 60  # Display message for 60 frames
        self.show_result = False
        self.battle_result = None

        # Attack and Knockback movement when attacking
        self.forward_distance = 190  # How much the character moves forward
        self.backward_distance = 20  # How much the character moves backward
        self.original_positions = {
            "player": (self.player_x, self.player_y),
            "enemy": (self.enemy_x, self.enemy_y)
        }

        self.font = pygame.font.Font(None, 27)  # Default font size for HP and MP
        self.item_font = pygame.font.Font(None, 25)
        self.level_font = pygame.font.Font(None, 27)  # Smaller font size for level display
    
    def use_item(self, item):
        """Use an item and display a message"""
        if self.All_Item_List[item]["type"] == "hp":
            if self.player.hp == self.player.max_hp:
                self.battle_message = f"{self.player.name}'s HP is already full!"
            else:
                self.battle_message = f"{self.player.name} used a {item}! +{self.All_Item_List[item]["effect"]} HP"
                self.player.use_item(item)
                self.manage_turn_change() # Change to the enemy turn after using an item
        elif self.All_Item_List[item]["type"] == "mp":
            if self.player.mp == self.player.max_mp:
                self.battle_message = f"{self.player.name}'s MP is already full!"
            else:
                self.battle_message = f"{self.player.name} used a {item}! +{self.All_Item_List[item]["effect"]} MP"
                self.player.use_item(item)
                self.manage_turn_change() # Change to the enemy turn after using an item
        self.message_timer = self.MESSAGE_DURATION

    def draw_items(self):
        """Draws the items menu when the Items button is clicked."""
        pygame.draw.rect(self.screen, (50, 50, 50), (50, 350, 700, 200), border_radius=10)
        y_offset = 360
        
        # Draw the close button (small red "X" in the corner)
        pygame.draw.rect(self.screen, (200, 0, 0), self.item_close_button_rect, border_radius=5)
        close_label = self.font.render("X", True, (255, 255, 255))
        self.screen.blit(close_label, (self.item_close_button_rect.x + 10, self.item_close_button_rect.y + 5))

        for item, count in self.player.inventory.items():
            item_text = f"{item} x{count} - {self.All_Item_List[item]["description"]}"
            label = self.item_font.render(item_text, True, (255, 255, 255))
            self.screen.blit(label, (100, y_offset))
            y_offset += 40

    def draw_status_window(self):
        """Displays player's current status in a popup window."""
        pygame.draw.rect(self.screen, (50, 50, 50), self.status_window_rect, border_radius=10)

        close_button = pygame.Rect(self.status_close_button_rect)
        pygame.draw.rect(self.screen, (255, 0, 0), close_button, border_radius=5)
        close_label = self.font.render("X", True, (255, 255, 255))
        self.screen.blit(close_label, (close_button.x + 10, close_button.y + 5))

        # Display player stats
        y_offset = 120
        status_texts = [
            f"Name: {self.player.name}",
            f"Level: {self.player.level}",
            f"HP: {self.player.hp}/{self.player.max_hp}",
            f"MP: {self.player.mp}/{self.player.max_mp}",
            f"Attack: {self.player.atk}",
            f"Defense: {self.player.dfn}",
            f"Speed: {self.player.spd}"
        ]

        for text in status_texts:
            label = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(label, (200, y_offset))
            y_offset += 30

    def draw_battle_message(self):
        """Display battle message on the screen."""
        if self.message_timer > 0:
            self.draw_rectangle(x=150, y=445, width=450, height=30, alpha=200, border_radius=10)
            message_text = self.font.render(self.battle_message, True, (255, 255, 255))
            self.screen.blit(message_text, (220, 450))  # Display the message at the bottom
            self.message_timer -= 1  # Countdown timer

    def draw_buttons(self):
        for text, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (0, 0, 0), rect, border_radius=10)
            label = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(label, (rect.x + 20, rect.y + 10))

        # Draw item window if open
        if self.items_open:
            self.draw_items()
        
        # Draw status window if open
        if self.status_open:
            self.draw_status_window()

    def draw_rectangle(self, x, y, width, height, alpha, border_radius):
        rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        #rect_surface.fill((0, 0, 0, 200))  # Black with transparency
        pygame.draw.rect(rect_surface, (0, 0, 0, alpha), (0, 0, width, height), border_radius=border_radius)
        self.screen.blit(rect_surface, (x, y))

    def draw_characters(self):
        # Ensure correct facing direction
        self.player.sprite.is_flipped = False  # Player should always face right
        self.enemy.sprite.is_flipped = True  # Enemy should always face left

        # display Characters
        self.player.sprite.draw(self.screen, self.player_x, self.player_y)
        self.enemy.sprite.draw(self.screen, self.enemy_x, self.enemy_y)

        # Draws a semi-transparent black rectangle for player window.
        self.draw_rectangle(x=75, y=50, width=250, height=150, alpha=200, border_radius=10)

        # Draws a semi-transparent black rectangle for enemy window.
        self.draw_rectangle(x=475, y=50, width=250, height=150, alpha=200, border_radius=10)

        # Draws a semi-transparent black rectangle for the turn number.
        self.draw_rectangle(x=5, y=565, width=120, height=30, alpha=200, border_radius=10)

        # Display Player and Enemy HP as text
        player_hp = self.font.render(f"HP: {self.player.hp}", True, (255, 255, 255))
        enemy_hp = self.font.render(f"HP: {self.enemy.hp}", True, (255, 255, 255))
        self.screen.blit(player_hp, (self.player_hp_x, self.player_hp_y))
        self.screen.blit(enemy_hp, (self.enemy_hp_x, self.enemy_hp_y))

        # Draw Player HP bar 
        player_hp_bar_width = 200  # Set the width of the HP bar
        player_hp_ratio = self.player.hp / self.player.max_hp  # Ratio of current HP to max HP
        pygame.draw.rect(self.screen, (170, 255, 0), pygame.Rect(self.player_hp_x, self.player_hp_y + 20, player_hp_bar_width * player_hp_ratio, 20))

        # Draw Enemy HP bar
        enemy_hp_bar_width = 200  # Set the width of the HP bar
        enemy_hp_ratio = self.enemy.hp / self.enemy.max_hp  # Ratio of current HP to max HP
        pygame.draw.rect(self.screen, (170, 255, 0), pygame.Rect(self.enemy_hp_x, self.enemy_hp_y + 20, enemy_hp_bar_width * enemy_hp_ratio, 20))

        # Display Player and Enemy MP as text
        player_mp = self.font.render(f"MP: {self.player.mp}", True, (255, 255, 255))
        enemy_mp = self.font.render(f"MP: {self.enemy.mp}", True, (255, 255, 255))
        self.screen.blit(player_mp, (self.player_hp_x, self.player_hp_y + 50))  # Position below HP
        self.screen.blit(enemy_mp, (self.enemy_hp_x, self.enemy_hp_y + 50))  # Position below HP

        # Draw Player MP bar (Blue)
        player_mp_bar_width = 200  # Set the width of the MP bar
        player_mp_ratio = self.player.mp / self.player.max_mp  # Ratio of current MP to max MP
        pygame.draw.rect(self.screen, (0, 150, 255), pygame.Rect(self.player_hp_x, self.player_hp_y + 70, player_mp_bar_width * player_mp_ratio, 20))

        # Draw Enemy MP bar (Blue)
        enemy_mp_bar_width = 200  # Set the width of the MP bar
        enemy_mp_ratio = self.enemy.mp / self.enemy.max_mp  # Ratio of current MP to max MP
        pygame.draw.rect(self.screen, (0, 150, 255), pygame.Rect(self.enemy_hp_x, self.enemy_hp_y + 70, enemy_mp_bar_width * enemy_mp_ratio, 20))

        # Display Player and Enemy Level
        player_level = self.level_font.render(f"Lvl: {self.player.level}", True, (255, 255, 0))
        enemy_level = self.level_font.render(f"Lvl: {self.enemy.level}", True, (255, 255, 0))
        self.screen.blit(player_level, (self.player_hp_x, self.player_hp_y + 100))  # Position below MP
        self.screen.blit(enemy_level, (self.enemy_hp_x, self.enemy_hp_y + 100))  # Position below MP

        # Display turn info
        turn_text = f"Turn {self.turn_number}: {self.player.name if self.turn=="player" else self.enemy.name}"
        turn_label = self.font.render(turn_text, True, (255, 255, 255))

        # Position: Bottom-left corner
        self.screen.blit(turn_label, (10, self.screen.get_height() - 30))

        self.draw_battle_message()

    def attack(self):
        if self.is_attacking:
            return  # Prevent multiple attacks at once

        self.is_attacking = True
        self.attack_timer = 0  # Reset the timer
        
        if self.turn == "player":
            self.player.sprite.set_animation('Attack03')
            self.enemy.sprite.set_animation('Hurt')
            self.player_x += self.forward_distance  # Player moves forward when attack
            self.enemy_x += self.backward_distance  # Enemy moves slightly backward when hit
            
        self.is_hurt = True  # Mark the character as hurt
        self.hurt_timer = 0  # Reset hurt timer

    def update_attack_animation(self):
        """Handle attack animation and transition back to idle."""
        if self.turn=="player" and self.is_attacking:
            self.attack_timer += 1
            self.hurt_timer += 1

            # Check if attack animation is completed
            attack_duration = self.player.sprite.num_frames_dict['Attack03'] * self.player.sprite.animation_speed
            hurt_duration = self.enemy.sprite.num_frames_dict['Hurt'] * self.enemy.sprite.animation_speed


            if self.attack_timer >= attack_duration and self.hurt_timer >= hurt_duration:
                if self.is_hurt:
                    
                    if self.hurt_timer >= self.enemy.sprite.num_frames_dict['Hurt'] * self.enemy.sprite.animation_speed:
                        self.is_hurt = False  # Reset hurt state
                        self.hurt_timer = 0
                        # Deal damage and switch turns
                        if self.turn == "player":      
                            self.enemy.hp -= self.player.attack(self.enemy) 
                            if self.enemy.hp <= 0:
                                self.enemy.hp = 0
                            
                            # Set the battle message to display who attacked and the damage
                            damage = self.player.attack(self.enemy, take_damage_on=False)
                            self.battle_message = f"{self.player.name} attacked! {self.enemy.name} took {damage} damage."
                            self.message_timer = self.MESSAGE_DURATION  # Show the message for a limited time
                            
                            
                            self.player.sprite.set_animation('Idle')
                            self.enemy.sprite.set_animation('Idle')

                            if self.enemy.hp <= 0:
                                self.enemy.sprite.set_animation('Death')
                                self.is_death = True

                                # Keep the player idle
                                self.player.sprite.set_animation('Idle')
                                self.player_x, self.player_y = self.original_positions["player"]
                                
                                return None
                            self.manage_turn_change()
                        
                        # Reset positions after attack animation
                        self.player_x, self.player_y = self.original_positions["player"]
                        self.enemy_x, self.enemy_y = self.original_positions["enemy"]
                        self.is_attacking = False
                        self.attack_timer = 0

        return None
    
    def enemy_attack(self):
        """Handles the enemy's turn automatically (movement, attack)."""
        if self.is_attacking:
            return  # Prevent multiple actions at once

        self.is_attacking = True  # Mark that the enemy is attacking
        self.attack_timer = 0  # Reset the timer for attack animation

        # Enemy automatically moves forward when attacking
        self.enemy.sprite.set_animation('Attack01')
        self.player.sprite.set_animation('Hurt')
        self.enemy_x -= self.forward_distance  # Move the enemy towards the player
        self.player_x -= self.backward_distance  # Move the player backward as they are hit

        # After attack animation ends, deal damage
        self.is_hurt = True  # Mark the player as hurt
        self.hurt_timer = 0  # Reset the hurt timer

    def update_enemy_attack_animation(self):
        """Manages the enemy's turn with animation and damage."""

        # Update attack and hurt animations
        if self.turn=="enemy" and self.is_attacking:
            self.attack_timer += 1
            self.hurt_timer += 1
            if self.attack_timer >= self.enemy.sprite.num_frames_dict['Attack01'] * self.enemy.sprite.animation_speed:
                if self.is_hurt:
                    if self.hurt_timer >= self.player.sprite.num_frames_dict['Hurt'] * self.player.sprite.animation_speed:
                        self.is_hurt = False  # Reset hurt state
                        self.hurt_timer = 0  # Reset hurt timer
                        # Deal damage and switch turns
                        self.player.hp -= self.enemy.attack(self.player)
        
                        # Set the battle message to display who attacked and the damage
                        damage = self.enemy.attack(self.player, take_damage_on=False)
                        self.battle_message = f"{self.enemy.name} attacked! {self.player.name} took {damage} damage."
                        self.message_timer = self.MESSAGE_DURATION  # Show the message for a limited time

                        self.enemy.sprite.set_animation('Idle')
                        self.player.sprite.set_animation('Idle')
                        if self.player.hp <= 0:
                            self.player.sprite.set_animation('Death')
                            self.is_death = True
                       
                            # Keep the player idle
                            self.enemy.sprite.set_animation('Idle')
                            self.player_x, self.player_y = self.original_positions["player"]
                            return None
                        
                        elif self.enemy.hp <= 0:
                            self.enemy.sprite.set_animation('Death')
                            self.is_death = True
                           
                            # Keep the player idle
                            self.player.sprite.set_animation('Idle')
                            self.player_x, self.player_y = self.original_positions["player"]    
                            return None
                        
                        self.manage_turn_change()  # Switch turn to player
                        self.enemy_x, self.enemy_y = self.original_positions["enemy"]  # Reset enemy position after attack
                        self.player_x, self.player_y = self.original_positions["player"]  # Reset player position after attack
                        self.is_attacking = False
                        self.attack_timer = 0
        return None

    def display_result_message(self):
        font = pygame.font.Font(None, 50)  # Load a font (default pygame font, size 50)

        # Determine the message based on game state
        if self.player.hp <= 0:
            message = "You Lost! Click to continue..."
            color = (255, 0, 0)  # Red color for losing
        elif self.enemy.hp <= 0:
            message = "You Won! Click to continue..."
            color = (0, 255, 0)  # Green color for winning
        else:
            return  # If no one has died, do nothing

        # Render the message
        text_surface = font.render(message, True, color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        # Draw a semi-transparent background box
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Black with 150 alpha (transparency)
        self.screen.blit(overlay, (0, 0))

        # Draw the text on screen
        self.screen.blit(text_surface, text_rect)

    def reset_original_state(self):
        self.player.sprite.rescale(self.original_scale)
        self.enemy.sprite.rescale(self.original_scale)
        self.player.sprite.set_animation("Walk")
        self.enemy.sprite.set_animation("Idle")

    def manage_turn_change(self):
        if self.turn == "player":
            self.turn = "enemy"
        elif self.turn == "enemy":
            self.turn = "player"
        # Mange turn number 
        if self.turn == self.start:
            self.turn_number += 1

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if self.status_open:
                # Close button functionality
                if self.status_close_button_rect.collidepoint(mouse_pos):
                    self.status_open = False # Close button menu
                    return # Exit early to prevent further processing

            if self.items_open:  # If item menu is open, detect clicks on items
                # Close button functionality
                if self.item_close_button_rect.collidepoint(mouse_pos):
                    self.items_open = False # Close button menu
                    return # Exit early to prevent further processing
                
                y_offset = 360
                for item, count in self.player.inventory.items():
                    item_rect = pygame.Rect(170, y_offset, 300, 30)
                    if item_rect.collidepoint(mouse_pos) and count > 0:
                        self.use_item(item)
                        self.items_open = False  # Close menu
                    y_offset += 40
                # Exclude an item from the inventory when it gets 0
                self.player.inventory = {key: value for key, value in self.player.inventory.items() if value > 0}

            if self.buttons["Attack"].collidepoint(mouse_pos):
                self.attack()

            elif self.buttons["Items"].collidepoint(mouse_pos):
                self.items_open = True  
            
            elif self.buttons["Status"].collidepoint(mouse_pos):
                self.status_open = True

            elif self.buttons["Escape"].collidepoint(mouse_pos):
                return "escape"
            return None
    
    def run(self):
        turn_delay = 1500
        turn_timer= 0

        running = True
        while running:
            if self.background_image == None:
                self.screen.fill((200, 200, 200))  # Background color
            else:
                self.screen.blit(self.background_image, (0, 0))  # Draw background first

            self.draw_characters()
            self.draw_buttons()

            # Check if anyone died
            if self.is_death == True:
                # Player died
                if self.player.hp <= 0:
                    self.battle_result = "lose"
                    self.enemy.sprite.force_last_frame()
                    self.enemy.update()
                    
                    if self.player.sprite.current_frame != (self.player.sprite.animation_speed * self.player.sprite.num_frames_dict['Death'] - 1):
                        self.player.update()         
                    else:
                        self.show_result = True  # Show result after player death motion

                # Enemy died
                elif self.enemy.hp <= 0:
                    self.battle_result = "win"
                    self.player.sprite.force_last_frame()
                    self.player.update()
                    
                    if self.enemy.sprite.current_frame != (self.enemy.sprite.animation_speed * self.enemy.sprite.num_frames_dict['Death'] - 1):
                        self.enemy.update()
                    else:
                        self.show_result = True  # Show result after enemy death motion
            else:
                self.player.update()
                self.enemy.update()

            if self.show_result:
                self.display_result_message()
                pygame.display.update()

                # Wait for user click to continue
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.player.sprite.rescale(self.original_scale)
                            self.enemy.sprite.rescale(self.original_scale)
                            waiting = False  # Exit wait loop on click
                            return self.battle_result
                self.show_result = False  # Reset the flag for the next battle

            # Handle attack animation logic
            attack_result = self.update_attack_animation()
            enemy_result = self.update_enemy_attack_animation()  # Handle the enemy's turn

            # If it's the player's turn, we track the timer for the delay
            if self.turn == "player":
                pygame.display.update()
                # Start the delay timer after the player's action
                turn_timer = pygame.time.get_ticks()  # Capture the current time in milliseconds

            # If it's the enemy's turn, wait until the delay has passed
            if self.turn == "enemy":
                elapsed_time = pygame.time.get_ticks() - turn_timer  # Get how much time has passed
                # If enough time has passed (delay is over), process the enemy's turn
                if elapsed_time >= turn_delay:
                    enemy_result = self.enemy_attack()  # Handle the enemy's turn
                    if enemy_result:
                        return enemy_result  # Return result from enemy turn

            pygame.display.update()
            self.clock.tick(30)  # Set FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                result = self.handle_event(event)
                if result == "escape":
                    self.reset_original_state()
                    return result


# Function to check if player collides with NPC
def check_collision(player_x, player_y, npc_x, npc_y, threshold=50):
    distance = math.sqrt((player_x - npc_x) ** 2 + (player_y - npc_y) ** 2)
    return distance < threshold