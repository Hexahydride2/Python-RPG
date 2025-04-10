import sys
import os
from cx_Freeze import setup, Executable

# Create directories if they don't exist
directories = ['SaveData', 'Fonts']
for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Include all necessary packages and modules
build_exe_options = {
    "packages": [
        "pygame", "numpy", "json", "random", "re", "math", "time", "os", "pathlib"
    ],
    "includes": [
        "game_manager", "events", "utilities", "character", "Maps", 
        "map_manager", "text_manager", "scene", "battle", "menu", 
        "shop", "adventure_guild", "sprite", "items"
    ],
    "include_files": [
        "Backgrounds/", 
        "music/", 
        "timefantasy_characters/", 
        "Monsters/", 
        "tf_svbattle/", 
        "icons/",
        "Fonts/",
        "Sound_Effects/",
        "SE/",
        "sounds/",
        "images/",
        "JsonData/",
        "SaveData/",
        "craftpix-net-270096-free-forest-battle-backgrounds/"
    ]
}

setup(
    name="DragonQuest",
    version="1.1",
    description="Dragon Quest Game",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base="Win32GUI", icon="icons/dialog.png")]
)