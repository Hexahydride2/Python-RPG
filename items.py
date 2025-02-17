def items_list():
    All_Item_List = {
        "Potion": {
            "description": "Restores 10 HP. A basic healing drink.",
            "type": "hp",
            "effect": 10,
            "price": 10
        },
        "Super Potion": {
            "description": "Restores 50 HP. A stronger variant of the potion.",
            "type": "hp",
            "effect": 50,
            "price": 50
        },
        "Mana Crystal": {
            "description": "Restores 10 MP. A small glowing crystal filled with energy.",
            "type": "mp",
            "effect": 10,
            "price": 12
        },
        "Ether": {
            "description": "Restores 50 MP. A refined magical liquid that energizes the mind.",
            "type": "mp",
            "effect": 50,
            "price": 40
        },
        "Elixir": {
            "description": "Restores both 30 HP and 30 MP. A magical drink.",
            "type": "both",
            "effect": (30, 30),
            "price": 75
        },
        "Antidote": {
            "description": "Cures poison and other harmful debuffs.",
            "type": "status",
            "effect": "cure_poison",
            "price": 20
        },
        "Revive": {
            "description": "Revives a fallen ally with 25% of their HP.",
            "type": "revive",
            "effect": 25,
            "price": 150
        },
        "Healing Herb": {
            "description": "A basic herb that restores 5 HP.",
            "type": "hp",
            "effect": 5,
            "price": 5
        },
        "Big Bomb": {
            "description": "Deals 100 damage to all enemies in range.",
            "type": "attack",
            "effect": 100,
            "price": 200
        },
        "Fire Scroll": {
            "description": "Deals 50 fire damage to a single target.",
            "type": "attack",
            "effect": 50,
            "price": 80
        },
        "Ice Orb": {
            "description": "Deals 60 ice damage and freezes a target.",
            "type": "attack",
            "effect": 60,
            "price": 90
        },
        "Wind Amulet": {
            "description": "Increases movement speed by 10%.",
            "type": "buff",
            "effect": "speed_up",
            "price": 120
        },
        "Strength Potion": {
            "description": "Temporarily increases attack by 20.",
            "type": "buff",
            "effect": "atk_up",
            "price": 50
        },
        "Defense Shield": {
            "description": "Temporarily boosts defense by 15.",
            "type": "buff",
            "effect": "dfn_up",
            "price": 60
        },
        "Cloak of Invisibility": {
            "description": "Makes you invisible for 5 turns.",
            "type": "buff",
            "effect": "invisibility",
            "price": 150
        },
        "Crystal of Wisdom": {
            "description": "Increases magic power by 10.",
            "type": "buff",
            "effect": "mp_up",
            "price": 70
        },
        "Gold Coin": {
            "description": "A shiny gold coin. Can be used for trading.",
            "type": "currency",
            "effect": 1,
            "price": 0  # Gold coins can be used in trade
        },
        "Mithril Ore": {
            "description": "A rare ore that can be used for crafting.",
            "type": "material",
            "effect": "mithril",
            "price": 250
        },
        "Giga Health Potion": {
            "description": "Restores 100 HP. A very potent healing item.",
            "type": "hp",
            "effect": 100,
            "price": 120
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
