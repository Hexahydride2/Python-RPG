import pygame
import json
import os
from pathlib import Path
from character import Character, Party
from Maps import map_configs
from map_manager import Map
from new_opening import opening_scene



class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.player = None  # Player instance
        self.save_file = "save_data.json"

        self.save_file

        # Main menu display
        self.options = ["New Game", "Continue", "Delete Data"]
        self.selected_option_index = 0
        self.selecting_new_game = False
        self.selecting_contine = 0
        self.selected_save_data_index = 0
        self.scroll_offset = 0
        self.visible_save_data = 8
        self.running = True

        # Get all the save data
        self.save_data_list = []
        directory = "SaveData"
        for root, dirs, files in os.walk(directory):
            for file in files:
                self.save_data_list.append(os.path.join(root, file))

        
        # Load background image
        self.background_image = pygame.image.load("Backgrounds\main_menu.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))

    def new_game(self, name):
        """Starts a new game by creating a character."""
        self.player = Character(name, 
                                x=1200, 
                                y=570, 
                                folder_paths=[
            R"timefantasy_characters\timefantasy_characters\frames\chara\chara1_1",
            R"tf_svbattle\singleframes\set1\1"
        ],                      level=1, 
                                hp=100, 
                                mp=50, 
                                atk=20, 
                                dfn=10, 
                                spd=5, 
                                inventory={
                                        "Potion": 3,
                                        "Mana Crystal": 3
                                            }, 
                                scale_factor=1)
        
        num_save_data = len(self.save_data_list)
        file_path = f"SaveData/Data{num_save_data + 1}.json"
        self.player_party = Party(self.player)
        # initial save
        self.save_game(file_path=file_path, current_map_id="Town_mapv1")
        self.running = False
        self.save_file = file_path
        opening_scene(self.screen, self.player_party)

    def save_game(self, file_path, current_map_id):
        """Saves the game state to a JSON file."""
        party_data = []
        for member in self.player_party.members + self.player_party.storage:
            member_data = {
                "name": member.name,
                "x": member.x,
                "y": member.y,
                "level": member.level,
                "hp": member.hp,
                "max_hp": member.max_hp,
                "mp": member.mp,
                "max_mp": member.max_mp,
                "atk": member.atk,
                "dfn": member.dfn,
                "spd": member.spd,
                "inventory": member.inventory,
                "gold": member.gold,
                "skills": member.skills,
                "folder_paths": member.folder_paths,
                "exp": member.exp,
                "scale_factor": member.scale_factor
            }
            party_data.append(member_data)
        game_state = {
            "current_map": current_map_id,
            "party_data": party_data
        }
        with open(file_path, "w") as file:
            json.dump(game_state, file, indent=4)

    def load_game(self, save_file):
        """Loads the game state from a JSON file."""
        with open(save_file, "r") as file:
            data = json.load(file)
        # Load party members from party_data
        self.members = []
        for member_data in data["party_data"]:
            character = Character(
                name=member_data["name"],
                x=member_data["x"],
                y=member_data["y"],
                folder_paths=member_data["folder_paths"],
                level=member_data["level"],
                hp=member_data["hp"],
                mp=member_data["mp"],
                atk=member_data["atk"],
                dfn=member_data["dfn"],
                spd=member_data["spd"],
                inventory=member_data["inventory"],
                gold=member_data["gold"],
                skills=member_data["skills"],
                scale_factor=member_data["scale_factor"]
            )
            character.max_hp = member_data["max_hp"]
            character.max_mp = member_data["max_mp"]
            character.exp = member_data["exp"]
            self.members.append(character)
        
        # Build the party
        for i, member in enumerate(self.members):
            if i == 0:
                self.player_party = Party(member)
            else:
                self.player_party.add_member(member)
        
        saved_map_id = data["current_map"]
        return self.player_party, saved_map_id
       
    def load_map(self, map_id, screen, player_party):
        config = map_configs.get(map_id)
        if config:
            map_instance = Map(
                screen=screen,
                map_image_path=config["map_image_path"],
                player_party=player_party,
                npcs=config.get("npcs", []),
                enemies=config.get("enemies", []),
                map_scale_factor=config.get("map_scale_factor"),
                bgm=config.get("bgm"),
                layer_json_path=config.get("layer_json_path"),
                allow_encounters=config.get("allow_encounters", False),
                encounter_rate=config.get("encounter_rate", 0),
                transitions=config.get("transitions", [])
            )
            map_instance.config_key = map_id
            return map_instance
        else:
            raise ValueError(f"Map {map_id} is not defined.")

    def delete_game_data(self):
        """Deletes the saved game data."""
        if os.path.exists(self.save_file):
            os.remove(self.save_file)
            print("Game data deleted.")
        else:
            print("No save file to delete.")

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        if self.selecting_new_game:
            self.new_game_ui()
        elif self.selecting_contine:
            self.draw_continue()
        else:
            self.draw_main_menu()

    def draw_main_menu(self):
        font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 28)
        BUTTON_WIDTH = self.screen.get_width()*0.3
        BUTTON_HEIGHT = self.screen.get_height()*0.1
        BUTTON_MARGIN = 20

        for i, label in enumerate(self.options):
            button_x = (self.screen.get_width() - BUTTON_WIDTH) // 2
            button_y = (self.screen.get_height() - (len(self.options) * (BUTTON_HEIGHT + BUTTON_MARGIN))) // 2 + i * (BUTTON_HEIGHT + BUTTON_MARGIN)

            if i == self.selected_option_index:
                color = (200, 200, 200, 200)
            else:
                color = (10, 10, 10, 200)

            rect_surface = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(rect_surface, color, (0, 0, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=10)            
            self.screen.blit(rect_surface, (button_x, button_y))

            pygame.draw.rect(self.screen, (245, 245, 245), (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT), width=2, border_radius=10) # Border

            # Render the text
            text = font.render(label, True, (255, 255, 255))
            text_rect = text.get_rect(center=(button_x + BUTTON_WIDTH // 2, button_y + BUTTON_HEIGHT // 2))  # Center the text
            self.screen.blit(text, text_rect)
    
    def draw_continue(self):
        base_x, base_y = self.screen.get_width()*0.25, self.screen.get_height()*0.2
        width, height = self.screen.get_width()*0.25, self.screen.get_height()*0.6
        # Print the list of file paths
        file_names = [Path(path).stem for path in self.save_data_list]

        # Left Pane
        rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(rect_surface, (10, 10, 10, 200), (0, 0, width, height), border_radius=10)            
        self.screen.blit(rect_surface, (base_x, base_y))
        pygame.draw.rect(self.screen, (245, 245, 245), (base_x, base_y, width, height), width=2, border_radius=10) # Border

        # Right Pane
        rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(rect_surface, (10, 10, 10, 200), (0, 0, width, height), border_radius=10)            
        self.screen.blit(rect_surface, (base_x + width + 10, base_y))
        pygame.draw.rect(self.screen, (245, 245, 245), (base_x + width + 10, base_y, width, height), width=2, border_radius=10) # Border

        font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 30)
        for i in range(self.scroll_offset, min(self.scroll_offset + self.visible_save_data, len(file_names))):
            color = (245, 245, 245) if i == self.selected_save_data_index else (150, 150, 150)
            text = font.render(file_names[i], True, color)
            self.screen.blit(text, (base_x + 10, base_y + 10 + (i - self.scroll_offset)*40))

        desc_font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 26)
        with open(self.save_data_list[self.selected_save_data_index], "r") as file:
            data = json.load(file)
        members = []
        for member in data["party_data"]:
            members.append(member)

        current_map = desc_font.render(f"Map: {data["current_map"]}", True, (245, 245, 245))
        self.screen.blit(current_map, (base_x + width + 20, base_y+10))

        party = desc_font.render(f"Party Info:", True, (245, 245, 245))
        self.screen.blit(party, (base_x + width + 20, base_y+40))

        for i in range(len(members)):
            leader_name = desc_font.render(f"  Name: {members[i]["name"]}", True, (245, 245, 245))
            self.screen.blit(leader_name, (base_x + width + 20, base_y+70 + i*60))

            leader_level = desc_font.render(f"  Lv. {members[i]["level"]}", True, (245, 245, 245))
            self.screen.blit(leader_level, (base_x + width + 20, base_y+100 + i*60))

        

        
        
        
        # Draw scrollbar if necessary
        total_save_data = len(self.save_data_list)
        inventory_x, inventory_y = base_x, base_y
        scrollbar_width = 10
        self.max_scroll = max(0, total_save_data - self.visible_save_data)
        
        scrollbar_x = inventory_x + width - 15  # Right edge for the scrollbar
        if total_save_data > self.visible_save_data:
            # Scroll indicator height
            scroll_indicator_height = max(30, (self.visible_save_data / total_save_data) * height)
            # Scroll indicator position (proportional to scroll offset)
            scroll_indicator_y = inventory_y + (self.scroll_offset / self.max_scroll) * (height - scroll_indicator_height)
            # Draw scroll indicator
            pygame.draw.rect(self.screen, (255, 255, 255), (scrollbar_x, scroll_indicator_y, scrollbar_width, scroll_indicator_height), border_radius=5)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.selecting_contine:
                if event.key == pygame.K_DOWN:
                    if self.selected_save_data_index < len(self.save_data_list) - 1:
                        self.selected_save_data_index += 1
                        if self.selected_save_data_index >= self.scroll_offset + self.visible_save_data:
                            self.scroll_offset += 1
                   
                elif event.key == pygame.K_UP:
                    if self.selected_save_data_index > 0:
                        self.selected_save_data_index -= 1
                        if self.selected_save_data_index < self.scroll_offset:
                            self.scroll_offset -= 1
                    
                elif event.key == pygame.K_RETURN:
                    self.select_continue()

                elif event.key == pygame.K_ESCAPE:
                    self.selecting_contine = False                    

            else:
                if event.key == pygame.K_DOWN:
                    self.selected_option_index = (self.selected_option_index + 1) % len(self.options)
                elif event.key == pygame.K_UP:
                    self.selected_option_index = (self.selected_option_index - 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.select_option()
    
    def select_option(self):
        selected_option = self.options[self.selected_option_index]
        
        if selected_option == "New Game":
            self.selecting_new_game = True
        elif selected_option == "Continue":
            self.selecting_contine = True
    
    def select_continue(self):
        selected_save_data = self.save_data_list[self.selected_save_data_index]
        self.save_file = selected_save_data
        self.running = False


    def new_game_ui(self):
        """Displays a UI for selecting a character and entering a name using keyboard input."""
        pygame.font.init()
        font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 33)
        BUTTON_WIDTH = 400  # Width of the input box
        BUTTON_HEIGHT = 50  # Height of the input box
        input_box = pygame.Rect((self.screen.get_width() - BUTTON_WIDTH) // 2, self.screen.get_height()//2, BUTTON_WIDTH, BUTTON_HEIGHT)  # Centered input box
        color = pygame.Color((245, 245, 245))  # Color when the box is active
        
        active = True  # Input box is always active (no mouse needed)
        text = ''  # Variable to store the user's input
        clock = pygame.time.Clock()
        cursor_visible = True  # Tracks whether the cursor is visible
        cursor_timer = 0  # Tracks the time for cursor blinking
        cursor_blink_interval = 300  # Cursor blink interval in milliseconds

        running = True
        while running:
            # Update cursor blinking
            cursor_timer += clock.get_time()
            if cursor_timer >= cursor_blink_interval:
                cursor_visible = not cursor_visible  # Toggle cursor visibility
                cursor_timer = 0  # Reset the timer
            self.screen.blit(self.background_image, (0, 0))

            # Render the "Please enter a name."
            rect_surface = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(rect_surface, (10, 10, 10, 200), (0, 0, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=10)            
            self.screen.blit(rect_surface, (input_box.x, input_box.y - BUTTON_HEIGHT - 30))
            pygame.draw.rect(self.screen, (245, 245, 245), (input_box.x, input_box.y - BUTTON_HEIGHT - 30, BUTTON_WIDTH, BUTTON_HEIGHT), width=2, border_radius=10) # Border

            navigation = font.render("Please enter a name.", True, (255, 255, 255))
            navigation_rect = navigation.get_rect(center=(input_box.x + BUTTON_WIDTH // 2, input_box.y - BUTTON_HEIGHT -30 + BUTTON_HEIGHT // 2))  # Center the text
            self.screen.blit(navigation, navigation_rect)
            
            # Render the input box with a semi-transparent black background and white border
            rect_surface = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(rect_surface, (10, 10, 10, 200), (0, 0, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=10)  # Semi-transparent black rectangle
            pygame.draw.rect(rect_surface, (245, 245, 245), (0, 0, BUTTON_WIDTH, BUTTON_HEIGHT), width=2, border_radius=10)  # White border
            self.screen.blit(rect_surface, (input_box.x, input_box.y))

            # Render the input box and text
            txt_surface = font.render(text, True, (255, 255, 255))  # White text
            text_x = input_box.x + 10  # Padding from the left edge of the input box
            text_y = input_box.y + (BUTTON_HEIGHT - txt_surface.get_height()) // 2  # Vertically center the text
            self.screen.blit(txt_surface, (text_x, text_y))

            # Render the blinking cursor
            if cursor_visible:
                cursor_x = input_box.x + 8 + txt_surface.get_width()
                cursor_y = input_box.y + 8
                cursor_height = font.get_height()
                pygame.draw.line(self.screen, color, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:  # Press Enter to confirm the name
                            if text.strip():  # Ensure the name is not empty
                                print(f"Character Name: {text}")
                                self.new_game(text)  # Start a new game with the entered name
                                running = False
                                self.selecting_new_game = False
                        elif event.key == pygame.K_ESCAPE:  # Press ESC to go back to the main menu
                            self.selecting_new_game = False
                            running = False
                        elif event.key == pygame.K_BACKSPACE:  # Press Backspace to delete a character
                            text = text[:-1]
                        else:
                            text += event.unicode  # Add the typed character to the input

            pygame.draw.rect(self.screen, color, input_box, 2)  # Draw the input box rectangle
            pygame.display.flip()  # Update the display
            clock.tick(30)  # Cap the frame rate

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))  # Clear the screen
            self.draw()
            # Your game logic here (draw player, handle movement, etc.)
            # if game_manager.player:
            #     print(f"Current Player: {game_manager.player.name}, Level: {game_manager.player.level}")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_input(event)

            pygame.display.flip()  # Update the screen
        return self.save_file
