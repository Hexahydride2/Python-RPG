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
        self.dfn = dfn
        self.spd = spd
        self.inventory = inventory
        self.gold = gold
        self.can_move = True
        self.moving = False  # Track movement state
        self.current_direction = "down"  # Default direction
        self.walkspeed = 5

        # Sprite system (supports multiple animations)
        self.sprite = Sprite(folder_paths, scale_factor, animation_speed)

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
    
    def move(self, keys):
        # Display Walk motion only moving
        self.sprite.is_flipped = False
        if self.moving == True:
            self.sprite.set_animation(f"{self.current_direction}_walk")
        else:
            self.sprite.set_animation(f"{self.current_direction}_stand")
        if not self.can_move:
            return
        if keys[pygame.K_LEFT]:  
            self.x -= self.walkspeed
            self.moving = True
            self.current_direction = "left"

        elif keys[pygame.K_RIGHT]:  
            self.x += self.walkspeed
            self.moving = True
            self.current_direction = "right"

        elif keys[pygame.K_UP]:  
            self.y -= self.walkspeed
            self.moving = True
            self.current_direction = "up"

        elif keys[pygame.K_DOWN]:  
            self.y += self.walkspeed
            self.moving = True
            self.current_direction = "down"

        else:
            self.moving = False  # Stop animation if no key is pressed

    


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
        screen.blit(self.interaction_symbol, (self.x + self.sprite.sprite_shape[self.sprite.current_animation]["width"] // 2 + 10, self.y - 30))

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
