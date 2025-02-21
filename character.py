import random
import pygame
from sprite import Sprite
from items import items_list, attack_list
from shop import Shop

class Character:
    def __init__(self, name, x, y, level, hp, mp, atk, dfn, spd, inventory, folder_paths, gold=100, scale_factor=3, animation_speed=5):
        # Character Stats
        self.name = name
        self.x, self.y = x, y
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
        self.can_move = True
        self.moving = False  # Track movement state
        self.current_direction = "down"  # Default direction
        self.walkspeed = 5

        # Used to diplay the camera based location
        self.draw_x = 0
        self.draw_y = 0

        # Sprite system (supports multiple animations)
        self.sprite = Sprite(folder_paths, scale_factor, animation_speed)

        # Define hitbox based on sprite dimenstions
        self.hitbox_width = (self.sprite.sprite_shape[self.sprite.current_animation]["width"]) * scale_factor
        self.hitbox_height = (self.sprite.sprite_shape[self.sprite.current_animation]["height"]//2) * scale_factor
        self.hitbox = pygame.Rect(self.x, self.y + self.hitbox_height, self.hitbox_width, self.hitbox_height)

        self.initial_x = x
        self.initial_y = y


    def level_up(self):
        """Increase stats when leveling up."""
        self.level += 1
        self.hp += 10
        self.mp += 5
        self.atk += 3
        self.dfn += 2
        self.dfn += 2
        self.spd += 2

    def take_damage(self, damage):
        """Reduce HP based on damage calculation."""
        damage_taken = max(1, damage - self.dfn)
        damage_taken = max(1, damage - self.dfn)
        self.hp -= damage_taken
        return damage_taken

    def attack(self, target, attack_name, take_damage_on=False):
        """Attack another character, dealing damage."""
        damage = max(1, int((self.atk - target.dfn)*attack_list()[attack_name]["effect"]))
        if take_damage_on:
            target.take_damage(damage)
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
        map_obj.clamp_player_position()

        # Update the camera to follow the player
        map_obj.update_camera()

        # Check for random encounter 
        if self.moving == True:
            map_obj.handle_random_encounter(self)

        # Simulate new position
        new_hitbox  = pygame.Rect(new_x, new_y + self.hitbox_height, self.hitbox_width, self.hitbox_height)
       
       # Check if new position collides with Buildings
        if map_obj.positions[new_x][new_y + self.hitbox_height] == 0:
            # Check if new position collides with NPCs
            if not any(new_hitbox.colliderect(char.hitbox) for char in map_obj.npcs+map_obj.enemies):
                self.x, self.y = new_x, new_y  # Update position
                self.hitbox.topleft = (self.x, self.y + self.hitbox_height)
        
    def move(self, direction):
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
    def __init__(self, name, dialogues, x, y, folder_paths, shop_items=None, scale_factor=3):
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
            
            # if npc hace shop_items, make a shop instance
            if self.shop_items:
                self.shop = Shop(screen, player, self.shop_items)
    
        else:
            self.current_dialogue = 0  # Reset when finished
            self.talking = False  # Stop conversation


class Enemy(Character):
    def __init__(self, name, x, y, level, hp, mp, atk, dfn, spd, inventory, exp_reward, loot, folder_paths, scale_factor=3):
        """Enemy inherits from Character and adds EXP & loot system."""
        super().__init__(name, x, y, level, hp, mp, atk, dfn, spd, inventory, folder_paths, scale_factor=scale_factor)
        
        self.exp_reward = exp_reward  # EXP gained by player on defeat
        self.loot = loot  # Dictionary of possible loot {"Potion": 50% chance, "Gold": 100% chance}
        self.is_alive = True  # Enemy state