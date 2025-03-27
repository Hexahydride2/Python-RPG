import random
import pygame
import json
from sprite import Sprite
from items import items_list, attack_list
from shop import Shop

class Character:
    def __init__(self, name, x, y, folder_paths, level=1, hp=1, mp=1, atk=1, dfn=1, spd=1, inventory={}, gold=100, skills=["Strike"], scale_factor=3, animation_speed=5):
        # Character Stats
        self.name = name
        self.x, self.y = x, y
        self.folder_paths = folder_paths
        self.level = level
        self.hp = hp
        self.max_hp = hp
        self.mp = mp
        self.max_mp = mp
        self.atk = atk
        self.dfn = dfn
        self.spd = spd
        self.inventory = inventory
        self.gold = gold
        self.skills = skills
        self.scale_factor = scale_factor
        self.can_move = True
        self.moving = False  # Track movement state
        self.current_direction = "down"  # Default direction
        self.walkspeed = 10
        self.buffs = []

        # Used to diplay the camera based location
        self.draw_x = 0
        self.draw_y = 0

        # Sprite system (supports multiple animations)
        self.sprite = Sprite(self.folder_paths, self.scale_factor, animation_speed)

        # Define hitbox based on sprite dimenstions
        self.hitbox_width = (self.sprite.sprite_shape[self.sprite.current_animation]["width"]) * scale_factor
        self.hitbox_height = (self.sprite.sprite_shape[self.sprite.current_animation]["height"]//2) * scale_factor
        self.hitbox = pygame.Rect(self.x, self.y + self.hitbox_height, self.hitbox_width, self.hitbox_height)

        self.initial_x = x
        self.initial_y = y

        # EXP system
        self.exp = 0  # Current EXP
        self.exp_to_next_level = self.calculate_exp_to_next_level()  # EXP required for next level
    
    def calculate_exp_to_next_level(self):
        """Calculate the EXP required to reach the next level using a DQ-style formula."""
        base_exp = 10  # Base value for EXP scaling
        return base_exp * (self.level ** 2)
    
    def gain_exp(self, amount):
        """Gain EXP and check for level up."""
        self.exp += amount
        while self.exp >= self.exp_to_next_level:
            self.level_up()

    def level_up(self):
        """Increase level and stats when enough EXP is gained."""
        self.level += 1
        self.exp -= self.exp_to_next_level  # Carry over remaining EXP
        self.exp_to_next_level = self.calculate_exp_to_next_level()  # Update EXP requirement for next level

        level_up_sound = pygame.mixer.Sound(R"Sound_Effects\level-win.mp3")
        level_up_sound.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
        level_up_sound.play()


        # Randomized stat increases
        hp_increase = random.randint(8, 12)  # HP increases by 8–12
        mp_increase = random.randint(3, 6)   # MP increases by 3–6
        atk_increase = random.randint(2, 4)  # Attack increases by 2–4
        dfn_increase = random.randint(1, 3)  # Defense increases by 1–3
        spd_increase = random.randint(1, 2)  # Speed increases by 1–2

        # Apply stat increases
        self.max_hp += hp_increase
        self.hp = self.max_hp  # Fully heal on level up
        self.max_mp += mp_increase
        self.mp = self.max_mp  # Fully restore MP on level up
        self.atk += atk_increase
        self.dfn += dfn_increase
        self.spd += spd_increase

        # Gain skill
        while True:
            skill_gained = random.choice(list(attack_list().keys()))
            if attack_list()[skill_gained]["state"] not in self.sprite.animations:
                pass
            elif skill_gained in self.skills:
                pass
            else:
                self.skills.append(skill_gained)
                break

    def calculate_damage(self, attacker_atk, defender_def, base_damage=1, is_critical=False):
        """Calculate damage using a DQ-style formula."""
        if is_critical:
            # Critical hits ignore DEF and deal double damage
            damage = attacker_atk * 2 * random.uniform(0.9, 1.1)
        else:
            # Normal damage calculation
            damage = (attacker_atk - (defender_def / 2)) * base_damage * random.uniform(0.9, 1.1)

        # Ensure minimum damage of 1
        return max(1, int(damage))

    def attack(self, target, attack_name, take_damage_on=False):
        """Attack another character, dealing damage."""
        damage = self.calculate_damage(self.atk, target.dfn, attack_list()[attack_name]["effect"])
        if take_damage_on:
            target.hp -= damage
            if target.hp <= 0:
                target.hp = 0
            self.mp -= attack_list()[attack_name]["mp"]
        return damage

    def add_item(self, item):
        """Add an item to inventory."""
        if item in self.inventory:
            self.inventory[item] += 1
        else:
            self.inventory[item] = 1

    def use_item(self, item):
        """Use an item if available in inventory."""
        All_Item_List = items_list()
        if item in self.inventory and self.inventory[item] > 0:
            if All_Item_List[item]["type"] == "hp":
                self.hp = min(self.hp + All_Item_List[item]["effect"], self.max_hp)
                
            elif All_Item_List[item]["type"] == "mp":
                self.mp = min(self.mp + All_Item_List[item]["effect"], self.max_mp)

            # Exclude the item if the count get 0
            self.inventory[item] -= 1
        else:
            return f"{item} not available!"
        All_Item_List = items_list()
        if item in self.inventory and self.inventory[item] > 0:
            if All_Item_List[item]["type"] == "hp":
                self.hp = min(self.hp + All_Item_List[item]["effect"], self.max_hp)
                
            elif All_Item_List[item]["type"] == "mp":
                self.mp = min(self.mp + All_Item_List[item]["effect"], self.max_mp)

            # Exclude the item if the count get 0
            self.inventory[item] -= 1
        else:
            return f"{item} not available!"

    def update(self):
        """Update the character sprite animation."""
        self.sprite.update_frame()
    
    def walk(self, keys, map_obj):
        # Display Walk motion only moving
        self.sprite.is_flipped = False
        if self.moving == True:
            self.sprite.set_animation(f"{self.current_direction}_walk")
        else:
            self.sprite.set_animation(f"{self.current_direction}_stand")
        if not self.can_move:
            return
        
        new_x, new_y = self.x, self.y
        if keys[pygame.K_LEFT]:  
            new_x -= self.walkspeed
            self.moving = True
            self.current_direction = "left"

        elif keys[pygame.K_RIGHT]:  
            new_x += self.walkspeed
            self.moving = True
            self.current_direction = "right"

        elif keys[pygame.K_UP]:  
            new_y -= self.walkspeed
            self.moving = True
            self.current_direction = "up"

        elif keys[pygame.K_DOWN]:  
            new_y += self.walkspeed
            self.moving = True
            self.current_direction = "down"

        else:
            self.moving = False  # Stop animation if no key is pressed

        # Clamp player position to map boundaries
        #map_obj.clamp_player_position()

        # Update the camera to follow the player
        map_obj.update_camera()

        # Check for random encounter 
        if self.moving == True:
            map_obj.handle_random_encounter(self)

        # Simulate new position
        new_hitbox  = pygame.Rect(new_x, new_y + self.hitbox_height, self.hitbox_width, self.hitbox_height)

        # Check if new position collides with Buildings
        try:
            if map_obj.positions[new_x][int(new_y + self.hitbox_height)] == 0:
            # Check if new position collides with NPCs
                if not any(new_hitbox.colliderect(char.hitbox) for char in map_obj.npcs+map_obj.enemies):
                    self.x, self.y = new_x, new_y  # Update position
                    self.hitbox.topleft = (self.x, self.y + self.hitbox_height)
        except:
            pass
        
    def move(self, direction):
        self.sprite.is_flipped = False
        self.moving = True
        if direction == "left":
            self.x -= self.walkspeed
            self.current_direction = "left"
            self.sprite.set_animation("left_walk")
        elif direction == "right":
            self.x += self.walkspeed
            self.current_direction = "right"
            self.sprite.set_animation("right_walk")
        elif direction == "up":
            self.y -= self.walkspeed
            self.current_direction = "up"
            self.sprite.set_animation("up_walk")
        elif direction == "down":
            self.y += self.walkspeed
            self.current_direction = "down"
            self.sprite.set_animation("down_walk")

class NPC(Character):
    def __init__(self, name, dialogues, x, y, folder_paths, shop_items=None, guild=False, inn=False, scale_factor=3):
        """NPC class that extends Character and supports conversations."""
        super().__init__(name, x, y, level=1, hp=50, mp=0, atk=1, dfn=1, spd=1, inventory={}, folder_paths=folder_paths, scale_factor=scale_factor)
        
        self.dialogues = dialogues  # List of dialogue strings
        self.current_dialogue = 0
        self.x = x
        self.y = y
        self.talking = False  # Is the NPC talking?
        self.interaction_symbol = pygame.image.load(R".\Icons\dialog.png")  # Load interaction icon
        self.shop_items = shop_items # Shop inventory (None if NPC isn't a shopkeeper)
        self.shop = None

        self.guild = guild
        self.inn = inn

    def draw(self, screen):
        """Draw NPC sprite and interaction symbol if the player is near."""
        self.sprite.draw(screen, self.x, self.y)

    def draw_interaction_symbol(self, screen):
        """Draw a floating symbol above the NPC when the player is near."""
        screen.blit(self.interaction_symbol, (self.draw_x + self.sprite.sprite_shape[self.sprite.current_animation]["width"] // 2 + 10, self.draw_y - 30))

    def talk(self, text_manager, player, screen):
        """Triggers NPC dialogue through `TextManager`."""
        if self.current_dialogue < len(self.dialogues):
            #for dialogue in self.dialogues:
            text_manager.add_message(self.dialogues[self.current_dialogue], self.name)
            self.current_dialogue += 1  # Move to the next dialogue line
            
            # if npc has shop_items, make a shop instance
            if self.shop_items:
                self.shop = Shop(screen, player, self.shop_items)
    
        else:
            self.current_dialogue = 0  # Reset when finished
            self.talking = False  # Stop conversation


    


class Enemy(Character):
    def __init__(self, name, x, y, folder_paths, level, hp, mp, atk, dfn, spd, inventory={}, gold=100, skills=["Strike"],   scale_factor=3):
        """Enemy inherits from Character and adds EXP & loot system."""
        super().__init__(name, x, y, folder_paths, level, hp, mp, atk, dfn, spd, inventory, gold=gold, skills=skills, scale_factor=scale_factor)
        self.is_alive = True  # Enemy state 


class Party:
    def __init__(self, leader):
        """
        Initialize the party with a leader (main character).
        :param leader: The main character (instance of Character class).
        """
        self.leader = leader
        self.members = [leader]  # Leader is the first member
        self.max_size = 4  # Maximum party size
        self.storage = []
        self.current_quests = [] # maximum 3
        self.guild_rank = "C"
        self.guild_point = 0
        self.gold = 500

    
    def add_member(self, character):
        """
        Add a new member to the party.
        :param character: The character to add (instance of Character class).
        """
        if len(self.members) < self.max_size:
            self.members.append(character)
        else:
            self.storage.append(character)
    