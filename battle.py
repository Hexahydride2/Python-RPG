import pygame
import math
import pygame
import sys
from sprite import Sprite

class Battle:
    def __init__(self, screen, player, enemy):
        self.screen = screen
        self.player = player
        self.enemy = enemy
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        
        self.buttons = {  # Button positions and labels
            "Attack": pygame.Rect(100, 500, 150, 50),
            "Items": pygame.Rect(300, 500, 150, 50),
            "Escape": pygame.Rect(500, 500, 150, 50),
        }
        
        self.turn = "player"  # Tracks whose turn it is

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

        # Battle message variables
        self.battle_message = ""    # Battle message (e.g., who attacked and damage)
        self.message_timer = 0
        self.MESSAGE_DURATION = 60  # Display message for 60 frames

        # Attack and Knockback movement when attacking
        self.forward_distance = 190  # How much the character moves forward
        self.backward_distance = 20  # How much the character moves backward
        self.original_positions = {
            "player": (self.player_x, self.player_y),
            "enemy": (self.enemy_x, self.enemy_y)
        }

        self.font = pygame.font.Font(None, 30)  # Default font size for HP and MP
        self.level_font = pygame.font.Font(None, 30)  # Smaller font size for level display


    def draw_battle_message(self):
        """Display battle message on the screen."""
        if self.message_timer > 0:
            message_text = self.font.render(self.battle_message, True, (0, 0, 0))
            self.screen.blit(message_text, (220, 20))  # Display the message at the top
            self.message_timer -= 1  # Countdown timer
    
    def draw_buttons(self):
        for text, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (0, 0, 0), rect, border_radius=10)
            label = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(label, (rect.x + 30, rect.y + 10))
    
    def draw_characters(self):
        # Ensure correct facing direction
        self.player.sprite.is_flipped = False  # Player should always face right
        self.enemy.sprite.is_flipped = True  # Enemy should always face left

        # display Characters
        self.player.sprite.draw(self.screen, self.player_x, self.player_y)
        self.enemy.sprite.draw(self.screen, self.enemy_x, self.enemy_y)

        # Display Player and Enemy HP as text
        player_hp = self.font.render(f"HP: {self.player.hp}", True, (255, 0, 0))
        enemy_hp = self.font.render(f"HP: {self.enemy.hp}", True, (255, 0, 0))
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
        player_mp = self.font.render(f"MP: {self.player.mp}", True, (0, 0, 255))
        enemy_mp = self.font.render(f"MP: {self.enemy.mp}", True, (0, 0, 255))
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

        self.draw_battle_message()

    def attack(self):
        if self.is_attacking:
            return  # Prevent multiple attacks at once

        self.is_attacking = True
        self.attack_timer = 0  # Reset the timer
        
        if self.turn == "player":
            self.player.sprite.set_animation('Attack01')
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
            if self.attack_timer >= self.player.sprite.num_frames_dict['Attack01'] * self.player.sprite.animation_speed:
                
                if self.is_hurt:
                    
                    if self.hurt_timer >= self.enemy.sprite.num_frames_dict['Hurt'] * self.enemy.sprite.animation_speed:
                        self.is_hurt = False  # Reset hurt state
                        self.hurt_timer = 0
                        # Deal damage and switch turns
                        if self.turn == "player":      
                            self.enemy.hp -= self.player.attack(self.enemy) 
                            
                            # Set the battle message to display who attacked and the damage
                            damage = self.player.attack(self.enemy, take_damage_on=False)
                            self.battle_message = f"{self.player.name} attacked! {self.enemy.name} took {damage} damage."
                            self.message_timer = self.MESSAGE_DURATION  # Show the message for a limited time
                            
                            
                            self.player.sprite.set_animation('Idle')
                            self.enemy.sprite.set_animation('Idle')

                            if self.enemy.hp <= 0:
                                self.enemy.sprite.set_animation('Death')
                                self.enemy.sprite.force_last_frame()

                                # Keep the player idle
                                self.player.sprite.set_animation('Idle')
                                self.player.sprite.rescale(self.original_scale)
                                self.enemy.sprite.rescale(self.original_scale)
                                
                                return "win"
                            self.turn = "enemy"
                        
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
                            self.player.sprite.rescale(self.original_scale)
                            self.enemy.sprite.rescale(self.original_scale)
                            return "lose"
                        
                        elif self.enemy.hp <= 0:
                                self.player.sprite.rescale(self.original_scale)
                                self.enemy.sprite.rescale(self.original_scale)
                                return "win"
                        
                        self.turn = "player"  # Switch turn to player
                        self.enemy_x, self.enemy_y = self.original_positions["enemy"]  # Reset enemy position after attack
                        self.player_x, self.player_y = self.original_positions["player"]  # Reset player position after attack
                        self.is_attacking = False
                        self.attack_timer = 0
        return None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.buttons["Attack"].collidepoint(mouse_pos):
                self.attack()
    
            elif self.buttons["Escape"].collidepoint(mouse_pos):
                return "escape"
        return None
    
    def run(self):
        turn_delay = 1500
        turn_timer= 0

        running = True
        while running:
            self.screen.fill((200, 200, 200))  # Background color
            self.draw_characters()
            self.draw_buttons()

            # Update frames
            self.player.update()
            self.enemy.update()

            # Handle attack animation logic
            attack_result = self.update_attack_animation()
            if attack_result:
                return attack_result
            enemy_result = self.update_enemy_attack_animation()  # Handle the enemy's turn
            if enemy_result:
                return enemy_result  # Return result from enemy turn

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
                self.handle_event(event)


# Function to check if player collides with NPC
def check_collision(player_x, player_y, npc_x, npc_y, threshold=50):
    distance = math.sqrt((player_x - npc_x) ** 2 + (player_y - npc_y) ** 2)
    return distance < threshold