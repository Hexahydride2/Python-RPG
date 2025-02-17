def items_list():
    All_Item_List = {
        "Potion": {
            "description": "Restores 10 HP. A basic healing drink.",
            "type": "hp",
            "effect": 10
        },
        "Super Potion": {
            "description": "Restores 50 HP. A stronger variant of the potion.",
            "type": "hp",
            "effect": 50
        },
        "Mana Crystal": {
            "description": "Restores 10 MP. A small glowing crystal filled with energy.",
            "type": "mp",
            "effect": 10
        },
        "Ether": {
            "description": "Restores 50 MP. A refined magical liquid that energizes the mind.",
            "type": "mp",
            "effect": 50
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
    }
    return Attack_List
