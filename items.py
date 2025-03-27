def items_list():
    All_Item_List = {
    "Potion": {
        "description": "Restores 15 HP. A basic healing drink.",
        "type": "hp",
        "effect": 15,
        "price": 15
    },
    "Super Potion": {
        "description": "Restores 60 HP. A stronger variant of the potion.",
        "type": "hp",
        "effect": 60,
        "price": 55
    },
    "Mega Potion": {
        "description": "Restores 150 HP. A rare and powerful potion.",
        "type": "hp",
        "effect": 150,
        "price": 200
    },
    "Mana Crystal": {
        "description": "Restores 15 MP. A small glowing crystal filled with energy.",
        "type": "mp",
        "effect": 15,
        "price": 18
    },
    "Ether": {
        "description": "Restores 60 MP. A refined magical liquid that energizes the mind.",
        "type": "mp",
        "effect": 60,
        "price": 50
    },
    "Elixir": {
        "description": "Fully restores both HP and MP.",
        "type": "hp+mp",
        "effect": "full",
        "price": 500
    },
    "Revive": {
        "description": "Revives a fallen ally with 50% of their HP.",
        "type": "re",
        "effect": 0.5,
        "price": 250
    },
    "Phoenix down": {
        "description": "Revives a fallen ally with full HP.",
        "type": "re",
        "effect": "full",
        "price": 500
    },
    "Strength Potion": {
        "description": "Increases attack by 25 for 4 turns.",
        "type": "atk_buff",
        "effect": 25,
        "duration": 4,
        "price": 65
    },
    "Berserker Brew": {
        "description": "Increases attack by 10% for 5 turns.",
        "type": "atk_buff",
        "effect": 0.1,
        "duration": 5,
        "price": 120
    },
    "Warrior's Elixir": {
        "description": "Boosts attack by 20 for 4 turns.",
        "type": "atk_buff",
        "effect": 20,
        "duration": 4,
        "price": 160
    },
    "Defense Shield": {
        "description": "Temporarily boosts defense by 20 for 4 turns.",
        "type": "dfn_buff",
        "effect": 20,
        "duration": 4,
        "price": 75
    },
    "Dragon Scale": {
        "description": "Temporarily increases defense by 40 for 3 turns.",
        "type": "dfn_buff",
        "effect": 40,
        "duration": 3,
        "price": 150
    },
    "Wind Amulet": {
        "description": "Increases movement speed by 15% for 3 turns.",
        "type": "spd_buff",
        "effect": 0.15,
        "duration": 3,
        "price": 140
    },
    "Shadow Cloak": {
        "description": "Increases speed by 30% for 3 turns.",
        "type": "spd_buff",
        "effect": 0.30,
        "duration": 3,
        "price": 180
    },
    "Bat Wing": {
        "description": "A wing from a bat. Can be used in crafting.",
        "type": "dropped",
        "effect": None,
        "price": 10
    },
    "Herb": {
        "description": "A common herb used in potions and remedies.",
        "type": "dropped",
        "effect": None,
        "price": 5
    },
    "Honey": {
        "description": "Sweet honey collected from bees. Used in cooking and potions.",
        "type": "dropped",
        "effect": None,
        "price": 8
    },
    "Stinger": {
        "description": "A sharp stinger from a bee. Can be used in crafting.",
        "type": "dropped",
        "effect": None,
        "price": 12
    },
    "Cheese": {
        "description": "A piece of cheese. Can be eaten for a small health boost.",
        "type": "dropped",
        "effect": 5,
        "price": 7
    },
    "Tail": {
        "description": "A tail from a mouse. Used in crafting.",
        "type": "dropped",
        "effect": None,
        "price": 6
    },
    "Spider Silk": {
        "description": "Strong silk from a spider. Used in crafting armor and tools.",
        "type": "dropped",
        "effect": None,
        "price": 20
    },
    "Venom Sack": {
        "description": "A sack filled with venom. Used in poison-based crafting.",
        "type": "dropped",
        "effect": None,
        "price": 25
    },
    "Slime Gel": {
        "description": "A sticky gel from a slime. Used in alchemy.",
        "type": "dropped",
        "effect": None,
        "price": 15
    },
    "Snake Skin": {
        "description": "The skin of a snake. Used in crafting light armor.",
        "type": "dropped",
        "effect": None,
        "price": 30
    },
    "Rare Flower": {
        "description": "A rare flower with magical properties. Used in high-level potions.",
        "type": "dropped",
        "effect": None,
        "price": 50
    },
    "Phoenix Feather": {
        "description": "A feather from a phoenix. Used to revive a fallen ally.",
        "type": "re",
        "effect": "full",
        "price": 100
    },
    "Flame Essence": {
        "description": "Essence of fire. Used in fire-based crafting.",
        "type": "dropped",
        "effect": None,
        "price": 75
    },
    "Sacred Ash": {
        "description": "Rare ash from a phoenix. Used in high-level crafting.",
        "type": "dropped",
        "effect": None,
        "price": 150
    },
    "Minotaur Horn": {
        "description": "A horn from a minotaur. Used in crafting weapons and armor.",
        "type": "dropped",
        "effect": None,
        "price": 80
    },
    "Beast Hide": {
        "description": "Tough hide from a beast. Used in crafting armor.",
        "type": "dropped",
        "effect": None,
        "price": 60
    },
    "Warrior's Medallion": {
        "description": "A rare medallion worn by warriors. Grants strength when equipped.",
        "type": "dropped",
        "effect": "strength",
        "price": 200
    },
    "Ancient Bark": {
        "description": "Bark from an ancient tree. Used in alchemy.",
        "type": "dropped",
        "effect": None,
        "price": 40
    },
    "Dryad Leaf": {
        "description": "A leaf from a dryad. Used in healing potions.",
        "type": "dropped",
        "effect": None,
        "price": 25
    },
    "Spirit Core": {
        "description": "The core of a spirit. Used in enchantments.",
        "type": "dropped",
        "effect": None,
        "price": 90
    }
}

    return All_Item_List

def shop_keeper_items_list():
    All_items = {
        "Potion": {
        "description": "Restores 15 HP. A basic healing drink.",
        "type": "hp",
        "effect": 15,
        "price": 15
    },
    "Super Potion": {
        "description": "Restores 60 HP. A stronger variant of the potion.",
        "type": "hp",
        "effect": 60,
        "price": 55
    },
    "Mega Potion": {
        "description": "Restores 150 HP. A rare and powerful potion.",
        "type": "hp",
        "effect": 150,
        "price": 200
    },
    "Mana Crystal": {
        "description": "Restores 15 MP. A small glowing crystal filled with energy.",
        "type": "mp",
        "effect": 15,
        "price": 18
    },
    "Ether": {
        "description": "Restores 60 MP. A refined magical liquid that energizes the mind.",
        "type": "mp",
        "effect": 60,
        "price": 50
    },
    "Phoenix down": {
        "description": "Revives a fallen ally with full HP.",
        "type": "re",
        "effect": "full",
        "price": 500
    },
    "Berserker Brew": {
        "description": "Increases attack by 10% for 5 turns.",
        "type": "atk_buff",
        "effect": 0.1,
        "duration": 5,
        "price": 120
    },
     "Defense Shield": {
        "description": "Temporarily boosts defense by 20 for 4 turns.",
        "type": "dfn_buff",
        "effect": 20,
        "duration": 4,
        "price": 75
    },
       "Revive": {
        "description": "Revives a fallen ally with 50% of their HP.",
        "type": "re",
        "effect": 0.5,
        "price": 250
    },
    }
    return All_items

def attack_list():
    Attack_List = {
    # Basic Melee Attacks (atk1)
    "Strike": {
        "description": "A swift melee attack.",
        "mp": 0,
        "effect": 1,
        "state": "atk1",
        "element": None  # No elemental affinity
    },
    "Earth Smash": {
        "description": "A powerful strike infused with earth energy.",
        "mp": 5,
        "effect": 1.2,
        "state": "atk1",
        "element": "earth"  # Earth element
    },
    "Flame Slash": {
        "description": "A fiery slash that burns the enemy.",
        "mp": 10,
        "effect": 1.3,
        "state": "atk1",
        "element": "fire"  # Fire element
    },

    # Advanced Melee Attacks (atk2)
    "Power Cleave": {
        "description": "A heavy attack that deals increased damage.",
        "mp": 20,
        "effect": 1.5,
        "state": "atk2",
        "element": None  # No elemental affinity
    },
    "Crystal Strike": {
        "description": "A dazzling attack infused with glass energy.",
        "mp": 25,
        "effect": 1.4,
        "state": "atk2",
        "element": "glass"  # Glass element
    },
    "Frost Blade": {
        "description": "A freezing slash that chills the enemy.",
        "mp": 15,
        "effect": 1.3,
        "state": "atk2",
        "element": "ice"  # Ice element
    },

    # Bow Attacks (bow)
    "Piercing Shot": {
        "description": "Fires an arrow at an enemy.",
        "mp": 10,
        "effect": 1.2,
        "state": "bow",
        "element": None  # No elemental affinity
    },
    "Explosive Arrow": {
        "description": "Fires an arrow that explodes on impact.",
        "mp": 15,
        "effect": 1.5,
        "state": "bow",
        "element": "explosion"  # Explosion element
    },
    "Sonic Shot": {
        "description": "Fires an arrow that creates a deafening sound wave.",
        "mp": 20,
        "effect": 1.4,
        "state": "bow",
        "element": "sound"  # Sound element
    },

    # Gun Attacks (gun)
    "Quick Shot": {
        "description": "A rapid shot from a gun.",
        "mp": 10,
        "effect": 1.2,
        "state": "gun",
        "element": None  # No elemental affinity
    },
    "Inferno Blast": {
        "description": "Fires a blazing shot that engulfs the enemy in flames.",
        "mp": 15,
        "effect": 1.5,
        "state": "gun",
        "element": "fire"  # Fire element
    },
    "Dark Bullet": {
        "description": "Fires a bullet infused with dark energy.",
        "mp": 20,
        "effect": 1.6,
        "state": "gun",
        "element": "darkness"  # Darkness element
    },

    # Magic Attacks (magic)
    "Fireball": {
        "description": "Launches a fireball at a target.",
        "mp": 15,
        "effect": 1.3,
        "state": "magic",
        "element": "fire"  # Fire element
    },
    "Ice Shard": {
        "description": "Summons a shard of ice to pierce the enemy.",
        "mp": 15,
        "effect": 1.3,
        "state": "magic",
        "element": "ice"  # Ice element
    },
    "Earthen Spike": {
        "description": "Summons a spike of earth to impale the enemy.",
        "mp": 20,
        "effect": 1.5,
        "state": "magic",
        "element": "earth"  # Earth element
    },
    "Dark Pulse": {
        "description": "Unleashes a wave of dark energy.",
        "mp": 25,
        "effect": 1.7,
        "state": "magic",
        "element": "darkness"  # Darkness element
    },
    "Sonic Boom": {
        "description": "Creates a powerful sound wave to damage enemies.",
        "mp": 20,
        "effect": 1.6,
        "state": "magic",
        "element": "sound"  # Sound element
    },
    "Glass Storm": {
        "description": "Summons a storm of razor-sharp glass shards.",
        "mp": 30,
        "effect": 1.8,
        "state": "magic",
        "element": "glass"  # Glass element
    },
    "Inferno Burst": {
        "description": "Unleashes a massive explosion of fire.",
        "mp": 35,
        "effect": 2.0,
        "state": "magic",
        "element": "explosion"  # Explosion element
    }   
    }

    return Attack_List

def monster_drop_list():
    monster_drop_tables = {
    # Bat
    "Bat": {
        "Bat Wing": 30,  # 30% chance to drop a Bat Wing
        "Herb": 10,      # 10% chance to drop a Herb
    },

    # Bee
    "Bee": {
        "Honey": 25,     # 25% chance to drop Honey
        "Stinger": 15,   # 15% chance to drop a Stinger
    },

    # Mouse
    "Mouse": {
        "Cheese": 20,    # 20% chance to drop Cheese
        "Tail": 10,      # 10% chance to drop a Tail
    },

    # Spider
    "Spider": {
        "Spider Silk": 25,  # 25% chance to drop Spider Silk
        "Venom Sack": 10,   # 10% chance to drop a Venom Sack
    },

    # Slime
    "Slime": {
        "Herb": 50,      # 50% chance to drop a Herb
        "Slime Gel": 20, # 20% chance to drop Slime Gel
    },

    # Green Snake
    "Snake(Green)": {
        "Snake Skin": 30,  # 30% chance to drop Snake Skin
        "Venom Sack": 15,  # 15% chance to drop a Venom Sack
    },

    # Pink Snake
    "Snake(Pink)": {
        "Snake Skin": 40,  # 40% chance to drop Snake Skin
        "Venom Sack": 20,  # 20% chance to drop a Venom Sack
        "Rare Flower": 5,  # 5% chance to drop a Rare Flower
    },

    # Pink Snake
    "Scorpion": {
        "Snake Skin": 40,  # 40% chance to drop Snake Skin
        "Venom Sack": 20,  # 20% chance to drop a Venom Sack
        "Rare Flower": 5,  # 5% chance to drop a Rare Flower
    },

    # Phoenix (Fire-based rare enemy)
    "Phoenix": {
        "Phoenix Feather": 50,   # 50% chance to drop Phoenix Feather (used for revival items)
        "Flame Essence": 25,     # 25% chance to drop Flame Essence (used for fire-based crafting)
        "Sacred Ash": 10,        # 10% chance to drop Sacred Ash (rare material)
    },

    # Minotaur (Strong melee-type enemy)
    "Minotaur": {
        "Minotaur Horn": 40,     # 40% chance to drop Minotaur Horn (used for weapons/armor)
        "Beast Hide": 30,        # 30% chance to drop Beast Hide (used for crafting)
        "Warrior’s Medallion": 5,# 5% chance to drop Warrior’s Medallion (rare accessory)
    },

    # Treant (Nature-based monster)
    "Treant": {
        "Ancient Bark": 45,      # 45% chance to drop Ancient Bark (used in alchemy)
        "Dryad Leaf": 25,        # 25% chance to drop Dryad Leaf (used for healing potions)
        "Spirit Core": 15,       # 15% chance to drop Spirit Core (used for enchantments)
    },
    "Alligator": {

    },
    "Armagiro": {

    },
    "Crub": {

    },
    "Frog(blue)": {

    },
    "Frog(green)": {
        
    },
    "Cultist A": {
    },
    "Cultist B": {
    },
    "Turtle": {
    },
    "Octopus": {
    }
    }
    return monster_drop_tables

def monster_exp_list():
    monster_exp_values = {
    "Slime": 20,
    "Bat": 30,
    "Bee": 50,
    "Mouse": 40,
    "Spider": 60,
    "Scorpion":28,
    "Snake(Green)": 80,
    "Snake(Pink)": 100,
    "Alligator": 110,
    "Armagiro": 110,
    "Crub": 110,
    "Frog(blue)": 80,
    "Frog(green)": 80,
    "Octpus": 100,
    "Turtle": 90,
    "Phoenix": 200,
    "Minotaur": 200,
    "Treant": 100,
    "Cultist A": 200,
    "Cultist B": 200,
    }
    return monster_exp_values


