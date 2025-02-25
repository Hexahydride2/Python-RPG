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
    }
}

    return All_Item_List


def attack_list():
    Attack_List = {
    # Basic Melee Attacks (atk1)
    "Strike": {
        "description": "A swift melee attack.",
        "mp": 0,
        "effect": 1,
        "state": "atk1"
    },
    "Slash": {
        "description": "A quick slash with a sword or axe.",
        "mp": 0,
        "effect": 1,
        "state": "atk1"
    },
    "Bash": {
        "description": "A blunt strike with a weapon.",
        "mp": 0,
        "effect": 1,
        "state": "atk1"
    },

    # Advanced Melee Attacks (atk2)
    "Power Slash": {
        "description": "A heavy attack that deals increased damage.",
        "mp": 20,
        "effect": 1.5,
        "state": "atk2"
    },
    "Cleave": {
        "description": "A wide swing that hits multiple enemies.",
        "mp": 25,
        "effect": 1.4,
        "state": "atk2"
    },
    "Whirlwind Strike": {
        "description": "A spinning attack that damages all nearby enemies.",
        "mp": 30,
        "effect": 1.6,
        "state": "atk2"
    },

    # Bow Attacks (bow)
    "Piercing Shot": {
        "description": "Fires an arrow at an enemy.",
        "mp": 10,
        "effect": 1.2,
        "state": "bow"
    },
    "Multi-Shot": {
        "description": "Fires multiple arrows at once.",
        "mp": 15,
        "effect": 1.3,
        "state": "bow"
    },
    "Snipe": {
        "description": "A precise shot that deals critical damage.",
        "mp": 20,
        "effect": 1.5,
        "state": "bow"
    },

    # Gun Attacks (gun)
    "Quick Shot": {
        "description": "A rapid shot from a gun.",
        "mp": 10,
        "effect": 1.2,
        "state": "gun"
    },
    "Buckshot": {
        "description": "Fires a spread of bullets at close range.",
        "mp": 15,
        "effect": 1.4,
        "state": "gun"
    },
    "Sniper Shot": {
        "description": "A high-precision shot that deals massive damage.",
        "mp": 25,
        "effect": 1.8,
        "state": "gun"
    },

    # Magic Attacks (magic)
    "Fireball": {
        "description": "Launches a fireball at a target.",
        "mp": 15,
        "effect": 1.3,
        "state": "magic"
    },
    "Ice Shard": {
        "description": "Summons a shard of ice to pierce the enemy.",
        "mp": 15,
        "effect": 1.3,
        "state": "magic"
    },
    "Thunderbolt": {
        "description": "Calls down a bolt of lightning to strike the enemy.",
        "mp": 20,
        "effect": 1.5,
        "state": "magic"
    },
    "Earthquake": {
        "description": "Shakes the ground to damage all enemies.",
        "mp": 30,
        "effect": 1.6,
        "state": "magic"
    },
    "Arcane Blast": {
        "description": "Unleashes a burst of pure magical energy.",
        "mp": 25,
        "effect": 1.7,
        "state": "magic"
    },
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
    "Snake(Green)": 80,
    "Snake(Pink)": 100,
    "Phoenix": 200,
    "Minotaur": 200,
    "Treant": 100
    }
    return monster_exp_values


