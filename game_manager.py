import pygame
import json
import os
from character import Character, Party

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.player = None  # Player instance
        self.save_file = "save_data.json"

    def new_game(self, name, character_folder):
        """Starts a new game by creating a character."""
        self.player = Character(name, x=100, y=100, folder_paths=[
            R"timefantasy_characters\timefantasy_characters\frames\chara\chara1_1",
            R"tf_svbattle\singleframes\set1\1"
        ], level=1, hp=100, mp=50, atk=10, dfn=5, spd=5, scale_factor=1)
        print(f"New Game Started: {self.player.name}")

    def save_game(self, file_path):
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
        
        with open(file_path, "w") as file:
            json.dump(party_data, file, indent=4)

    def load_game(self, save_file):
        """Loads the game state from a JSON file."""
        with open(save_file, "r") as file:
            party_data = json.load(file)
            self.members = []  # Clear existing members
            for member_data in party_data:
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
            
            for i, member in enumerate(self.members):
                if i == 0:
                    self.player_party = Party(member)
                else:
                    self.player_party.add_member(member)
            
            return self.player_party
       

    def delete_game_data(self):
        """Deletes the saved game data."""
        if os.path.exists(self.save_file):
            os.remove(self.save_file)
            print("Game data deleted.")
        else:
            print("No save file to delete.")

    def main_menu(self):
        """Displays the main menu with New Game, Continue, and Delete Data options."""
        pygame.font.init()
        font = pygame.font.Font(None, 50)
        clock = pygame.time.Clock()

        new_game_rect = pygame.Rect(200, 200, 200, 50)
        continue_rect = pygame.Rect(200, 300, 200, 50)
        delete_rect = pygame.Rect(200, 400, 200, 50)

        running = True
        while running:
            self.screen.fill((30, 30, 30))
            new_game_text = font.render("New Game", True, (255, 255, 255))
            continue_text = font.render("Continue", True, (255, 255, 255))
            delete_text = font.render("Delete Data", True, (255, 255, 255))
            
            pygame.draw.rect(self.screen, (50, 50, 200), new_game_rect)
            pygame.draw.rect(self.screen, (50, 200, 50), continue_rect)
            pygame.draw.rect(self.screen, (200, 50, 50), delete_rect)
            
            self.screen.blit(new_game_text, (new_game_rect.x + 20, new_game_rect.y + 10))
            self.screen.blit(continue_text, (continue_rect.x + 20, continue_rect.y + 10))
            self.screen.blit(delete_text, (delete_rect.x + 20, delete_rect.y + 10))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if new_game_rect.collidepoint(event.pos):
                        self.new_game_ui()
                        running = False
                    elif continue_rect.collidepoint(event.pos):
                        self.load_game()
                        running = False
                    elif delete_rect.collidepoint(event.pos):
                        self.delete_game_data()
            clock.tick(30)

    def new_game_ui(self):
        """Displays a UI for selecting a character and entering a name."""
        pygame.font.init()
        font = pygame.font.Font(None, 36)
        input_box = pygame.Rect(200, 200, 400, 50)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        clock = pygame.time.Clock()

        running = True
        while running:
            self.screen.fill((30, 30, 30))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            print(f"Character Name: {text}")
                            self.new_game(text, ["player_sprites"])
                            running = False
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            txt_surface = font.render(text, True, color)
            width = max(400, txt_surface.get_width() + 10)
            input_box.w = width
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(self.screen, color, input_box, 2)
            pygame.display.flip()
            clock.tick(30)

   