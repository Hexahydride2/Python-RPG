import random
from sprite import Sprite
from items import items_list

class Character:
    def __init__(self, name, level, hp, mp, atk, dfn, spd, inventory, folder_paths, scale_factor=3, num_frames_dict=None, animation_speed=5):
        # Character Stats
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = hp
        self.mp = mp
        self.max_mp = mp
        self.atk = atk
        self.dfn = dfn
        self.spd = spd
        self.inventory = inventory

        # Sprite system (supports multiple animations)
        self.sprite = Sprite(folder_paths, scale_factor, animation_speed)

    def level_up(self):
        """Increase stats when leveling up."""
        self.level += 1
        self.hp += 10
        self.mp += 5
        self.atk += 3
        self.dfn += 2
        self.spd += 2

    def take_damage(self, damage):
        """Reduce HP based on damage calculation."""
        damage_taken = max(1, damage - self.dfn)
        self.hp -= damage_taken
        return damage_taken

    def attack(self, target, take_damage_on=True):
        """Attack another character, dealing damage."""
        damage = max(1, self.atk - target.dfn)
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
    
    def update(self):
        """Update the character sprite animation."""
        self.sprite.update_frame()

    
