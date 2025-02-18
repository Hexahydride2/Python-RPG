import pygame
from items import items_list

class Menu:
    def __init__(self, screen, player):
        self.screen = screen
        self.active = False  # Whether the menu is currently open
        self.options = ["Status", "Items", "Quests", "Exit"]
        self.selected_index = 0 # Track which option is selected
        self.font = pygame.font.Font(None, 27)
        self.player = player

        self.menu_width, self.menu_height = 300, 200
        self.menu_x, self.menu_y = (self.screen.get_width() - self.menu_width) // 2, (self.screen.get_height() - self.menu_height) // 2

        self.showing_status = False
        self.showing_inventory = False

        self.scroll_offset = 0  # Track the scroll position in the inventory
        self.visible_items = 7
        self.item_selected_index = 0 # Track which item is selected

         # Load ESC icon (Replace 'esc_icon.png' with your actual image file)
        self.esc_icon = pygame.image.load(".\Icons\icons8-esc-key-50.png")  
        self.esc_icon = pygame.transform.scale(self.esc_icon, (40, 40))  # Resize for visibility
    
    def draw(self):
        """Draw the menu when it's active"""
        if not self.active:
            return
        self.player.can_move = False # Deny the player moving when menu is open

        if self.showing_status:
            self.draw_status_screen()
        elif self.showing_inventory:
            self.draw_inventory_screen()
        else:
            self.draw_pause_menu()
    
    def draw_pause_menu(self):
        """draw_pause_menu"""
        # Draw Title
        title_font = pygame.font.Font(None, 40)
        self.draw_rectangle(300, 20, 150, 50, alpha=200, border_radius=10, c1=10, c2=10, c3=10)
        pygame.draw.rect(self.screen, (255, 255, 255), (300, 20, 150, 50), width=3, border_radius=10) # Border
        text = title_font.render("Menu", True, (255, 255, 255))
        self.screen.blit(text, (330, 30))

        menu_width, menu_height = 300, 200
        menu_x, menu_y = (self.screen.get_width() - menu_width) // 2, (self.screen.get_height() - menu_height) // 2
        
        self.draw_rectangle(menu_x, menu_y, menu_width, menu_height, alpha=200, border_radius=10, c1=10, c2=10, c3=10)
        pygame.draw.rect(self.screen, (255, 255, 255), (menu_x, menu_y, menu_width, menu_height), width=3, border_radius=10) # Border

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_index else (150, 150, 150)
            text_surface = self.font.render(option, True, color)
            self.screen.blit(text_surface, (menu_x + 20, menu_y + 30 + i * 40))


    def draw_rectangle(self, x, y, width, height, alpha, border_radius, c1, c2, c3):
        rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(rect_surface, (c1, c2, c3, alpha), (0, 0, width, height), border_radius=border_radius)
        self.screen.blit(rect_surface, (x, y))

    def handle_input(self, event):
        """Handle user input for menu navigation"""
        if not self.active:
            return
        
        if event.type == pygame.KEYDOWN:
            if self.showing_status or self.showing_inventory:
                if event.key == pygame.K_ESCAPE:  # Close status/inventory screen
                    self.showing_status = False
                    self.showing_inventory = False
                    self.selected_index = 0 # Reset to default when going back to pause menu window
                    self.scroll_offset = 0 # Reset to default when going back to pause menu window
            else:
                if event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_RETURN: # Select option
                    self.select_option()
            
            # Handle scrolling in the inventory screen
            if self.showing_inventory:
                if event.key == pygame.K_DOWN:
                    if self.selected_index < len(self.player.inventory) - 1:
                        self.selected_index += 1
                        if self.selected_index >= self.scroll_offset + self.visible_items:
                            self.scroll_offset += 1
                elif event.key == pygame.K_UP:
                    if self.selected_index > 0:
                        self.selected_index -= 1
                        if self.selected_index < self.scroll_offset:
                            self.scroll_offset -= 1
    
    def select_option(self):
        """Execute the selected menu option."""
        selected_option = self.options[self.selected_index]
        if selected_option == "Exit":
            self.player.can_move = True # Allow the player to move when menu is not open
            self.active = False # Close menu
        elif selected_option == "Status":
            self.showing_status = True
        elif selected_option == "Items":
            self.showing_inventory = True
            self.selected_index = 0
        elif selected_option == "Quests":
            print("Showing quests")
    
    def toggle(self):
        """Open or close the menu"""
        self.active = not self.active

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

    def draw_status_screen(self):
        """Display character stats."""
        # Draw Title
        title_font = pygame.font.Font(None, 40)
        self.draw_rectangle(300, 20, 150, 50, alpha=200, border_radius=10, c1=10, c2=10, c3=10)
        pygame.draw.rect(self.screen, (255, 255, 255), (300, 20, 150, 50), width=3, border_radius=10) # Border
        text = title_font.render("Status", True, (255, 255, 255))
        self.screen.blit(text, (330, 30))


        stats = [
            f"Name: {self.player.name}",
            f"Level: {self.player.level}",
            f"HP: {self.player.hp}/{self.player.max_hp}",
            f"MP: {self.player.mp}/{self.player.max_mp}",
            f"ATK: {self.player.atk}",
            f"DEF: {self.player.dfn}",
            f"SPD: {self.player.spd}",
            f"Gold: {self.player.gold} G"
        ]

        self.draw_rectangle(self.menu_x, self.menu_y - 120, self.menu_width, self.menu_height + 160, alpha=200, border_radius=10, c1=10, c2=10, c3=10)
        pygame.draw.rect(self.screen, (255, 255, 255), (self.menu_x, self.menu_y - 120, self.menu_width, self.menu_height + 160), width=3, border_radius=10) # Border

        for i, stat in enumerate(stats):
            text_surface = self.font.render(stat, True, (255, 255, 255))
            self.screen.blit(text_surface, (300, 100+i * 40))

        esc_icon_x, esc_icon_y = self.menu_x + (self.menu_y - 120) - 50, self.menu_y -120 + self.menu_height + 160 + 20  # Bottom-right

         # Draw ESC icon (Go Back)
        self.draw_rectangle(esc_icon_x, esc_icon_y, self.esc_icon.get_width(), self.esc_icon.get_height(), alpha=225, border_radius=10, c1=255, c2=255, c3=255)
        self.screen.blit(self.esc_icon, (esc_icon_x, esc_icon_y))  
        # Display text "Back" under the ESC icon
        esc_text = self.font.render("Back", True, (255, 255, 255))
        self.screen.blit(esc_text, (esc_icon_x + 10, esc_icon_y + 45))

    def draw_inventory_screen(self):
        """Display inventory items and their descriptions."""

        # Draw Title
        title_font = pygame.font.Font(None, 40)
        self.draw_rectangle(300, 20, 150, 50, alpha=200, border_radius=10, c1=10, c2=10, c3=10)
        pygame.draw.rect(self.screen, (255, 255, 255), (300, 20, 150, 50), width=3, border_radius=10) # Border
        text = title_font.render("Items", True, (255, 255, 255))
        self.screen.blit(text, (330, 30))


        All_Item_List = items_list()

        # Constants
        inventory_x, inventory_y = 50, 100
        inventory_width, inventory_height = 300, 300  # The height of the inventory window
        scrollbar_x = inventory_x + inventory_width - 15  # Right edge for the scrollbar
        scrollbar_width = 10
        scrollbar_padding = 10  # Padding for spacing
        item_height = 40  # Height of each item entry
        esc_icon_x, esc_icon_y = inventory_x + inventory_width - 50, inventory_y + inventory_height + 20  # Bottom-right

         # Draw ESC icon (Go Back)
        self.draw_rectangle(esc_icon_x, esc_icon_y, self.esc_icon.get_width(), self.esc_icon.get_height(), alpha=225, border_radius=10, c1=255, c2=255, c3=255)
        self.screen.blit(self.esc_icon, (esc_icon_x, esc_icon_y))  
        # Display text "Back" under the ESC icon
        esc_text = self.font.render("Back", True, (255, 255, 255))
        self.screen.blit(esc_text, (esc_icon_x + 10, esc_icon_y + 45))


        # Draw inventory box
        self.draw_rectangle(inventory_x, inventory_y, inventory_width, inventory_height, alpha=200, border_radius=10, c1=10, c2=10, c3=10)
        pygame.draw.rect(self.screen, (255, 255, 255), (inventory_x, inventory_y, inventory_width, inventory_height), width=3, border_radius=10)  # Border

        # Draw item list section (Reight side)
        self.draw_rectangle(400, inventory_y, inventory_width, inventory_height, alpha=200, border_radius=10, c1=10, c2=10, c3=10)
        pygame.draw.rect(self.screen, (255, 255, 255), (400, 100, 300, 300), width=3, border_radius=10) # Border

        # Draw Item possession section (Bottom)
        self.draw_rectangle(400, 410, 150, 50, alpha=200, border_radius=10, c1=10, c2=10, c3=10)
        pygame.draw.rect(self.screen, (255, 255, 255), (400, 410, 150, 50), width=3, border_radius=10) # Border

        # Get inventory items
        items = list(self.player.inventory.keys())
        total_items = len(items)

        # Maximum number of visible items
        self.visible_items = inventory_height // item_height

        # Calculate max scroll
        self.max_scroll = max(0, total_items - self.visible_items)

        # Draw inventory items (only visible ones)
        for i in range(self.scroll_offset, min(self.scroll_offset + self.visible_items, total_items)):
            item = items[i]
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            text = self.font.render(f"{item} x{self.player.inventory[item]}", True, color)
            self.screen.blit(text, (inventory_x + 10, inventory_y + 10 + (i - self.scroll_offset) * item_height))
    
        selected_item = list(self.player.inventory.items())[self.selected_index]
        # Draw Item possession section (Bottom))
        if selected_item[0] in self.player.inventory:
            possesion = self.player.inventory[selected_item[0]]
        else:
            possesion=0
        possession_text = self.font.render(f"Possession {possesion}", True, (255, 255, 255))
        self.screen.blit(possession_text, (410, 430))

        # Draw description of selected Item
        wrapped_description = self.wrap_text(All_Item_List[selected_item[0]]["description"], inventory_width)
        for i, line in enumerate(wrapped_description):
            description_text = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(description_text, (420, 120 + i*30))

        # Draw scrollbar if necessary
        if total_items > self.visible_items:
            # Scroll indicator height
            scroll_indicator_height = max(30, (self.visible_items / total_items) * inventory_height)

            # Scroll indicator position (proportional to scroll offset)
            scroll_indicator_y = inventory_y + (self.scroll_offset / self.max_scroll) * (inventory_height - scroll_indicator_height)

            # Draw scroll indicator
            pygame.draw.rect(self.screen, (255, 255, 255), (scrollbar_x, scroll_indicator_y, scrollbar_width, scroll_indicator_height), border_radius=5)



####### How to Use #######
# menu = Menu(screen, player)

### In main loop 
# events = pygame.event.get()
# menu_active = add_menu(menu, events)
