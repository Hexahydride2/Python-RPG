import pygame
from text_manager import TextManager

class Shop:
    def __init__(self, screen, player, items_for_sale, background_image_path=".\Backgrounds\shop.png"):
        self.screen = screen
        self.player = player
        self.items_for_sale = items_for_sale
        self.selected_index = 0
        self.scroll_offset = 0
        self.font = pygame.font.Font(None, 25)
        self.visible_items = 7
        self.item_list_width, self.item_list_height = 300, 300
        self.desc_list_width, self.desc_list_height = 300, 300
        self.text_manager = TextManager(screen)

        # Load background image if provided       
        self.background = pygame.image.load(background_image_path)
        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))  # Resize to match the screen size

        # Load purchase sound effect
        self.purchase_sound = pygame.mixer.Sound(".\Sound_Effects\coins.wav")
        self.purchase_sound.set_volume(0.7)  # Adjust the volume
        
    
    def wrap_text(self, text, max_width):
        """Wraps text into multiple lines if it exceeds max width."""
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] > max_width - 20:
                lines.append(current_line)
                current_line = word + " "
            else:
                current_line = test_line
        
        lines.append(current_line)
        return lines
    
    def draw_rectangle(self, x, y, width, height, alpha, border_radius):
        rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(rect_surface, (10, 10, 10, alpha), (0, 0, width, height), border_radius=border_radius)
        self.screen.blit(rect_surface, (x, y))

    def draw(self):
        """Draw the shop interface with three sections."""
        # Draw background if available
        self.screen.fill((0, 0, 0))
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((0, 0, 0))  # Clear screen with black
        
        # Draw item list section (Left side)
        self.draw_rectangle(50,100, self.item_list_width, self.item_list_height, alpha=200, border_radius=10)
        items = list(self.items_for_sale.items())
    
        for i in range(self.scroll_offset, min(self.scroll_offset + self.visible_items, len(items))):
            item = items[i][0]
            price = items[i][1]["price"]
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            text = self.font.render(f'{item}: {price} G', True, color)
            self.screen.blit(text, (60, 120 + (i - self.scroll_offset) * 40))
        
        # Draw item description section (Right side)
        self.draw_rectangle(400 ,100, self.desc_list_width, self.desc_list_height, alpha=200, border_radius=10)
        selected_item = list(self.items_for_sale.items())[self.selected_index]
        wrapped_description = self.wrap_text(selected_item[1]["description"], self.desc_list_width)

        for i, line in enumerate(wrapped_description):
            description_text = self.font.render(line, True, (255,255,255))
            self.screen.blit(description_text, (420, 120 + i*30))

        # Draw Item possession section (Bottom)
        self.draw_rectangle(200, 430, 150, 50, alpha=200, border_radius=10)
        if selected_item[0] in self.player.inventory:
            possesion = self.player.inventory[selected_item[0]]
        else:
            possesion=0
        possession_text = self.font.render(f"Possession {possesion}", True, (255, 255, 255))
        self.screen.blit(possession_text, (220, 440))
        
        # Draw gold possession section (Bottom)
        self.draw_rectangle(50, 430, 120, 50, alpha=200, border_radius=10)
        gold_text = self.font.render(f"{self.player.gold} G", True, (255, 255, 255))
        self.screen.blit(gold_text, (90, 440))
        
        # Load gold image
        gold_image = pygame.image.load(".\Icons\gold.png")
        gold_image = pygame.transform.scale(gold_image, (40, 40))  # Resize the image to fit next to the text

        # Display the gold image
        self.screen.blit(gold_image, (50, 430))


        # Instructions
        instructions = [
            "Use UP/DOWN to scroll", 
            "Press E to buy", 
            "Press ESC to exit"
        ]
        instruction_font = pygame.font.Font(None, 22)
        for i, instruction in enumerate(instructions):
            inst_text = instruction_font.render(instruction, True, (255, 255, 255))
            self.screen.blit(inst_text, (500, 420 + i * 25))

        # Draw scrollbar if necessary
        total_items = len(items)
        inventory_x, inventory_y = 50, 100
        inventory_height = self.item_list_height
        inventory_width = self.item_list_width
        scrollbar_width = 10
        self.max_scroll = max(0, total_items - self.visible_items)
        
        scrollbar_x = inventory_x + inventory_width - 15  # Right edge for the scrollbar
        if total_items > self.visible_items:
            # Scroll indicator height
            scroll_indicator_height = max(30, (self.visible_items / total_items) * inventory_height)

            # Scroll indicator position (proportional to scroll offset)
            scroll_indicator_y = inventory_y + (self.scroll_offset / self.max_scroll) * (inventory_height - scroll_indicator_height)

            # Draw scroll indicator
            pygame.draw.rect(self.screen, (255, 255, 255), (scrollbar_x, scroll_indicator_y, scrollbar_width, scroll_indicator_height), border_radius=5)
        if self.text_manager.messages != []:
            self.text_manager.update()
            self.text_manager.draw()
        
        pygame.display.flip()
    
    def handle_event(self, event):
        """Handle user input."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if self.selected_index < len(self.items_for_sale) - 1:
                    self.selected_index += 1
                    if self.selected_index >= self.scroll_offset + self.visible_items:
                        self.scroll_offset += 1
            elif event.key == pygame.K_UP:
                if self.selected_index > 0:
                    self.selected_index -= 1
                    if self.selected_index < self.scroll_offset:
                        self.scroll_offset -= 1
            elif event.key == pygame.K_e:
                self.buy_item()

            elif event.key == pygame.K_RETURN:
                if not self.text_manager.message_finished:
                    self.text_manager.skipping = True  # Skip typewriter effect
                elif self.text_manager.waiting_for_next:
                    self.text_manager.next_message()


    def buy_item(self):
        """Handle item purchase."""
        item_name = list(self.items_for_sale.keys())[self.selected_index]
        item_price = self.items_for_sale[item_name]["price"]

        if self.player.gold >= item_price:
            self.player.gold -= item_price
            self.player.add_item(item_name)
            # Play the purchase sound effect
            self.purchase_sound.play()
            self.text_manager.add_message("Thank you for your purchase! May your journey be prosperous!")
       
        else:
            self.text_manager.add_message("I'm sorry, you don't have enough gold, Come back when you're ready!")
          
    

############
## Create NPCs.
# npc = NPC("Shopkeeper", ["Welcome to my shop!  I sell potions and weapons."], 1024, 1700,
#            [R".\timefantasy_characters\timefantasy_characters\frames\npc\npc1_2"], items_list())
# npcs = [npc]

# shop_active = False # Track shop state
# current_npc = None

###### In main loop ######

#shop_active, current_npc = handle_npc_interaction(player, npcs, text_manager, screen, shop_active, current_npc)