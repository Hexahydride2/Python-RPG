import pygame
import json
from text_manager import TextManager
from game_manager import GameManager

class AdventurerGuild:
    def __init__(self, screen, player_party):
        self.screen = screen
        self.player_party = player_party
        self.clock = pygame.time.Clock()
        self.running = True
        self.quests = []  # List of available quests
        self.active_quests = []  # Quests currently being undertaken
        self.completed_quests = []  # Quests that have been completed
        self.party_rank = self.player_party.guild_rank  # Initial rank of the party
        self.rank_progress = 0  # Progress towards the next rank
        self.rank_thresholds = {  # Thresholds for rank progression
            "C": 100,
            "B": 300,
            "A": 600,
            "S": 1000
        }

        self.background_image = pygame.image.load("Backgrounds\guild.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))

        self.text_manager = TextManager(self.screen)

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
    
    def handle_input(self):
    

    
    def call_available_quests(self):
        with open("JsonData/quests.json", "r") as file:
            quests_data = json.load(file)
            available_quests = quests_data[self.party_rank]
            return available_quests
    
    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.draw()
            self.call_available_quests()

            pygame.display.update()
            self.clock.tick(30)

        pygame.quit()

    
# Example usage
pygame.init()
screen = pygame.display.set_mode((1280, 720))

game_manager = GameManager(screen)
player_party = game_manager.load_game(save_file="JsonData\data1.json")

adventurer_guild = AdventurerGuild(screen, player_party)
adventurer_guild.run()