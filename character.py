import random
from sprite import Sprite

class Character:
    def __init__(self, name, level, hp, mp, atk, defense, spd, inventory, sprite_paths, sprite_width=100, sprite_height=100, scale_factor=3, num_frames_dict=None, animation_speed=5):
        # Character Stats
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = hp
        self.mp = mp
        self.max_mp = mp
        self.atk = atk
        self.defense = defense
        self.spd = spd
        self.inventory = inventory

        # Sprite system (supports multiple animations)
        self.sprite = Sprite(sprite_paths, sprite_width, sprite_height, scale_factor, num_frames_dict, animation_speed)

    def level_up(self):
        """Increase stats when leveling up."""
        self.level += 1
        self.hp += 10
        self.mp += 5
        self.atk += 3
        self.defense += 2
        self.spd += 2

    def take_damage(self, damage):
        """Reduce HP based on damage calculation."""
        damage_taken = max(1, damage - self.defense)
        self.hp -= damage_taken
        return damage_taken

    def attack(self, target, take_damage_on=True):
        """Attack another character, dealing damage."""
        damage = max(1, self.atk - target.defense)
        if take_damage_on:
            target.take_damage(damage)
        return damage

    def add_item(self, item):
        """Add an item to inventory."""
        self.inventory.append(item)

    def use_item(self, item_name):
        """Use an item if available in inventory."""
        for item in self.inventory:
            if item["name"] == item_name:
                effect = item["effect"]
                if effect == "heal":
                    self.hp += item["value"]
                elif effect == "mp_restore":
                    self.mp += item["value"]
                self.inventory.remove(item)
                return f"Used {item_name}!"
        return f"{item_name} not available!"
    
    def update(self):
        """Update the character sprite animation."""
        self.sprite.update_frame()
