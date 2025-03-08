import pygame
import json
import time
from text_manager import TextManager

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

        self.quest_board_image = pygame.image.load("Backgrounds\quest_board1.png")
        self.quest_board_image = pygame.transform.scale(self.quest_board_image, (self.screen.get_height()*0.6, self.screen.get_height()))

        self.text_manager = TextManager(self.screen)

        self.options = ["Available Quests", "Active Quests", "Complete Quests"]
        self.selected_option_index = 0
        self.buttons = []

        self.selecting_quests = False
        self.selected_quest_index = 0
        self.viewing_active_quests = False
        self.selected_active_quest_index = 0
        self.viewing_complete_quests = False
        self.selected_complete_quest_index = 0
        self.scroll_offset = 0
        self.visible_quests = 10

        # Sound effects
        self.quest_complete_sound = pygame.mixer.Sound(R"Music\success-fanfare-trumpets.mp3")
        self.quest_complete_sound.set_volume(0.5)  # Adjust volume (0.0 to 1.0)

        self.level_up_sound = pygame.mixer.Sound(R"Sound_Effects\level-win.mp3")
        self.level_up_sound.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
        
        self.channel1 = pygame.mixer.Channel(1)
    

    def draw(self):
        if self.selecting_quests:
            self.draw_available_quests()
        elif self.viewing_active_quests:
            self.draw_active_quests()
        elif self.viewing_complete_quests:
            self.draw_complete_quests()
        else:
            self.draw_first_buttons()
        self.draw_guild_status()
        self.text_manager.update()
        self.text_manager.draw()
    
    def draw_guild_status(self):
        # Display player's current rank
        font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 28)
        
        base_x, base_y = self.screen.get_width()*0.1 - 20, self.screen.get_height()* 0.1
        self.draw_rectangle(base_x, base_y, 200, 100, alpha=200, border_radius=10)
        pygame.draw.rect(self.screen, (245, 245, 245), (base_x, base_y, 200, 100), width=2, border_radius=10) # Border

        rank = font.render(f"Rank: {self.player_party.guild_rank}", True, (255, 255, 255))
        self.screen.blit(rank, (base_x + 10, base_y + 10))

        point = font.render(f"Point: {self.player_party.guild_point}/{self.rank_thresholds[self.player_party.guild_rank]}", True, (255, 255, 255))
        self.screen.blit(point, (base_x + 10, base_y + 50))

    def draw_first_buttons(self):
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

            # Render the text
            text = font.render(label, True, (255, 255, 255))
            text_rect = text.get_rect(center=(button_x + BUTTON_WIDTH // 2, button_y + BUTTON_HEIGHT // 2))  # Center the text
            self.screen.blit(text, text_rect)

    def draw_available_quests(self):
        self.screen.blit(self.quest_board_image, (self.screen.get_width()//2 , 0))
        available_quests = self.call_available_quests()
        quest_list_width, quest_list_height = self.screen.get_width()*0.25, self.screen.get_height()*0.6
        base_x, base_y = self.screen.get_width()*0.25, self.screen.get_height()*0.2
        paper_x, paper_y = self.screen.get_width()//2 + 50, self.screen.get_height()*0.1

        self.draw_rectangle(base_x, base_y, quest_list_width, quest_list_height, alpha=200, border_radius=10)
        pygame.draw.rect(self.screen, (245, 245, 245), (base_x, base_y, quest_list_width, quest_list_height), width=2, border_radius=10) # Border
        # self.draw_rectangle(base_x + quest_list_width +10, base_y, quest_list_width, quest_list_height*0.8, alpha=200, border_radius=10)
        # pygame.draw.rect(self.screen, (245, 245, 245), (base_x + quest_list_width +10, base_y, quest_list_width, quest_list_height* 0.8), width=2, border_radius=10) # Border

        font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 26)
        for i in range(self.scroll_offset, min(self.scroll_offset + self.visible_quests, len(available_quests))):
            color = (255, 255, 255) if i == self.selected_quest_index else (150, 150, 150)
            text = font.render(available_quests[i]["name"], True, color)
            self.screen.blit(text, (base_x+10, base_y+10 + (i - self.scroll_offset) * 40))
        
        title_font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 26)
        desc_font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 22)
        reward_font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 24)
        obj_font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 24)
        selected_quest = available_quests[self.selected_quest_index]

        # Display quest name
        title_text = title_font.render(selected_quest["name"], True, (200, 50, 50))
        self.screen.blit(title_text, (paper_x, paper_y))

        # Display quest description
        wrapped_description = self.wrap_text(selected_quest["description"], desc_font,  self.screen.get_height()*0.6 - 80)
        paper_y += 50
        for i, line in enumerate(wrapped_description):
            description_text = desc_font.render(line, True, (10, 10, 10))
            paper_y += 30
            self.screen.blit(description_text, (paper_x, paper_y))
        
        # Display quest objective
        paper_y += 50
        obj_text = obj_font.render('Objective', True, (50, 200, 50))
        self.screen.blit(obj_text, (paper_x, paper_y))
        paper_y += 30
        type_text = reward_font.render(f"Type: {selected_quest['objective']['type']}", True, (10, 10, 10))
        self.screen.blit(type_text, (paper_x+50, paper_y))
        paper_y += 30
        target_text = reward_font.render(f"Target: {selected_quest['objective']['target']} x{selected_quest['objective']['count']}", True, (10, 10, 10))
        self.screen.blit(target_text, (paper_x+50, paper_y))
        
        # Display quest reward
        paper_y += 50
        reward_text = reward_font.render("Reward", True, (50, 200, 50))
        self.screen.blit(reward_text, (paper_x, paper_y))
        paper_y += 30
        money_text = reward_font.render(f"Gold: {selected_quest['reward']['gold']} G", True, (10, 10, 10))
        self.screen.blit(money_text, (paper_x+50, paper_y))
        paper_y += 30
        
        items_text = reward_font.render(f"Items:", True, (10, 10, 10))
        self.screen.blit(items_text, (paper_x+50,  paper_y))

        for item in selected_quest["reward"]["items"]:
            item_text = reward_font.render(item, True, (10, 10, 10))
            self.screen.blit(item_text, (paper_x + 120, paper_y))
            paper_y += 30
        
        
        # Draw scrollbar if necessary
        total_items = len(available_quests)
        inventory_x, inventory_y = base_x, base_y
        scrollbar_width = 10
        self.max_scroll = max(0, total_items - self.visible_quests)
        
        scrollbar_x = inventory_x + quest_list_width - 15  # Right edge for the scrollbar
        if total_items > self.visible_quests:
            # Scroll indicator height
            scroll_indicator_height = max(30, (self.visible_quests / total_items) * quest_list_height)

            # Scroll indicator position (proportional to scroll offset)
            scroll_indicator_y = inventory_y + (self.scroll_offset / self.max_scroll) * (quest_list_height - scroll_indicator_height)

            # Draw scroll indicator
            pygame.draw.rect(self.screen, (255, 255, 255), (scrollbar_x, scroll_indicator_y, scrollbar_width, scroll_indicator_height), border_radius=5)

    def draw_active_quests(self):
        self.screen.blit(self.quest_board_image, (self.screen.get_width()//2 , 0))
        active_quests = self.player_party.current_quests
        quest_list_width, quest_list_height = self.screen.get_width()*0.25, self.screen.get_height()*0.6
        base_x, base_y = self.screen.get_width()*0.25, self.screen.get_height()*0.2
        paper_x, paper_y = self.screen.get_width()//2 + 50, self.screen.get_height()*0.1

        self.draw_rectangle(base_x, base_y, quest_list_width, quest_list_height, alpha=200, border_radius=10)
        pygame.draw.rect(self.screen, (245, 245, 245), (base_x, base_y, quest_list_width, quest_list_height), width=2, border_radius=10) # Border

        font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 26)
        for i in range(self.scroll_offset, min(self.scroll_offset + self.visible_quests, len(active_quests))):
            color = (255, 255, 255) if i == self.selected_active_quest_index else (150, 150, 150)
            text = font.render(active_quests[i]["name"], True, color)
            self.screen.blit(text, (base_x+10, base_y+10 + (i - self.scroll_offset) * 40))
        
        title_font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 26)
        desc_font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 22)
        reward_font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 24)
        obj_font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 24)
        selected_quest = active_quests[self.selected_active_quest_index]

        # Display quest name
        title_text = title_font.render(selected_quest["name"], True, (200, 50, 50))
        self.screen.blit(title_text, (paper_x, paper_y))

        # Display quest description
        wrapped_description = self.wrap_text(selected_quest["description"], desc_font,  self.screen.get_height()*0.6 - 80)
        paper_y += 50
        for i, line in enumerate(wrapped_description):
            description_text = desc_font.render(line, True, (10, 10, 10))
            paper_y += 30
            self.screen.blit(description_text, (paper_x, paper_y))

        # Display quest objective
        paper_y += 50
        obj_text = obj_font.render("Objective", True, (50, 200, 50))
        self.screen.blit(obj_text, (paper_x, paper_y))
        paper_y += 30
        type_text = reward_font.render(f"Type: {selected_quest['objective']['type']}", True, (10, 10, 10))
        self.screen.blit(type_text, (paper_x+50, paper_y))
        paper_y += 30
        target_text = reward_font.render(f"Target: {selected_quest['objective']['target']} x{selected_quest['objective']['count']}", True, (10, 10, 10))
        self.screen.blit(target_text, (paper_x+50, paper_y))
        
        # Display quest reward
        paper_y += 50
        reward_text = reward_font.render("Reward", True, (50, 200, 50))
        self.screen.blit(reward_text, (paper_x, paper_y))
        paper_y += 30
        money_text = reward_font.render(f"Gold: {selected_quest['reward']['gold']} G", True, (10, 10, 10))
        self.screen.blit(money_text, (paper_x+50, paper_y))
        paper_y += 30
        
        items_text = reward_font.render(f"Items:", True, (10, 10, 10))
        self.screen.blit(items_text, (paper_x+50,  paper_y))

        for item in selected_quest["reward"]["items"]:
            item_text = reward_font.render(item, True, (10, 10, 10))
            self.screen.blit(item_text, (paper_x + 120, paper_y))
            paper_y += 30
        
        
        # Draw scrollbar if necessary
        total_items = len(active_quests)
        inventory_x, inventory_y = base_x, base_y
        scrollbar_width = 10
        self.max_scroll = max(0, total_items - self.visible_quests)
        
        scrollbar_x = inventory_x + quest_list_width - 15  # Right edge for the scrollbar
        if total_items > self.visible_quests:
            # Scroll indicator height
            scroll_indicator_height = max(30, (self.visible_quests / total_items) * quest_list_height)

            # Scroll indicator position (proportional to scroll offset)
            scroll_indicator_y = inventory_y + (self.scroll_offset / self.max_scroll) * (quest_list_height - scroll_indicator_height)

            # Draw scroll indicator
            pygame.draw.rect(self.screen, (255, 255, 255), (scrollbar_x, scroll_indicator_y, scrollbar_width, scroll_indicator_height), border_radius=5)

    def draw_complete_quests(self):
        self.screen.blit(self.quest_board_image, (self.screen.get_width()//2 , 0))
        complete_quests = self.call_complete_quests()
        quest_list_width, quest_list_height = self.screen.get_width()*0.25, self.screen.get_height()*0.6
        base_x, base_y = self.screen.get_width()*0.25, self.screen.get_height()*0.2
        paper_x, paper_y = self.screen.get_width()//2 + 50, self.screen.get_height()*0.1

        self.draw_rectangle(base_x, base_y, quest_list_width, quest_list_height, alpha=200, border_radius=10)
        pygame.draw.rect(self.screen, (245, 245, 245), (base_x, base_y, quest_list_width, quest_list_height), width=2, border_radius=10) # Border

        font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 26)
        for i in range(self.scroll_offset, min(self.scroll_offset + self.visible_quests, len(complete_quests))):
            color = (255, 255, 255) if i == self.selected_quest_index else (150, 150, 150)
            text = font.render(complete_quests[i]["name"], True, color)
            self.screen.blit(text, (base_x+10, base_y+10 + (i - self.scroll_offset) * 40))
        
        title_font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 26)
        desc_font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 22)
        reward_font = pygame.font.Font(".\Fonts\RotisSerif.ttf", 24)

        print(complete_quests)
        print(self.selected_complete_quest_index)
        selected_quest = complete_quests[self.selected_complete_quest_index]

        # Display quest name
        title_text = title_font.render(selected_quest["name"], True, (200, 50, 50))
        self.screen.blit(title_text, (paper_x, paper_y))

        # Display quest description
        wrapped_description = self.wrap_text(selected_quest["description"], desc_font,  self.screen.get_height()*0.6 - 80)
        paper_y += 50
        for i, line in enumerate(wrapped_description):
            description_text = desc_font.render(line, True, (10, 10, 10))
            paper_y += 30
            self.screen.blit(description_text, (paper_x, paper_y))
 
        # Display quest reward
        paper_y += 50
        reward_text = reward_font.render("Reward", True, (50, 200, 50))
        self.screen.blit(reward_text, (paper_x, paper_y))
        paper_y += 30
        money_text = reward_font.render(f"Gold: {selected_quest['reward']['gold']} G", True, (10, 10, 10))
        self.screen.blit(money_text, (paper_x+50, paper_y))
        paper_y += 30
        
        items_text = reward_font.render(f"Items:", True, (10, 10, 10))
        self.screen.blit(items_text, (paper_x+50,  paper_y))

        for item in selected_quest["reward"]["items"]:
            item_text = reward_font.render(item, True, (10, 10, 10))
            self.screen.blit(item_text, (paper_x + 120, paper_y))
            paper_y += 30
        
        
        # Draw scrollbar if necessary
        total_items = len(complete_quests)
        inventory_x, inventory_y = base_x, base_y
        scrollbar_width = 10
        self.max_scroll = max(0, total_items - self.visible_quests)
        
        scrollbar_x = inventory_x + quest_list_width - 15  # Right edge for the scrollbar
        if total_items > self.visible_quests:
            # Scroll indicator height
            scroll_indicator_height = max(30, (self.visible_quests / total_items) * quest_list_height)

            # Scroll indicator position (proportional to scroll offset)
            scroll_indicator_y = inventory_y + (self.scroll_offset / self.max_scroll) * (quest_list_height - scroll_indicator_height)

            # Draw scroll indicator
            pygame.draw.rect(self.screen, (255, 255, 255), (scrollbar_x, scroll_indicator_y, scrollbar_width, scroll_indicator_height), border_radius=5)



    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within a specified width."""
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            test_width, _ = font.size(test_line)
            if test_width <= max_width:
                current_line = test_line
            else:

                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    def draw_rectangle(self, x, y, width, height, alpha, border_radius):
        rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(rect_surface, (10, 10, 10, alpha), (0, 0, width, height), border_radius=border_radius)
        self.screen.blit(rect_surface, (x, y))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.text_manager.messages:
                if event.key == pygame.K_RETURN:
                        if not self.text_manager.message_finished:
                            self.text_manager.skipping = True  # Skip typewriter effect
                        elif self.text_manager.waiting_for_next:
                            self.text_manager.next_message()
            else:
                # Available quests menu
                if self.selecting_quests:
                    if event.key == pygame.K_DOWN:
                        if self.selected_quest_index < len(self.call_available_quests()) - 1:
                            self.selected_quest_index += 1
                            if self.selected_quest_index >= self.scroll_offset + self.visible_quests:
                                self.scroll_offset += 1

                    elif event.key == pygame.K_UP:
                        if self.selected_quest_index > 0:
                            self.selected_quest_index -= 1
                            if self.selected_quest_index < self.scroll_offset:
                                self.scroll_offset -= 1
                    elif event.key == pygame.K_RETURN:
                        self.store_selected_quest()

                    elif event.key == pygame.K_ESCAPE:
                        self.selecting_quests = False
                        self.scroll_offset = 0
                
                # Active Quests menu
                elif self.viewing_active_quests:
                    if event.key == pygame.K_DOWN:
                        if self.selected_active_quest_index < len(self.player_party.current_quests) - 1:
                            self.selected_active_quest_index += 1
                            if self.selected_active_quest_index >= self.scroll_offset + self.visible_quests:
                                self.scroll_offset += 1

                    elif event.key == pygame.K_UP:
                        if self.selected_active_quest_index > 0:
                            self.selected_active_quest_index -= 1
                            if self.selected_active_quest_index < self.scroll_offset:
                                self.scroll_offset -= 1
                    elif event.key == pygame.K_RETURN:
                        pass

                    elif event.key == pygame.K_ESCAPE:
                        self.viewing_active_quests = False
                        self.scroll_offset = 0
                
                # Complete Quests menu
                elif self.viewing_complete_quests:
                    if event.key == pygame.K_DOWN:
                        if self.selected_complete_quest_index < len(self.call_complete_quests()) - 1:
                            self.selected_complete_quest_index += 1
                            if self.selected_complete_quest_index >= self.scroll_offset + self.visible_quests:
                                self.scroll_offset += 1

                    elif event.key == pygame.K_UP:
                        if self.selected_complete_quest_index > 0:
                            self.selected_complete_quest_index -= 1
                            if self.selected_complete_quest_index < self.scroll_offset:
                                self.scroll_offset -= 1
                    elif event.key == pygame.K_RETURN:
                        self.finish_quest()

                    elif event.key == pygame.K_ESCAPE:
                        self.viewing_complete_quests = False
                        self.scroll_offset = 0

                # First Select options
                else:
                    if event.key == pygame.K_DOWN:
                        self.selected_option_index = (self.selected_option_index + 1) % len(self.options)
                    elif event.key == pygame.K_UP:
                        self.selected_option_index = (self.selected_option_index - 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        self.selected_option()
    
    def finish_quest(self):
        selected_quest = self.call_complete_quests()[self.selected_complete_quest_index]
        id = selected_quest["id"]
        gold = selected_quest["reward"]["gold"]
        items = selected_quest["reward"]["items"]
        point = selected_quest["reward"]["guild_point"]

        #self.quest_complete_sound.play()
        self.channel1.play(self.quest_complete_sound)
        if items:
            result = ", ".join(items)
            self.text_manager.add_message(f"Congratulations on completing the quest! Here's your reward: {gold} G, {result} and {point} Guild point.")
        else:
            self.text_manager.add_message(f"Congratulations on completing the quest! Here's your reward: {gold} G and {point} Guild point.")

        # Reduce items from a leader inventry if it is collect quest
        if selected_quest["objective"]["type"] == "collect":
            target = selected_quest["objective"]["target"]
            count = selected_quest["objective"]["count"]
            self.player_party.leader.inventory[target] -= count
            if self.player_party.leader.inventory[target] <= 0:
                self.player_party.leader.inventory.pop(target)

        self.player_party.leader.gold += gold
        self.receive_guild_point(point)

        for quest in self.player_party.current_quests:
            if quest["id"] == id:
                self.player_party.current_quests.remove(quest)
        
        self.scroll_offset = 0
        self.selected_complete_quest_index = 0

        if not self.player_party.current_quests:
            self.viewing_complete_quests = False


    def selected_option(self):
        selected_option = self.options[self.selected_option_index]
        print(self.player_party.current_quests)
        if selected_option == "Available Quests":
            self.text_manager.add_message("Here are the available quests for your rank, Take your pick!")
            self.selecting_quests = True
        
        elif selected_option == "Active Quests":
            if self.player_party.current_quests:
                self.text_manager.add_message("Here are your active quests.")
                self.viewing_active_quests = True
            else:
                self.text_manager.add_message("You seem not to have any active quests.")
        
        elif selected_option == "Complete Quests":
            if self.call_complete_quests():
                self.text_manager.add_message("What quest have you completed?")
                self.viewing_complete_quests = True
            else:
                self.text_manager.add_message("Come back when you've completed any quests.")
    
    
    def call_available_quests(self):
        with open("JsonData/quests.json", "r") as file:
            quests_data = json.load(file)
            available_quests = quests_data[self.party_rank]
            return available_quests
    
    def call_complete_quests(self):
        complete_quests = []
        for quest in self.player_party.current_quests:
            if quest["objective"]["type"] == "kill":
                if quest["objective"]["count"] <= 0:
                    complete_quests.append(quest)
            elif quest["objective"]["type"] == "collect":
                target = quest["objective"]["target"]
                count = quest["objective"]["count"]
                if target in self.player_party.leader.inventory and self.player_party.leader.inventory[target] >= count:
                    complete_quests.append(quest)
        return complete_quests

    def store_selected_quest(self):
        selected_quest = self.call_available_quests()[self.selected_quest_index]

        id_list = []
        for quest in self.player_party.current_quests:
            id_list.append(quest["id"])
        if len(self.player_party.current_quests) > 3:
            self.text_manager.add_message("I'm sorry, but you already have too many active quests. Please complete some of your current tasks before taking on new ones.")
        else:
            if selected_quest["id"] in id_list:
                self.text_manager.add_message("You've already activated this quest.")
            else:
                self.player_party.current_quests.append(selected_quest)
                self.text_manager.add_message("Great choice! I'll mark this quest as active for you! Good luck!")

    def receive_guild_point(self, point):
        rank = ["C", "B", "A", "S"]
        index = rank.index(self.player_party.guild_rank)
        self.player_party.guild_point += point

        if self.player_party.guild_point >= self.rank_thresholds[self.player_party.guild_rank]:
            if self.player_party.guild_rank != "S":
                self.player_party.guild_point -= self.rank_thresholds[self.player_party.guild_rank]
                self.player_party.guild_rank = rank[index + 1]
                #self.level_up_sound.play()
                # Wait for the first sound to finish
                while self.channel1.get_busy():
                    time.sleep(0.1)  # Sleep for a short time to avoid busy-waiting
                self.channel1.play(self.level_up_sound)
                self.text_manager.add_message(f"Congratulations! You've been promoted to {self.player_party.guild_rank}! Your hard work has paid off!")
                

