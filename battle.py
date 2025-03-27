import pygame
import random
#from character import Character, NPC, Enemy
from text_manager import TextManager
from items import items_list, attack_list, monster_exp_list, monster_drop_list
from utilities import change_theme

class Battle:
    def __init__(self, screen, player_party, enemies, background_image=None, escape_chance=0.5, boss_x=0, boss_y=0):
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.player_party = player_party
        self.player_party_alive = player_party.copy()
        self.enemies = enemies
        self.enemies_alive = self.enemies.copy()

        # Granual configuration for boss:
        self.boss_x, self.boss_y = boss_x, boss_y

        if background_image != None:
            self.background_image = pygame.image.load(background_image)  # Adjust the path as needed
            self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))
        else:
            self.background_image = background_image
        self.font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 28)  # Or use SysFont if installed
        self.escape_chance = escape_chance

        self.selected_option = 0
        self.options = ["Attack", "Defend", "Items", "Status", "Escape"]
        self.battle_over = False

        # Save and change animation
        # Scale sprites larger in battle
        self.current_position = {}
        self.initial_player_party_info = {}
        self.initial_enemies_info = {}
        
        self.save_initial_settings()

        # Turn system
        self.turn_num = 1
        self.action_order = []  # List of characters in order of their turns
        self.current_turn_index = 0  # Index of the current character taking a turn
        self.is_player_turn = False  # Whether it's the player's turn
        self.player_actions = {}  # Stores actions chosen by the player for each character
        self.enemy_actions = {}
        self.current_player_index = 0
        self.selected_enemy_index = 0

        # Attack selection state 
        self.selecting_attack = False
        self.selected_attack_index = 0
        self.attack_list = attack_list()

        # Item selection state
        self.selecting_item = False
        self.selected_item_index = 0
        self.items_scroll_offset = 0
        self.visible_items = 10
        self.items_list = items_list()
        self.selected_item_target_index = 0
        self.selecting_item_target = False

        self.battle_items = {}
        for item, count in self.player_party[0].inventory.items():
            if items_list()[item]["type"] != "dropped":
                self.battle_items[item] = count

        # Status window
        self.showing_status = False

        # Action execution state
        self.executing_actions = False
        self.current_action_index = 0
        #self.current_action_in_progress = False  # Track if an action is in progress
        self.action_changed_charas = []

        # Text Manager for battle message display
        self.text_manager = TextManager(self.screen, font_size=26)

        # Initialize turn order
        self.initialize_action_order()

        # Sound Effects
        # Load attack sound effect
        pygame.mixer.init()  # Initialize the mixer
        self.attack_sound = pygame.mixer.Sound(".\Sound_Effects\punch.mp3")  
        self.attack_sound.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
        self.gun_sound = pygame.mixer.Sound(".\Sound_Effects\gunshot.mp3")  
        self.gun_sound.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
        self.magic_sound = pygame.mixer.Sound(".\Sound_Effects\magic_spell.mp3")  
        self.magic_sound.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
        self.bow_sound = pygame.mixer.Sound(R".\Sound_Effects\bow.mp3")  
        self.bow_sound.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
        self.win_sound = pygame.mixer.Sound(R"Music\success-fanfare-trumpets.mp3")
        self.win_sound.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
        self.heal_sound = pygame.mixer.Sound(R"Sound_Effects\8_Buffs_Heals_SFX\heal.wav")
        self.heal_sound.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
        self.atk_buff_sound = pygame.mixer.Sound(R"Sound_Effects\8_Buffs_Heals_SFX\atk_buff.wav")
        self.atk_buff_sound.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
        self.dfn_buff_sound = pygame.mixer.Sound(R"Sound_Effects\8_Buffs_Heals_SFX\dfn_buff.wav")
        self.dfn_buff_sound.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
        self.spd_buff_sound = pygame.mixer.Sound(R"Sound_Effects\8_Buffs_Heals_SFX\spd_buff.wav")
        self.spd_buff_sound.set_volume(0.5)  # Adjust volume (0.0 to 1.0)

        # Key icons
        self.key_icons = {
        "up": pygame.image.load(R".\Icons\up_key.png"),
        "down": pygame.image.load(R".\Icons\down_key.png"),
        "left": pygame.image.load(R".\Icons\left_key.png"),
        "right": pygame.image.load(R".\Icons\right_key.png"),
        "enter": pygame.image.load(R".\Icons\enter_key.png"),
        "esc": pygame.image.load(R".\Icons\esc_key.png"),
        }
        for key in self.key_icons:
            self.key_icons[key] = pygame.transform.scale(self.key_icons[key], (40, 40))  # Adjust size
        
        # Save battle result
        self.result = None

        # Attack Effects
        self.active_effects = []

        # buff icons
        self.buff_icons = {
            "atk_buff": pygame.image.load(R"Icons\atk_buff.png"),
            "dfn_buff": pygame.image.load(R"Icons\dfn_buff.png"),
            "spd_buff": pygame.image.load(R"Icons\spd_buff.png")
        }

        for icon in self.buff_icons:
            self.buff_icons[icon] = pygame.transform.scale(self.buff_icons[icon], (25, 25))

        # battle music
        change_theme(R"Music/beyond-the-dark-battle-epic-orchestral-274992.mp3")


    def save_initial_settings(self):
        """Save initial state of each character and decide the location where it will be displayed"""
        # Scale sprites larger in battle
        player_start_x = int(self.screen.get_width() * 0.6)  # 70% from the left
        # Decides the start y location depends on the number of players
        if len(self.player_party) == 1:
            player_start_y = int(self.screen.get_height()//3)
        else:
            player_start_y = int(self.screen.get_height() // len(self.player_party) // 1.5)  # 20% from the top
        count = 1
        for i, player in enumerate(self.player_party):
            self.initial_player_party_info[player] ={"state": player.sprite.current_animation, "hp": player.hp, "mp": player.mp, "atk": player.atk, "dfn": player.dfn, "spd": player.spd, "x": None, "y": None, "scale_factor": player.sprite.scale_factor} 

            if player.hp == 0:
                player.sprite.set_animation("dead")
                self.player_party_alive.remove(player)
            else:
                player.sprite.set_animation("idle1")
            player.sprite.rescale(4)
            self.PLAYER_HEIGHT = player.sprite.sprite_shape[player.sprite.current_animation]["height"] 
            if count % 2 == 0:
                if not self.initial_player_party_info[player]["x"] and not self.initial_player_party_info[player]["y"]:
                    self.initial_player_party_info[player]["x"] = player_start_x
                    self.initial_player_party_info[player]["y"] = player_start_y + i * (self.PLAYER_HEIGHT + 40)
                    self.current_position[player] = {"x": player_start_x, "y": player_start_y + i * (self.PLAYER_HEIGHT + 40)}
            else:
                if not self.initial_player_party_info[player]["x"] and not self.initial_player_party_info[player]["y"]:
                    self.initial_player_party_info[player]["x"] = player_start_x - 50
                    self.initial_player_party_info[player]["y"] = player_start_y + i * (self.PLAYER_HEIGHT + 40)
                    self.current_position[player] = {"x": player_start_x - 50, "y": player_start_y + i * (self.PLAYER_HEIGHT + 40)}
            count += 1

        
        # Decides the start y location depends on the number of enemies
        enemy_start_x = int(self.screen.get_width() * 0.2)  # 10% from the left
        if len(self.enemies) == 1:
            enemy_start_y = int(self.screen.get_height()//3)
        else:
            enemy_start_y = int(self.screen.get_height() // len(self.enemies) // 1.5)

        count = 1
        for i, enemy in enumerate(self.enemies):
            self.initial_enemies_info[enemy] = {"state": enemy.sprite.current_animation, "hp": enemy.hp, "mp": enemy.mp, "atk": enemy.atk, "dfn": enemy.dfn, "spd": enemy.spd, "x": None, "y": None, "scale_factor": enemy.sprite.scale_factor}
            enemy.sprite.set_animation("idle1")
            enemy.sprite.rescale(4)
            enemy.sprite.is_flipped = True
            if count % 2 == 0:
                if not self.initial_enemies_info[enemy]["x"] and not self.initial_enemies_info[enemy]["y"]:
                    self.initial_enemies_info[enemy]["x"] = enemy_start_x 
                    self.initial_enemies_info[enemy]["y"] = enemy_start_y + i * (self.PLAYER_HEIGHT + 40)
                    self.current_position[enemy] = {"x": enemy_start_x, "y": enemy_start_y + i * (self.PLAYER_HEIGHT + 40)}
            else:
                if not self.initial_enemies_info[enemy]["x"] and not self.initial_enemies_info[enemy]["y"]:
                    self.initial_enemies_info[enemy]["x"] = enemy_start_x -50
                    self.initial_enemies_info[enemy]["y"] = enemy_start_y + i * (self.PLAYER_HEIGHT + 40)
                    self.current_position[enemy] = {"x": enemy_start_x - 50, "y": enemy_start_y + i * (self.PLAYER_HEIGHT + 40)}
            count += 1
    
    def initialize_action_order(self):
        """Initialize the turn order based on the speed of character"""

        all_characters = self.player_party_alive + self.enemies_alive
        # Sort characters by speed (highest speed first)
        self.action_order = sorted(all_characters, key=lambda x: x.spd, reverse=True)
    
    def draw(self):
        # Draw the background
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill((255, 255, 255))  # Clear screen with black

        self.draw_characters()
        if self.player_party_alive:
            self.draw_chara_window()

        # Draw effects
        self.draw_attack_effects()

        # Diplay the turn number on the top left
        font = pygame.font.Font(".\Fonts\RotisSerif-Bold.ttf", 30)
        turn_num_text = font.render(f'Turn: {self.turn_num}', True, (255, 255, 255))  # White text
        turn_num_text_border = font.render(f'Turn: {self.turn_num}', True, (0, 0, 0))  # Black border
        # Draw the black border by rendering the text multiple times with offsets
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                self.screen.blit(turn_num_text_border, (self.screen.get_width()*0.05 + dx, self.screen.get_height()*0.05 + dy))
        
        # Draw the white text on top
        self.screen.blit(turn_num_text, (self.screen.get_width()*0.05, self.screen.get_height()*0.05))

        # Display only the selection phase
        if not self.executing_actions and not self.text_manager.messages and self.player_party_alive:
            if self.selecting_attack:
                self.draw_attack_menu()
            elif self.selecting_item:
                self.draw_item_menu()
                if self.selecting_item_target:
                    self.draw_item_target_menu()
            elif self.showing_status:
                self.draw_status_menu()

            self.draw_aim_enemy()
            self.draw_navigation()

            # Draw options in the bottom left
            options_start_x = int(self.screen.get_width() * 0.05)  # 5% from the left
            options_start_y = int(self.screen.get_height() * 0.7)  # 80% from the top

            self.draw_rectangle(options_start_x - 20, options_start_y - 10, self.screen.get_width()*0.1, self.screen.get_height()*0.3, alpha=200, border_radius=10)
            pygame.draw.rect(self.screen, (245, 245, 245), (options_start_x - 20, options_start_y - 10, self.screen.get_width()*0.1, self.screen.get_height()*0.3), width=2, border_radius=10) # Border

            for i, option in enumerate(self.options):
                color = (255, 255, 255) if i == self.selected_option else (128, 128, 128)
                text = self.font.render(option, True, color)
                self.screen.blit(text, (options_start_x, options_start_y + i * 40))

        
        # Draw battle messages
        self.text_manager.draw()
    
    def draw_navigation(self):
        """Draws the navigation guide on the screen."""
        nav_x = self.screen.get_width()*0.5  # X position
        nav_y = self.screen.get_height() - 80  # Position near bottom
        font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 20)

        spacing = 100  # Space between key icons

        nav_items = [
            ("up", "Scroll"), 
            ("down", "Scroll"), 
            ("left", "Aim"), 
            ("right", "Aim"), 
            ("enter", "Select"), 
            ("esc", "Back")
        ]

        for key, label in nav_items:
            rect_surface = pygame.Surface((36, 36), pygame.SRCALPHA)
            pygame.draw.rect(rect_surface, (255, 255, 255, 255), (0, 0, 36, 36), border_radius=5)
            self.screen.blit(rect_surface, (nav_x + 2, nav_y + 1))

            self.screen.blit(self.key_icons[key], (nav_x, nav_y))  # Draw icon
            text = font.render(label, True, (255, 255, 255))  # Render text
            self.screen.blit(text, (nav_x + 40, nav_y + 5))  # Offset text next to icon
            nav_x += spacing  # Move to the right for next icon

    def draw_chara_window(self):
        """Draw HP and MP bars for the player party."""
        bar_width = 200  # Width of the HP/MP bars
        bar_height = 10  # Height of the HP/MP bars
        start_x = self.screen.get_width() - bar_width - 40  # Right side of the screen
        start_y = self.screen.get_height() * 0.2

        # Font for displaying text
        font = pygame.font.Font('.\Fonts\Montserrat-SemiBold.ttf', 16)
        name_font = pygame.font.Font('.\Fonts\Rotisserif-Bold.ttf', 22)

        chara_window_y_pos = {}

        for i, player in enumerate(self.player_party):
            # Calculate bar positions
            bar_y = start_y + i * (bar_height + self.screen.get_height()//6)  # Spacing between bars
            chara_window_y_pos[player] = bar_y

            # Draw character name with black border
            name_text = name_font.render(player.name, True, (255, 255, 255))  # White text
            name_text_border = name_font.render(player.name, True, (0, 0, 0))  # Black border

            # Draw the black border by rendering the text multiple times with offsets
            for dx in [-1, 1]:
                for dy in [-1, 1]:
                    self.screen.blit(name_text_border, (start_x + bar_width - 70 + dx, bar_y - 40 + dy))
            
            # Draw the white text on top
            self.screen.blit(name_text, (start_x + bar_width - 70, bar_y - 40))

            # Draw buff icons
            self.draw_buff_icons(player, start_x+10, bar_y-30)


            # Draw HP bar
            hp_ratio = player.hp / player.max_hp
            pygame.draw.rect(self.screen, (30, 30, 30), (start_x, bar_y, bar_width, bar_height), border_radius=10)  # Red background
            pygame.draw.rect(self.screen, (30, 255, 30), (start_x, bar_y, bar_width * hp_ratio, bar_height), border_radius=10)  # Green filled
            pygame.draw.rect(self.screen, (10, 10, 10), (start_x, bar_y, bar_width, bar_height), width=2, border_radius=10) # Border

            # Draw MP bar
            mp_ratio = player.mp / player.max_mp
            pygame.draw.rect(self.screen, (30, 30, 30), (start_x, bar_y + bar_height + 5, bar_width, bar_height), border_radius=10)  # Blue background
            pygame.draw.rect(self.screen, (30, 255, 255), (start_x, bar_y + bar_height + 5, bar_width * mp_ratio, bar_height), border_radius=10)  # Cyan filled
            pygame.draw.rect(self.screen, (10, 10, 10), (start_x, bar_y + bar_height + 5, bar_width, bar_height), width=2, border_radius=10) # Border

            # Draw character HP with black border
            hp_text = font.render("HP", True, (30, 255, 30))  # White text
            hp_text_border = font.render("HP", True, (0, 0, 0))  # Black border
            # Draw the black border by rendering the text multiple times with offsets
            for dx in [-1, 1]:
                for dy in [-1, 1]:
                    self.screen.blit(hp_text_border, (start_x - 20 + dx, bar_y - 10 + dy))
            # Draw the white text on top
            self.screen.blit(hp_text, (start_x - 20, bar_y - 10))

            # Draw character HP number with black border
            hp_num = font.render(str(player.hp), True, (255, 255, 255))  # White text
            hp_num_border = font.render(str(player.hp), True, (0, 0, 0))  # Black border
            # Draw the black border by rendering the text multiple times with offsets
            for dx in [-1, 1]:
                for dy in [-1, 1]:
                    self.screen.blit(hp_num_border, (start_x - 30 + bar_width + dx, bar_y - 15 + dy))
            # Draw the white text on top
            self.screen.blit(hp_num, (start_x + bar_width - 30, bar_y - 15))

            # Draw character MP with black border
            mp_text = font.render("MP", True, (30, 255, 255))  # White text
            mp_text_border = font.render("MP", True, (0, 0, 0))  # Black border
            # Draw the black border by rendering the text multiple times with offsets
            for dx in [-1, 1]:
                for dy in [-1, 1]:
                    self.screen.blit(mp_text_border, (start_x - 20 + dx, bar_y + 10 + dy))
            # Draw the white text on top
            self.screen.blit(mp_text, (start_x - 20, bar_y + 10))

            # Draw character MP with black border
            mp_num = font.render(str(player.mp), True, (255, 255, 255))  # White text
            mp_num_border = font.render(str(player.mp), True, (0, 0, 0))  # Black border
            # Draw the black border by rendering the text multiple times with offsets
            for dx in [-1, 1]:
                for dy in [-1, 1]:
                    self.screen.blit(mp_num_border, (start_x + bar_width - 30 + dx, bar_y + 5 + dy))
            # Draw the white text on top
            self.screen.blit(mp_num, (start_x + bar_width - 30, bar_y + 5))

        if not self.executing_actions:
            y = chara_window_y_pos[self.player_party_alive[self.current_player_index]]
            # Highlight the current player's stats window
            # Create a semi-transparent white surface
            highlight_surface = pygame.Surface((bar_width + 220, bar_height * 2 + 60), pygame.SRCALPHA)
            pygame.draw.rect(highlight_surface, (255, 255, 255, 128), (0, 0, bar_width + 80, bar_height * 2 + 60), border_radius=15)  # White with 50% transparency
            self.screen.blit(highlight_surface, (start_x - 50, y - 40))  # Position the highlight
            pygame.draw.rect(self.screen, (245, 245, 245), (start_x - 50, y - 40, bar_width + 80, bar_height * 2 + 60), width=2, border_radius=10) # Border

    def draw_characters(self):
        # Draw enemies on the left side
        for enemy in self.enemies:
            enemy.sprite.draw(self.screen, self.current_position[enemy]["x"] + self.boss_x, self.current_position[enemy]["y"] + self.boss_y)

        # Draw player party on the right side
        for player in self.player_party:
            player.sprite.draw(self.screen, self.current_position[player]["x"], self.current_position[player]["y"])   

    def draw_attack_menu(self):
        # Draw the attack selection menu
        current_player = self.player_party_alive[self.current_player_index]
        menu_width = int(self.screen.get_width() * 0.5)  # 50% of screen width
        menu_height = int(self.screen.get_height() * 0.6)  # 60% of screen height
        menu_x = int(self.screen.get_width() * 0.3)  # 30% from the left
        menu_y = int(self.screen.get_height() * 0.2)  # 20% from the top
        # Draw the left pane (attack names)
        left_pane_width = int(menu_width * 0.5)  # 50% of menu width
        left_pane_x = menu_x
        left_pane_y = menu_y
        self.draw_rectangle(left_pane_x, left_pane_y, left_pane_width, menu_height, alpha=200, border_radius=10)
        pygame.draw.rect(self.screen, (245, 245, 245), (left_pane_x, left_pane_y, left_pane_width, menu_height,), width=2, border_radius=10) # Border

        # Draw the right pane (attack description)
        right_pane_width = int(menu_width * 0.5)  # 50% of menu width
        right_pane_x = left_pane_x + left_pane_width + 10
        right_pane_y = menu_y
        self.draw_rectangle(right_pane_x, right_pane_y, right_pane_width, menu_height, alpha=200, border_radius=10)
        pygame.draw.rect(self.screen, (245, 245, 245), (right_pane_x, right_pane_y, right_pane_width, menu_height,), width=2, border_radius=10) # Border

        attack_menu_font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 24)  # Or use SysFont if installed
        # Draw attack names in the left pane
        for i, attack_name in enumerate(current_player.skills):
            color = (255, 255, 255) if i == self.selected_attack_index else (128, 128, 128)
            text = attack_menu_font.render(attack_name + f' (MP {self.attack_list[attack_name]["mp"]})', True, color)
            self.screen.blit(text, (left_pane_x + 10, left_pane_y + 10 + i * 40))
        # Draw attack description in the right pane
        selected_attack = current_player.skills[self.selected_attack_index]
        attack_info = self.attack_list[selected_attack]
        description = attack_info["description"]
        description_lines = self.wrap_text(description, right_pane_width - 20)
        for i, line in enumerate(description_lines):
            text = attack_menu_font.render(line, True, (255, 255, 255))
            self.screen.blit(text, (right_pane_x + 10, right_pane_y + 10 + i * 40))

    def draw_item_menu(self):
        # Draw item selection menu
        item_list_width, item_list_height = self.screen.get_width()*0.25, self.screen.get_height()*0.6
        base_x, base_y = self.screen.get_width()*0.25, self.screen.get_height()*0.2
        # Draw item list section and description section
        self.draw_rectangle(base_x, base_y, item_list_width, item_list_height, alpha=200, border_radius=10)
        pygame.draw.rect(self.screen, (245, 245, 245), (base_x, base_y, item_list_width, item_list_height), width=2, border_radius=10) # Border
        self.draw_rectangle(base_x + item_list_width +10, base_y, item_list_width, item_list_height, alpha=200, border_radius=10)
        pygame.draw.rect(self.screen, (245, 245, 245), (base_x + item_list_width +10, base_y, item_list_width, item_list_height), width=2, border_radius=10) # Border

        item_font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 24)

        items = list(self.battle_items)
        inventory = self.battle_items

        for i in range(self.items_scroll_offset, min(self.items_scroll_offset + self.visible_items, len(items))):
            item = items[i]
            possession = inventory[item]
            color = (255, 255, 0) if i == self.selected_item_index else (255, 255, 255)
            text = item_font.render(f'{item} x {possession}', True, color)
            self.screen.blit(text, (base_x+10, base_y+10 + (i - self.items_scroll_offset) * 40))

        selected_item = items[self.selected_item_index]
        wrapped_description = self.wrap_text(self.items_list[selected_item]["description"], item_list_width -20)

        for i, line in enumerate(wrapped_description):
            description_text = item_font.render(line, True, (255,255,255))
            self.screen.blit(description_text, (base_x + item_list_width + 20, base_y + 10 + i*30))

        
        # Draw scrollbar if necessary
        total_items = len(items)
        inventory_x, inventory_y = base_x, base_y
        inventory_height = item_list_height
        inventory_width = item_list_width
        scrollbar_width = 10
        self.max_scroll = max(0, total_items - self.visible_items)
        
        scrollbar_x = inventory_x + inventory_width - 15  # Right edge for the scrollbar
        if total_items > self.visible_items:
            # Scroll indicator height
            scroll_indicator_height = max(30, (self.visible_items / total_items) * inventory_height)

            # Scroll indicator position (proportional to scroll offset)
            scroll_indicator_y = inventory_y + (self.items_scroll_offset / self.max_scroll) * (inventory_height - scroll_indicator_height)

            # Draw scroll indicator
            pygame.draw.rect(self.screen, (255, 255, 255), (scrollbar_x, scroll_indicator_y, scrollbar_width, scroll_indicator_height), border_radius=5)
    
    def draw_item_target_menu(self):
        menu_width, menu_height = self.screen.get_width()*0.1, self.screen.get_height()*0.25
        x, y = self.screen.get_width()*0.6, self.screen.get_height()*0.4

        self.draw_rectangle(x, y, menu_width, menu_height, alpha=200, border_radius=10)
        pygame.draw.rect(self.screen, (245, 245, 245), (x, y, menu_width, menu_height), width=2, border_radius=10) # Border

        font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 24)  # Or use SysFont if installed
        # Draw attack names in the left pane
        for i, player in enumerate(self.player_party):
            if i == self.selected_item_target_index:
                if player in self.player_party_alive:
                    color = (255, 255, 255)
                else:
                    color = (255, 30, 30)
            else:
                if player in self.player_party_alive:
                    color = (128, 128, 128)
                else:
                    color =  (196, 30, 58)                    
            
            text = font.render(player.name, True, color)
            self.screen.blit(text, (x + 10, y + 10 + i * 40))

    def draw_status_menu(self):
        window_width = self.screen.get_width() * 0.2
        window_height = self.screen.get_height() * 0.6
        start_x = self.screen.get_width() * 0.15
        start_y = self.screen.get_height() * 0.2
        stat_font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 24)

        for i, player in enumerate(self.player_party):
            self.draw_rectangle(start_x + i*(window_width+10), start_y, window_width, window_height, 200, 10)
            pygame.draw.rect(self.screen, (245, 245, 245), (start_x + i*(window_width+10), start_y, window_width, window_height), width=2, border_radius=10) # Border

            text = stat_font.render(f'Name: {player.name}', True, (255,255,255))
            self.screen.blit(text, (start_x + i*(window_width+10) + 20, start_y + 10))

            text = stat_font.render(f'Lv. {player.level}', True, (255,255,255))
            self.screen.blit(text, (start_x + i*(window_width+10) + 20, start_y + 50))

            text = stat_font.render(f'HP: {player.hp}/{player.max_hp}', True, (255,255,255))
            self.screen.blit(text, (start_x + i*(window_width+10) + 20, start_y + 90))

            text = stat_font.render(f'MP: {player.mp}/{player.max_mp}', True, (255,255,255))
            self.screen.blit(text, (start_x + i*(window_width+10) + 20, start_y + 130))

            text = stat_font.render(f'ATK: {player.atk}', True, (255,255,255))
            self.screen.blit(text, (start_x + i*(window_width+10) + 20, start_y + 170))

            text = stat_font.render(f'DEF: {player.dfn}', True, (255,255,255))
            self.screen.blit(text, (start_x + i*(window_width+10) + 20, start_y + 210))

            text = stat_font.render(f'SPD: {player.spd}', True, (255,255,255))
            self.screen.blit(text, (start_x + i*(window_width+10) + 20, start_y + 250))

            text = stat_font.render(f'EXP: {player.exp}/{player.exp_to_next_level}', True, (255,255,255))
            self.screen.blit(text, (start_x + i*(window_width+10) + 20, start_y + 290))

    def draw_rectangle(self, x, y, width, height, alpha, border_radius):
        rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(rect_surface, (10, 10, 10, alpha), (0, 0, width, height), border_radius=border_radius)
        self.screen.blit(rect_surface, (x, y))

    def wrap_text(self, text, max_width):
        """Wrap text to fit within a specified width."""
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            test_width, _ = self.font.size(test_line)
            if test_width <= max_width:
                current_line = test_line
            else:

                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines
    
    def draw_aim_enemy(self):
        # Draw options in the bottom left
        options_start_x = int(self.screen.get_width() * 0.05)  # 5% from the left
        options_start_y = int(self.screen.get_height() * 0.2)  # 80% from the top
        for i, enemy in enumerate(self.enemies_alive):
            color = (255, 255, 255) if i == self.selected_enemy_index else (128, 128, 128)
            text = self.font.render(enemy.name, True, color)
            self.screen.blit(text, (options_start_x, options_start_y + i * 40))
    
    def draw_buff_icons(self, player, x, y):
        i = 0
        atk_buff_displayed, dfn_buff_displayed, spd_buff_displayed = False, False, False

        
        for buff in player.buffs:
            if not atk_buff_displayed and buff["type"] == "atk_buff":
                self.screen.blit(self.buff_icons["atk_buff"], (x+(i*30), y))
                atk_buff_displayed = True
            elif not dfn_buff_displayed and buff["type"] == "dfn_buff":
                self.screen.blit(self.buff_icons["dfn_buff"], (x+(i*30), y))
                dfn_buff_displayed = True
            elif not spd_buff_displayed and buff["type"] == "spd_buff":
                self.screen.blit(self.buff_icons["spd_buff"], (x+(i*30), y))
            i += 1

    def draw_attack_effects(self):
        """Draw attack effects on the screen."""
        if hasattr(self, "active_effects"):
            for effect in self.active_effects:
                if effect["index"] < len(effect["frames"]):
                    self.screen.blit(effect["frames"][effect["index"]], effect["position"])
                    effect["timer"] += 1
                    if effect["timer"] % 2 == 0:  # Adjust speed of animation
                        effect["index"] += 1
                else:
                    self.active_effects.remove(effect)  # Remove finished effects

    def add_attack_effect(self, target, element):
        """Trigger an attack effect animation at the target's position."""
        effect_frames = [pygame.image.load(fR".\SE\Single\{element}\frame({i}).png") for i in range(1, 21)]
        effect_position = (self.current_position[target]["x"], self.current_position[target]["y"])
        effect_animation = {"frames": effect_frames, "index":0, "position": effect_position, "timer":0}

        # Store the effect in a list
        if not hasattr(self, "active_effects"):
            self.active_effects = []
        self.active_effects.append(effect_animation)
    
    
    def is_animation_complete(self, character):
        """Check if the current animation has finished playing."""
        if character.sprite.current_animation in character.sprite.animations:
            num_frames = len(character.sprite.animations[character.sprite.current_animation]) * character.sprite.animation_speed
            return character.sprite.current_frame >= num_frames - 1
        return True
    
    def is_animation_finish(self, character):
        if character.sprite.current_animation != "idle1" and character.sprite.current_animation != "idle2":
            return character.sprite.current_frame >= character.sprite.num_frames_dict[character.sprite.current_animation] * character.sprite.animation_speed - 1
        else:
            return True

    def update(self):
        # Update animations for all characters and enemies
        for player in self.player_party:     
            if "idle" not in player.sprite.current_animation and player.sprite.current_frame >= player.sprite.num_frames_dict[player.sprite.current_animation] * player.sprite.animation_speed - 1:
                player.sprite.current_frame -= 1
            player.sprite.update_frame()  # Update player animation frame
        for enemy in self.enemies:
            if "idle" not in enemy.sprite.current_animation and enemy.sprite.current_frame >= enemy.sprite.num_frames_dict[enemy.sprite.current_animation] * enemy.sprite.animation_speed - 1:
                enemy.sprite.current_frame -= 1
            enemy.sprite.update_frame()  # Update enemy animation frame
            # print(enemy.sprite.current_animation, enemy.sprite.current_frame)


        if self.executing_actions:
            self.execute_actions()
        
        # Update text manager
        self.text_manager.update()

        # Check if the battle finished
        if self.battle_over:
            if not self.text_manager.messages:
                self.running = False
                return self.result
        else:
            self.check_battle_over()
    

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.text_manager.messages:
                if event.key == pygame.K_RETURN:
                        if not self.text_manager.message_finished:
                            self.text_manager.skipping = True  # Skip typewriter effect
                        elif self.text_manager.waiting_for_next:
                            self.text_manager.next_message()
            else:
                if not self.battle_over:
                    if not self.executing_actions:

                        # Attack skill selection input
                        if self.selecting_attack:
                            if event.key == pygame.K_DOWN:
                                self.selected_attack_index = (self.selected_attack_index + 1) % len(self.player_party_alive[self.current_player_index].skills)
                            elif event.key == pygame.K_UP:
                                self.selected_attack_index = (self.selected_attack_index - 1) % len(self.player_party_alive[self.current_player_index].skills)
                            elif event.key == pygame.K_RETURN:
                                if self.text_manager.messages == []:
                                    self.store_selected_attack_skill()
                                elif not self.text_manager.message_finished:
                                    self.text_manager.skipping = True  # Skip typewriter effect
                                elif self.text_manager.waiting_for_next:
                                    self.text_manager.next_message()
                            elif event.key == pygame.K_ESCAPE:
                                self.selecting_attack = False

                        # Target selection window after choosing item
                        elif self.selecting_item and self.selecting_item_target:
                            if event.key == pygame.K_DOWN:
                                self.selected_item_target_index = (self.selected_item_target_index + 1) % len(self.player_party)
                            elif event.key == pygame.K_UP:
                                self.selected_item_target_index = (self.selected_item_target_index - 1) % len(self.player_party)
                            elif event.key == pygame.K_RETURN:
                                self.store_selected_item()
                            elif event.key == pygame.K_ESCAPE:
                                self.selecting_item_target = False

                        # Item selection input
                        elif self.selecting_item:
                            if event.key == pygame.K_DOWN:
                                if self.selected_item_index < len(self.player_party_alive[self.current_player_index].inventory) - 1:
                                    self.selected_item_index += 1
                                    if self.selected_item_index >= self.items_scroll_offset + self.visible_items:
                                        self.items_scroll_offset += 1
                            elif event.key == pygame.K_UP:
                                if self.selected_item_index > 0:
                                    self.selected_item_index -= 1
                                    if self.selected_item_index < self.items_scroll_offset:
                                        self.items_scroll_offset -= 1
                            elif event.key == pygame.K_RETURN:
                                self.selecting_item_target = True
                                #self.store_selected_item()
                            elif event.key == pygame.K_ESCAPE:
                                self.selecting_item = False
                                self.selected_item_index = 0
                                self.items_scroll_offset = 0

                        elif self.showing_status:
                            if event.key == pygame.K_ESCAPE:
                                self.showing_status = False

                        # Basic option input (Attack, Defend, Item, Escape)
                        else:    
                            if event.key == pygame.K_DOWN:
                                self.selected_option = (self.selected_option + 1) % len(self.options)
                            elif event.key == pygame.K_UP:
                                self.selected_option = (self.selected_option - 1) % len(self.options)
                            elif event.key == pygame.K_RETURN:
                                self.select_option()
                            elif event.key == pygame.K_ESCAPE:
                                if self.current_player_index > 0:
                                    self.current_player_index -= 1

                        # Aim Enemy (Works in all selection phase)
                        if event.key == pygame.K_LEFT:
                            self.selected_enemy_index = (self.selected_enemy_index + 1) % len(self.enemies_alive)
                        elif event.key == pygame.K_RIGHT:
                            self.selected_enemy_index = (self.selected_enemy_index - 1) % len(self.enemies_alive)
                    # Action phase (only accept ENTER for text message)
                    else:
                        if event.key == pygame.K_RETURN:
                            if not self.text_manager.message_finished:
                                self.text_manager.skipping = True  # Skip typewriter effect
                            elif self.text_manager.waiting_for_next:
                                self.text_manager.next_message()
                # Result message after battle
                else:
                    if event.key == pygame.K_RETURN:
                            if not self.text_manager.message_finished:
                                self.text_manager.skipping = True  # Skip typewriter effect
                            elif self.text_manager.waiting_for_next:
                                self.text_manager.next_message()

    def select_option(self):
        """Store the selected action for the current player."""
        current_player = self.player_party_alive[self.current_player_index]
        selected_action = self.options[self.selected_option]
        
        if selected_action == "Attack":
            self.selecting_attack = True
            self.selected_attack_index = 0
        elif selected_action == "Items":
            self.selecting_item = True
            self.selected_item_index = 0
        elif selected_action == "Status":
            self.showing_status = True
        elif selected_action == "Defend":
            self.select_defense()
        elif selected_action == "Escape":
            self.select_escape()
    
    def select_escape(self):
        if self.escape_chance == 0:
            self.text_manager.add_message("The boss's overwhelming presence makes escape impossible!")
        else:
            if random.random() <= self.escape_chance:
                self.battle_over = True
                self.end_battle(result="Escaped")
            else:
                self.text_manager.add_message("The enemies surround you, cutting off your escape!")
                self.executing_actions = True
                self.select_enemy_actions()
                self.current_action_index = 0
                self.current_player_index = 0

                for player in self.player_party_alive:
                    self.player_actions[player] = {"action": "Escape"}


    def select_defense(self):
        """Store the selected defend for the current player."""
        current_player = self.player_party_alive[self.current_player_index]
        self.player_actions[current_player] = {"action": "Defend"}

        self.current_player_index += 1
        self.selected_option = 0

        # If all players have chosen actions, execute them in order
        if self.current_player_index >= len(self.player_party_alive):
            self.executing_actions = True
            self.select_enemy_actions()
            self.current_action_index = 0
            self.current_player_index = 0
    
    def store_selected_item(self):
        """Store the selected item for the current player."""
        current_player = self.player_party_alive[self.current_player_index]
        selected_item = list(self.battle_items)[self.selected_item_index]
        target = self.player_party[self.selected_item_target_index]
        self.player_actions[current_player] = {"action": "Items", "item": selected_item, "target": target}
        
        self.current_player_index += 1
        self.selecting_item = False
        self.selecting_item_target = False
        self.selected_item_index = 0
        self.selected_item_target_index = 0
        self.items_scroll_offset = 0
        self.selected_option = 0

        # If all players have chosen actions, execute them in order
        if self.current_player_index >= len(self.player_party_alive):
            self.executing_actions = True
            self.select_enemy_actions()
            self.current_action_index = 0
            self.current_player_index = 0
    

    def store_selected_attack_skill(self):
        """Store the selected attack for the current player."""
        current_player = self.player_party_alive[self.current_player_index]
        selected_attack = current_player.skills[self.selected_attack_index]

        if current_player.mp < self.attack_list[selected_attack]["mp"]:
            self.text_manager.add_message(f"Not enough MP to use {selected_attack}!")
            return
        
        # # Check if there are any enemies alive before proceeding
        # if not self.enemies_alive:
        #     self.check_battle_over()
        #     return
        
        # # Make sure selected_enemy_index is valid
        # if self.selected_enemy_index >= len(self.enemies_alive):
        #     self.selected_enemy_index = 0
        
        # Now it's safe to access the enemy
        self.player_actions[current_player] = {"action": "Attack", "skill": selected_attack, "target": self.enemies_alive[self.selected_enemy_index]}

        self.current_player_index += 1
        self.selecting_attack = False
        self.selected_option = 0

        # If all players have chosen actions, execute them in order
        if self.current_player_index >= len(self.player_party_alive):
            self.executing_actions = True
            self.select_enemy_actions()
            self.current_action_index = 0
            self.current_player_index = 0

    def select_enemy_actions(self):
        ####################################
        # Temporaliy enemy action selection
        for enemy in self.enemies_alive:
            target = random.choice(self.player_party_alive)
            
            while True:
                attack_skill = random.choice(enemy.skills)
                if enemy.mp >= self.attack_list[attack_skill]["mp"]:
                    break
            self.enemy_actions[enemy] = {"action": "Attack", "skill": attack_skill, "target": target}
    
        
    def execute_actions(self):
        # Execute actions if the previous animation is completed
        if not self.active_effects and self.current_action_index < len(self.action_order) and self.is_animation_finish(self.action_order[self.current_action_index-1]):
            # Remove dead characters from alive list and check if the battle finished
            for chara in self.action_order:
                if chara.hp <= 0:
                    if chara in self.player_party_alive:
                        self.player_party_alive.remove(chara)
                    elif chara in self.enemies_alive:
                        self.enemies_alive.remove(chara)
                    self.action_order.remove(chara)    
            self.check_battle_over()
            if self.battle_over:
                return
                
            # Set the action completed charas to idle or dead
            self.dead_or_idle()

            # Only after text message finish, go to next action
            if self.text_manager.messages == []:
                current_action_chara = self.action_order[self.current_action_index]

                # Check if the current action chara is player or enemy
                if current_action_chara in self.player_party:
                    if self.player_actions[current_action_chara]["action"] == "Attack":
                        self.player_attack(current_action_chara, self.player_actions[current_action_chara])
                    elif self.player_actions[current_action_chara]["action"] == "Items":
                        self.player_use_item(current_action_chara, self.player_actions[current_action_chara])
                    elif self.player_actions[current_action_chara]["action"] == "Defend":
                        self.player_defend(current_action_chara)

                elif current_action_chara in self.enemies:
                    if self.enemy_actions[current_action_chara]["action"] == "Attack":
                        self.enemy_attack(current_action_chara, self.enemy_actions[current_action_chara])

                if self.current_action_index< len(self.action_order):
                    self.current_action_index += 1

        # Check if all charas action has finished
        if self.current_action_index >= len(self.action_order) and self.is_animation_finish(self.action_order[self.current_action_index-1]):
            self.dead_or_idle()

            # Only after text message finish, go to next action
            if self.text_manager.messages == []:
                self.executing_actions = False
                self.turn_num += 1
                self.current_player_index = 0

                self.buff_timer()
                self.initialize_action_order()
    
    def player_defend(self, player):
        player.buffs.append({"type": "dfn_buff", "duration": 1, "effect": 0.5})
        player.dfn = player.dfn * 1.5
        self.text_manager.add_message(f"{player.name} takes a defensive stance!")


    def player_use_item(self, player, action):
        item = action["item"]
        type = self.items_list[item]["type"]
        effect = self.items_list[item]["effect"]
        target = action["target"]
        
        # Set Item animation
        player.sprite.set_animation("item")
        player.sprite.current_frame = 0
        self.action_changed_charas.append(player)
        
        # Use Item depends on its effect
        if target.hp > 0:
            if type == "hp":
                if effect == "full":
                    target.hp = target.max_hp
                    self.text_manager.add_message(f"{player.name} used a {item}! {target.name}'s HP was fully restored!")
                else:
                    target.hp = min(target.max_hp, target.hp+effect)
                    self.text_manager.add_message(f'{player.name} used a {item}! {target.name} +{effect} HP')
                self.heal_sound.play()

            elif type == "mp":
                if effect == "full":
                    target.mp = target.max_mp
                    self.text_manager.add_message(f"{player.name} used a {item}! {target.name}'s MP was fully restored!")
                else:
                    target.mp = min(target.max_mp, target.mp+effect)
                    self.text_manager.add_message(f'{player.name} used a {item}! {target.name} +{effect} MP')
                self.heal_sound.play()

            elif type == "hp+mp":
                if effect == "full":
                    target.hp = target.max_hp
                    target.mp = target.max_mp
                    self.text_manager.add_message(f"{player.name} used a {item}! {target.name}'s HP and MP were fully restored!")
                else:
                    target.hp = min(target.max_hp, target.hp+effect)
                    target.mp = min(target.max_mp, target.mp+effect)
                    self.text_manager.add_message(f'{player.name} used a {item}! {target.name} +{effect} HP and +{effect} MP')
                self.heal_sound.play()
            
            elif type == "atk_buff":
                duration = self.items_list[item]["duration"]
                target.buffs.append({"type": type, "duration": duration, "effect": effect})
                if 0 < effect < 1:
                    target.atk = int(target.atk * (1 + effect))
                    self.text_manager.add_message(f'{target.name} feels empowered! ATK boosted for {duration} turns!')
                else:
                    target.atk += effect
                    self.text_manager.add_message(f'{target.name} feels empowered! ATK boosted for {duration} turns!')
                self.atk_buff_sound.play()
            
            elif type == "dfn_buff":
                duration = self.items_list[item]["duration"]
                target.buffs.append({"type": type, "duration": duration, "effect": effect})
                if 0 < effect < 1:
                    target.dfn = int(target.dfn * (1 + effect))
                    self.text_manager.add_message(f'{target.name}\'s defense hardens! DEF increased by {effect*100}% for {duration} turns!')
                else:
                    target.dfn += effect
                    self.text_manager.add_message(f'{target.name} braces themselves! DEF boosted for {duration} turns!')
                self.dfn_buff_sound.play()
            
            elif type == "spd_buff":
                duration = self.items_list[item]["duration"]
                target.buffs.append({"type": type, "duration": duration, "effect": effect})
                if 0 < effect < 1:
                    target.spd = int(target.spd * (1 + effect))
                    self.text_manager.add_message(f'{target.name} feels lighter on their feet! SPD increased by {effect*100}% for {duration} turns!')
                else:
                    target.spd += effect
                    self.text_manager.add_message(f'{target.name} moves with blinding speed! SPD boosted for {duration} turns!')
                self.spd_buff_sound.play()

        else:
            if type == "re":
                if effect == "full":
                    target.hp = target.max_hp
                    self.text_manager.add_message(f'{target.name} was fully revived!')
                elif 0 < effect < 1:
                    target.hp = int(target.max_hp * effect)
                    self.text_manager.add_message(f'{target.name} was revived with {target.hp} HP!')
                else:
                    target.hp = min(target.max_hp, target.hp+effect)
                    self.text_manager.add_message(f'{target.name} was revived with {target.hp} HP!')
                self.heal_sound.play()
                
                # Set revived chara animation to idle
                target.sprite.set_animation("idle1")
                # Add revived chara into alive list
                index = self.player_party.index(target)
                self.player_party_alive.insert(index, target)
            else:
                self.text_manager.add_message(f'{target.name} is already dead, The item has no effect.')

        if self.player_party[0].inventory[item] > 1:
            self.player_party[0].inventory[item] -= 1
            self.battle_items[item] -= 1
        else:
            self.player_party[0].inventory.pop(item)
            self.battle_items.pop(item)


    def player_attack(self, player, action):
        skill = action["skill"]
        target = action["target"]
        attack_info = self.attack_list[skill]
        element = self.attack_list[skill]["element"]

        # Set attack, hit animmation
        player.sprite.set_animation(attack_info["state"])
        self.action_changed_charas.append(player)
        # Check the target is stll alive if not change the target
        if target not in self.enemies_alive:
            self.selected_enemy_index = 0
            target = self.enemies_alive[0]
        if "hit" in target.sprite.animations:
            target.sprite.set_animation("hit")
        self.action_changed_charas.append(target)

        if element:
            # Add attack effect
            self.add_attack_effect(target, element)

        # Move forward for attack depending on attack type
        if attack_info["state"] == "atk1" or attack_info["state"] == "atk2":
            self.current_position[player]["x"] = self.current_position[target]["x"] + 50
            self.current_position[player]["y"] = self.current_position[target]["y"]
            self.attack_sound.play()
        elif attack_info["state"] == "magic":
            self.magic_sound.play()
        elif attack_info["state"] == "gun":
            self.gun_sound.play()
        elif attack_info["state"] == "bow":
            self.bow_sound.play()

        # Knock back
        self.current_position[target]["x"] = self.current_position[target]["x"] - 20
        
        # Perform attack
        damage = player.attack(target, skill, take_damage_on=True)
        attack_message = f'{player.name} attacked {target.name} for {damage} damage!'
        self.text_manager.add_message(attack_message)

        
        if target.hp <= 0:
            if target in self.enemies_alive:
                self.text_manager.add_message(f'{player.name} defeated {target.name}!')
                # Remove the defeated enemy from enemies_alive and action_order lists
                # self.enemies_alive.remove(target)
                # if target in self.action_order:
                #     self.action_order.remove(target)
                    
                # # Reset selected_enemy_index if it's now out of range
                # if self.selected_enemy_index >= len(self.enemies_alive):
                #     self.selected_enemy_index = 0 if self.enemies_alive else 0
                    
                # Check if all enemies are defeated
                # self.check_battle_over()

        player.sprite.current_frame = 0


    def enemy_attack(self, enemy, action):
        skill = action["skill"]
        target = action["target"]
        attack_info = self.attack_list[skill]
        element = self.attack_list[skill]["element"]

        # Set attack
        # Some monsters does not have attack motion(only atk1)
        try:
            enemy.sprite.set_animation(attack_info["state"])
        except:
            enemy.sprite.set_animation(attack_info["atk1"])
        self.action_changed_charas.append(enemy)
        # Check the target is stll alive if not change the target
        if target not in self.player_party_alive:
            target = self.player_party_alive[0]
        target.sprite.set_animation("hit")
        self.action_changed_charas.append(target)

        if element:
            # Add attack effect
            self.add_attack_effect(target, element)

        # Move forward for attack depending on attack type
        if attack_info["state"] == "atk1" or attack_info["state"] == "atk2":
            self.current_position[enemy]["x"] = self.current_position[target]["x"] - 50
            self.current_position[enemy]["y"] = self.current_position[target]["y"]
            self.attack_sound.play()
        elif attack_info["state"] == "magic":
            self.magic_sound.play()
        elif attack_info["state"] == "gun":
            self.gun_sound.play()
        elif attack_info["state"] == "bow":
            self.bow_sound.play()
       

        # Knock back
        self.current_position[target]["x"] = self.current_position[target]["x"] + 20

        # Perform attack
        damage = enemy.attack(target, skill, take_damage_on=True)
        attack_message = f'{enemy.name} attacked {target.name} for {damage} damage!'
        self.text_manager.add_message(attack_message)

        self.attack_sound.play()

        if target.hp <= 0:
            if target in self.player_party_alive:
                self.text_manager.add_message(f'{target.name} falls to the ground, defeated by {enemy.name}!')

        enemy.sprite.current_frame = 0
    
    def buff_timer(self):
        for chara in self.player_party + self.enemies:
            for buff in chara.buffs:
                buff["duration"] -= 1
                if buff["duration"] == 0:
                    if 0 < buff["effect"] < 1:
                        if buff["type"] == "atk_buff":
                            chara.atk = chara.atk // (1 + buff["effect"])
                        elif buff["type"] == "dfn_buff":
                            chara.dfn = chara.dfn // (1 + buff["effect"])
                        elif buff["type"] == "spd_buff":
                            chara.spd = chara.spd // (1 + buff["effect"])
                    else:
                        if buff["type"] == "atk_buff":
                            chara.atk -=  buff["effect"]
                        elif buff["type"] == "dfn_buff":
                            chara.dfn -= buff["effect"]
                        elif buff["type"] == "spd_buff":
                            chara.spd -= buff["effect"]
                    chara.buffs.remove(buff)

    def dead_or_idle(self):
        """Check if the chara animation change to dead or idle"""
        for chara in self.action_changed_charas:
            if chara.hp <= 0:
                chara.sprite.set_animation("dead")
                if chara in self.player_party_alive:
                    self.player_party_alive.remove(chara)
                elif chara in self.enemies_alive:
                    self.enemies_alive.remove(chara)
            else:
                chara.sprite.set_animation("idle1")
            
            if chara in self.player_party:
                self.current_position[chara]["x"] = self.initial_player_party_info[chara]["x"]
                self.current_position[chara]["y"] = self.initial_player_party_info[chara]["y"]
                
            else:
                self.current_position[chara]["x"] = self.initial_enemies_info[chara]["x"]
                self.current_position[chara]["y"] = self.initial_enemies_info[chara]["y"]
                
        self.action_changed_charas = []

    def check_battle_over(self):
        if not self.player_party_alive:
            self.dead_or_idle()
            self.battle_over = True
            self.executing_actions = False
            self.end_battle("Defeat")
        elif not self.enemies_alive:
            self.dead_or_idle()
            self.battle_over = True
            self.executing_actions = False
            self.end_battle("Victory")

    def end_battle(self, result):
        """End the battle and display the result."""
        # Reset all the status change
        self.clean_up()
        if result == "Victory":
            self.result = "Victory"
            total_exp = self.calculate_total_exp()
            exp_per_member = self.distribute_exp(total_exp=total_exp)
            drop_items = self.get_drop_item()
            total_gold = self.calculate_total_gold()
            self.win_sound.play()
            self.text_manager.add_message(f"Victory! You gained {exp_per_member} EXP, found {total_gold} gold, and obtained {', '.join(drop_items) if drop_items else 'nothing'}!")
            self.player_party[0].gold += total_gold

            for item in drop_items:
                self.player_party[0].add_item(item)

        elif result == "Defeat":
            self.result = "Defeat"
            self.text_manager.add_message("Defeat! All party members defeated.")
        elif result == "Escaped":
            self.result = "Escaped"
            self.text_manager.add_message("Escaped from battle!")
            
        #self.display_result_window(result)

    def calculate_total_gold(self):
        """Calculate the total Gold from defeated monsters."""
        total_gold = 0
        for enemy in self.enemies:
            total_gold += enemy.gold
        return total_gold
    
    def calculate_total_exp(self):
        """Calculate the total EXP from defeated monsters."""
        total_exp = 0
        for enemy in self.enemies:
            total_exp += monster_exp_list()[enemy.name]
        return total_exp
    
    def distribute_exp(self, total_exp):
        """Distribute EXP equally among party members."""
        ### Save the previous level to check if the level went up
        prev_level = {}
        for member in self.player_party_alive:
            prev_level[member.name] = (member.level, len(member.skills))

        exp_per_member = total_exp // len(self.player_party_alive)
        for member in self.player_party_alive:
            member.gain_exp(exp_per_member)

            if member.level > prev_level[member.name][0]:
                self.text_manager.add_message(f"{member.name} has reached Level {member.level}!")
                if len(member.skills) > prev_level[member.name][1]:
                    self.text_manager.add_message(f"A new skill has been unlocked: {member.skills[-1]}")
        

        return exp_per_member
    
    def get_drop_item(self):
        """Get a random drop item from the enemy's drop table."""
        drop_table = monster_drop_list()
        drop_items = []

        # Roll a random number between 1 and 100
        roll = random.randint(1, 100)
        item_dropped = False
        # Check each item in the drop table
        for enemy in self.enemies:
            cumulative_chance = 0
            for item, chance in drop_table[enemy.name].items():
                cumulative_chance += chance
                if not item_dropped:
                    if roll <= cumulative_chance:
                        drop_items.append(item)
                        item_dropped = True
            item_dropped = False
        return drop_items

    def clean_up(self):
        for chara in self.player_party:
            chara.atk = self.initial_player_party_info[chara]["atk"]
            chara.dfn = self.initial_player_party_info[chara]["dfn"]
            chara.spd = self.initial_player_party_info[chara]["spd"]
            chara.buffs = []
        
        for chara in self.enemies:
            chara.atk = self.initial_enemies_info[chara]["atk"]
            chara.dfn = self.initial_enemies_info[chara]["dfn"]
            chara.spd = self.initial_enemies_info[chara]["spd"]
            chara.buffs = []

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                self.handle_input(event)

            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(30)
        
        # Rescale to original size
        for player in self.player_party:
            player.sprite.rescale(self.initial_player_party_info[player]["scale_factor"])
            player.sprite.set_animation(self.initial_player_party_info[player]["state"])
        for enemy in self.enemies:
            enemy.sprite.rescale(self.initial_enemies_info[enemy]["scale_factor"])
            enemy.sprite.set_animation(self.initial_enemies_info[enemy]["state"])
            enemy.sprite.is_flipped = False
        return self.result



# Example usage
# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# pygame.display.set_caption("Battle System")

# inventory = {}
# for key in items_list().keys():
#     inventory[key] = 2

# player1 = Character(
#     name="Hero",
#     x=700,
#     y=700,
#     level=10,
#     hp=10000,
#     mp=20,
#     atk=4000,
#     dfn=20,
#     spd=1000,
#     skills=["Strike", "Power Slash", "Fireball", "Piercing Shot"],
#     inventory=inventory.copy(),
#     folder_paths=[fR".\timefantasy_characters\timefantasy_characters\frames\chara\chara2_5",
#                   fR".\tf_svbattle\singleframes\set2\5"]
# )

# player2 = Character(
#     name="Mage",
#     x=750,
#     y=700,
#     level=10,
#     hp=70,   # Low HP
#     mp=100,  # High MP
#     atk=20,  # Weak physical attack
#     dfn=15,  # Weak defense
#     spd=25,  # Moderate speed
#     skills=["Strike", "Power Slash", "Fireball"],
#     inventory=inventory.copy(),
#     folder_paths=[fR".\timefantasy_characters\timefantasy_characters\frames\chara\chara2_2",
#                   fR".\tf_svbattle\singleframes\set2\2"]
# )

# player3 = Character(
#     name="Rogue",
#     x=800,
#     y=700,
#     level=10,
#     hp=90,   # Decent HP
#     mp=30,   # Low MP
#     atk=50,  # High attack
#     dfn=10,  # Weak defense
#     spd=45,  # High speed
#     skills=["Strike", "Power Slash", "Fireball", "Quick Shot"],
#     inventory=inventory.copy(),
#     folder_paths=[fR".\timefantasy_characters\timefantasy_characters\frames\military\military3_1",
#                   fR".\tf_svbattle\singleframes\military3/1"]
# )

# player4 = Character(
#     name="Cleric",
#     x=850,
#     y=700,
#     level=10,
#     hp=85,   # Moderate HP
#     mp=90,   # High MP (for healing)
#     atk=25,  # Weak attack
#     dfn=30,  # Good defense
#     spd=20,  # Low speed
#     inventory=inventory.copy(),
#     folder_paths=[fR".\timefantasy_characters\timefantasy_characters\frames\chara\chara2_6",
#                   fR".\tf_svbattle\singleframes\set2\6"]
# )

# enemy1 = Enemy(
#     name="Orc",
#     x=1515,
#     y=1585,
#     level=8,
#     hp=120,  # High HP
#     mp=30,   # Some MP
#     atk=35,  # Strong attack
#     dfn=30,  # High defense
#     spd=20,  # Slow
#     inventory={},
#     exp_reward=10,
#     loot=None,
#     folder_paths=[
#         R".\timefantasy_characters\timefantasy_characters\frames\chara\chara5_8",
#         R".\tf_svbattle\singleframes\set5\8"
#     ]
# )

# enemy2 = Enemy(
#     name="Goblin",
#     x=1550,
#     y=1585,
#     level=7,
#     hp=60,   # Low HP
#     mp=20,   # Some MP
#     atk=2500,  # Weak attack
#     dfn=10,  # Weak defense
#     spd=50,  # Very fast
#     inventory={},
#     exp_reward=7,
#     loot=None,
#     folder_paths=[
#     R".\timefantasy_characters\timefantasy_characters\frames\chara\chara5_8",
#     R".\tf_svbattle\singleframes\set5\8"
# ]
# )

# enemy3 = Enemy(
#     name="Dark Mage",
#     x=1585,
#     y=1585,
#     level=9,
#     hp=80,   # Medium HP
#     mp=120,  # Very High MP
#     atk=20,  # Weak physical attack
#     dfn=15,  # Weak defense
#     spd=25,  # Medium speed
#     inventory={},
#     exp_reward=12,
#     loot=None,
#     folder_paths=[
#     R".\timefantasy_characters\timefantasy_characters\frames\chara\chara5_8",
#     R".\tf_svbattle\singleframes\set5\8"
# ]
# )

# enemy4 = Enemy(
#     name="Giant Spider",
#     x=1620,
#     y=1585,
#     level=8,
#     hp=100,  # Medium HP
#     mp=40,   # Some MP for abilities
#     atk=30,  # Decent attack
#     dfn=20,  # Medium defense
#     spd=35,  # Fast
#     inventory={},
#     exp_reward=8,
#     loot=None,
#     folder_paths=[
#     R".\timefantasy_characters\timefantasy_characters\frames\chara\chara5_8",
#     R".\tf_svbattle\singleframes\set5\8"
# ]
# )

# enemy5 = Enemy(
#     name="Bat",
#     x=1620,
#     y=1585,
#     level=8,
#     hp=100,  # Medium HP
#     mp=40,   # Some MP for abilities
#     atk=30,  # Decent attack
#     dfn=20,  # Medium defense
#     spd=35,  # Fast
#     inventory={},
#     exp_reward=8,
#     loot=None,
#     folder_paths=[
#     R".\Monsters\bat",
# ]
# )

# enemy6 = Enemy(
#     name="Slime",
#     x=1620,
#     y=1585,
#     level=8,
#     hp=100,  # Medium HP
#     mp=40,   # Some MP for abilities
#     atk=30,  # Decent attack
#     dfn=20,  # Medium defense
#     spd=35,  # Fast
#     inventory={},
#     exp_reward=8,
#     loot=None,
#     folder_paths=[
#     R".\Monsters\slime",
# ]
# )

# player_party = [player1, player2, player3, player4]
# enemies = [enemy1, enemy2, enemy3, enemy4]
# enemies = [enemy5, enemy6]


# battle = Battle(screen, player_party, enemies, ".\Backgrounds\game_background_2.png")
# battle.run()


# pygame.quit()