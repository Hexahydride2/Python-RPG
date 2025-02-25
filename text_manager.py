import pygame

class TextManager:
    def __init__(self, screen, font_size=25, font_file=".\Fonts\RotisSerif.ttf", sound_file=R".\Sound_Effects\Retro_03\Retro_Single_v5_wav.wav"):
        self.screen = screen
        self.font = pygame.font.Font(font_file, font_size)
        self.messages = []  # List of messages to display
        self.current_message = ""  # Text being displayed
        self.typing_index = 0  # For typewriter effect
        self.typing_speed = 0.5  # Number of frames per character

        # Text box size
        self.box_width = self.screen.get_width() * 0.9
        self.box_height = self.screen.get_height() * 0.15

        # Text control
        self.message_finished = False
        self.waiting_for_next = False
        self.skipping = False

        # Blinking Symbol Timer
        self.blink_timer = 0

        # Load the text blip sound
        pygame.mixer.init()
        self.text_sound = pygame.mixer.Sound(sound_file)
        self.text_sound.set_volume(0.5)  # Adjust volume if needed

    def add_message(self, message, speaker=None):
        """Add a new message to display."""
        message_sentences = message.split('. ')
        for message in message_sentences:
            # Handle the multiple period problem
            if message == message_sentences[-1]:
                wrapped_lines = self.wrap_text(message)
            else:
                wrapped_lines = self.wrap_text(message+".")
            self.messages.append((wrapped_lines, speaker))
            self.current_message = []
            self.typing_index = 0  # Reset typing effect
            self.message_finished = False
            self.waiting_for_next = False

    def wrap_text(self, text):
        """Wraps text intp multiple lines based on box width."""
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            test_width, _ = self.font.size(test_line)

            if test_width > self.box_width - 20:
                lines.append(current_line)
                current_line = word + " "
            else:
                current_line = test_line
        
        lines.append(current_line)
        return lines
    
    def next_message(self):
        """Advance to the next message, if available."""
        if len(self.messages) > 1:
            self.messages.pop(0)
            self.current_message = []
            self.typing_index = 0
            self.message_finished = False
            self.waiting_for_next = False
        else:
            self.messages = []
            self.current_message = []
            self.typing_index = 0
            self.message_finished = False
            self.waiting_for_next = False

    def update(self):
        """Update text display (handles typewriter effect)."""
        if self.messages: 
            if not self.message_finished:
                # Simulate a typewriter effect

                # If skipping is activated, show full text immediately
                if self.skipping:
                    self.typing_index = len(" ".join(self.messages[0][0]) )
                    self.current_message = self.messages[0][0]  # Display full wrapped lines
                    self.message_finished = True
                    self.waiting_for_next = True
                    self.skipping = False  # Reset skipping

                elif self.typing_index < len(" ".join(self.messages[0][0])):
                    if pygame.time.get_ticks() % self.typing_speed == 0:
                        self.typing_index += 1
                        total_text = " ".join(self.messages[0][0])
                        self.current_message = self.wrap_text(total_text[:self.typing_index])

                        #Play sound effect every few letters (to avoid overlap)
                        if self.typing_index % 4 == 0:  # Play every 2 characters
                            self.text_sound.play()
                else:
                    self.message_finished = True
                    self.waiting_for_next = True

            # Blinking symbol effect
            self.blink_timer += 1
            if self.blink_timer > 15:  # Change every 30 frames
                self.blink_timer = 0

    def draw(self):
        """Draw the current message on screen."""
        x, y = self.screen.get_width() * 0.05, self.screen.get_height() * 0.85
        if self.messages:
            message_text, speaker = self.messages[0]

            """Draws a semi-transparent text box."""
            rect_surface = pygame.Surface((self.box_width, self.box_height), pygame.SRCALPHA)
            pygame.draw.rect(rect_surface, (10, 10, 10, 200), (0, 0, self.box_width, self.box_height), border_radius=10)
            self.screen.blit(rect_surface, (x - 10, y - 10))

            pygame.draw.rect(self.screen, (255, 255, 255), (x - 10, y - 10, self.box_width, self.box_height), width=2, border_radius=10) # Border

            # Draw speaker name if exists
            if speaker:
                # Speaker box
                # Draw a transparent rectangle
                rect_surface = pygame.Surface((self.box_width, self.box_height), pygame.SRCALPHA)
                pygame.draw.rect(rect_surface, (10, 10, 10, 200), (0, 0, self.box_width // 4, self.box_height // 3), border_radius=10)
                self.screen.blit(rect_surface, (x - 10, y - 50))

                pygame.draw.rect(self.screen, (255, 255, 255), (x - 10, y - 50, self.box_width // 4, self.box_height //3), width=2, border_radius=10)

                name_surface = self.font.render(speaker, True, (255, 255, 100))  # Yellow color
                self.screen.blit(name_surface, (x + 10, y - 50))  # Place above the text box

            for i, line in enumerate(self.current_message):
                text_surface = self.font.render(line, True, (255, 255, 255))
                self.screen.blit(text_surface, (x, y + i * 30))
            
            # Show blinking symbol instead of "Press Enter"
            if self.waiting_for_next:
                if self.blink_timer < 7:  # Blink on and off every 30 frames
                    pygame.draw.polygon(self.screen, (255, 255, 255), ((x+self.box_width-30, y+self.box_height-30),(x+self.box_width-30, y+self.box_height-20),(x+self.box_width-20, y+self.box_height-25)))


# pygame.init()
# # Screen settings
# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Character Animation")

# clock = pygame.time.Clock()

# running = True

# ###########################################################################################
# text_manager = TextManager(screen)
# text_manager.add_message("Hello, traveler! This is a very long sentence that will automatically wrap into multiple lines. Yes may be this is too long but it is worth testing. I dont know what is going to happen if I put too long sentence. hello still too short I just want to see if the size of the text box will change or not", speaker="Dragon")
# ###################################################################################################

# while running:
#     screen.fill((255, 255, 255))  # Clear screen

#     # Event handling
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

# ###############################################################################
#         # Go to the next message when Enter is pressed
#         if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
#             if not text_manager.message_finished:
#                 text_manager.skipping = True  # Skip typewriter effect
#             elif text_manager.waiting_for_next:
#                 text_manager.next_message()

#     text_manager.update()
#     text_manager.draw()
# ##################################################################################


#     pygame.display.update()
#     clock.tick(30)  # Control animation speed (10 FPS)

# pygame.quit()