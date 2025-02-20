# Group1 Dragon Quest

A Dragon Quest–inspired RPG game built with Python and Pygame. The project features multiple maps, dynamic transitions, NPC interactions, menu systems, battle scenes, and a music manager to create an immersive game experience.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Controls](#controls)
- [Credits](#credits)
- [License](#license)

## Features

- **Multiple Maps & Transitions:** Experience different environments (town, dungeon, shop) with seamless transitions.
- **Dynamic Music Management:** Each map has its own background music which changes automatically during transitions.
- **NPC Interactions:** Engage in dialogue with various characters and access shop inventory.
- **Battle System:** Real-time battle scenes featuring turn-based combat, animations, and detailed stat displays.
- **Menu System:** Access character status, inventory, quests, and other game options through a pause menu.
- **Custom Sprite Animations:** Dynamic sprite animations for characters, NPCs, and enemies.

## Prerequisites

- **Python 3.6+**
- **Pygame**  
  Install via:
  ```bash
  pip install pygame
  ```

## Installation

Clone the repository:
```bash
git clone https://10.21.75.193/csnt-161/lab-assignment-2/group1-dragonquest.git
```
Navigate into the project directory:
```bash
cd group1-dragonquest
```
Install dependencies: Make sure Pygame is installed using the command shown above.

## Usage

Run the main game file:
```bash
python main.py
```
Enjoy the game! The game window opens with the initial town map, background music, and visible NPCs.

## File Structure

group1-dragonquest

├── main.py                  # Main game loop and initialization

├── character.py             # Defines player, NPC, and enemy 

classes

├── battle.py                # Contains the battle system and animations

├── map_manager.py           # Manages maps, camera updates, and transitions

├── menu.py                  # In-game menu system for status, inventory, etc.

├── items.py                 # Definitions for items and attacks

├── Draw.py                  # Utility functions for drawing and music management

├── utilities.py             # Additional helper functions and utilities

├── poc.py                   # Proof-of-concept file for testing collisions and transitions

└── README.md                # This file

## Controls

Movement: Arrow keys (Up, Down, Left, Right) move the character.

Interactions:
Press E near an NPC to start a dialogue.

Press Enter to continue dialogue.

Menu: Press M to open or close the in-game menu.

Battle Options: Within battle scenes, use designated keys/buttons to attack, use items, or escape.

## Credits

Developed by Gabriel Paquette and Reyia Ihara

Music and assets have been ethically borrowed

Map design by Belle Stott

Inspired by classic Dragon Quest-style RPG games.
