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
        "type": "hp",
        "effect": "full",
        "price": 500
    },
    "Revive": {
        "description": "Revives a fallen ally with 50% of their HP.",
        "type": "re",
        "effect": 50,
        "price": 250
    },
    "Phoenix Feather": {
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
        "description": "Increases attack by 50 but lowers defense by 15 for 5 turns.",
        "type": "atk_buff",
        "effect": 50,
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
        "effect": 15,
        "duration": 3,
        "price": 140
    },
    "Shadow Cloak": {
        "description": "Increases speed by 30% for 3 turns.",
        "type": "spd_buff",
        "effect": 30,
        "duration": 3,
        "price": 180
    }
}

    return All_Item_List


def attack_list():
    Attack_List = {
        "Strike": {
            "description": "A swift melee attack.",
            "mp": 0,
            "effect": 1,
            "state": "atk1"
        },
        "Power Slash": {
            "description": "A heavy attack that deals increased damage.",
            "mp": 20,
            "effect": 1.5,
            "state": "atk2"
        },
        "Piercing Shot": {
            "description": "Fires an arrow at an enemy.",
            "mp": 10,
            "effect": 1.2,
            "state": "bow"
        },
        "Fireball": {
            "description": "Launches a fireball at a target.",
            "mp": 15,
            "effect": 1.3,
            "state": "magic"
        },        
    }
    return Attack_List
