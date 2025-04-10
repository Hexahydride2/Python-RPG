# Group1 Dragon Quest

An immersive Dragon Quest-inspired RPG built with Python and Pygame, featuring dynamic maps, engaging battles, and interactive NPC conversations.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Controls](#controls)
- [Battle System](#battle-system)
- [Credits](#credits)

## Overview

Group1 Dragon Quest is a turn-based RPG game that captures the nostalgic essence of classic JRPGs while implementing modern programming practices. Navigate through various maps, interact with NPCs, engage in strategic battles, and progress through an engaging storyline.

## Features

- **Rich World Environment:** Multiple detailed maps including towns, dungeons, and shops with seamless transitions
- **Dynamic Character System:** Customizable player characters with stats, equipment, and skills
- **Strategic Turn-Based Combat:** Battle enemies with an intuitive combat system featuring attacks, skills, and items
- **Interactive NPCs:** Engage in dialogues, receive quests, and trade with merchants
- **Immersive Audio:** Dynamic soundtrack that changes based on location and battle status
- **Inventory Management:** Collect, use, and manage various items throughout your adventure
- **Status Effects:** Experience buffs, debuffs, and special conditions during battles

## Prerequisites

- **Python 3.6+**
- **Pygame**
- **Numpy**

## Installation

Clone the repository:
```bash
git clone https://10.21.75.193/csnt-161/lab-assignment-2/group1-dragonquest.git
```

Navigate into the project directory:
```bash
cd group1-dragonquest
```

Install dependencies:
```bash
pip install pygame, numpy
```

## Usage

Run the main game file:
```bash
python main.py
```

## Controls

### General Navigation
- **Arrow Keys:** Move character (Up, Down, Left, Right)
- **E:** Interact with NPCs/objects
- **Enter/Return:** Confirm selections, advance dialogue
- **M:** Open/close the game menu

### Battle Controls
- **Arrow Keys:** Navigate battle options and target selection
- **Enter/Return:** Select action
- **Escape:** Attempt to flee from battle (success rate varies)

### Menu Navigation
- **Arrow Keys:** Navigate menu options
- **Enter/Return:** Select menu item
- **Escape/M:** Close current menu

## Battle System

The battle system features turn-based combat with the following elements:

- **Turn Order:** Characters act based on speed stats
- **Action Types:** Attack, Defend, Use Item, Escape
- **Special Attacks:** Character-specific skills with MP costs
- **Status Effects:** Temporary stat changes affecting battle performance
- **Victory Rewards:** Experience points, gold, and item drops
- **Dynamic Difficulty:** Enemy strength scales with player progression

## Gameplay Demonstrations

**Battle Demonstration**

![](demonstration(battle).mp4)

**NPC hitbox reg + drawing**

![](demonstration(npc-hit-box-and-drawing-order-system).mp4)

**Transition Zones, Barriers, Talking to NPCs**

![](demonstration(transition-zone,-wall-hit-box,-and-communication-with-a-npc).mp4)

## Credits

- **Development Team:** Gabriel Paquette and Reyia Ihara
- **Map Design:** Belle Stott
- **Inspired by:** Classic Dragon Quest-style RPG games

<a href="https://www.flaticon.com/free-icons/buff" title="buff icons">Buff icons created by Freepik - Flaticon</a>

---

*This project was developed as part of a programming course assignment.*

