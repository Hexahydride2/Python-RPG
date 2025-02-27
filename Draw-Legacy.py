# import pygame
# import sys


# def initialize_screen(cell_width, cell_height, title="Dragon Quest-like RPG"):

#     screen = pygame.display.set_mode((cell_width, cell_height))
#     pygame.display.set_caption(title)

#     return screen

# def initialize_dungeon(cell_width, cell_height, map_rows, map_cols, map_left_path, map_right_path):
#     pygame.mixer.init()
#     change_theme("Music\\DungeonTheme.mp3")
#     screen = pygame.display.set_mode((cell_width, cell_height))
#     pygame.display.set_caption("Dungeon Area")
    
#     # Load the left and right maps.
#     map_surface_L = pygame.image.load(map_left_path)
#     map_surface_R = pygame.image.load(map_right_path)
    
#     # Scale maps.
#     scaled_map_size = (map_cols * cell_width, map_rows * cell_height)
#     map_surface_L = pygame.transform.scale(map_surface_L, scaled_map_size)
#     map_surface_R = pygame.transform.scale(map_surface_R, scaled_map_size)
    
#     # Combine maps side-by-side.
#     combined_map_width = map_cols * cell_width * 2
#     combined_map_height = map_rows * cell_height
#     combined_map_surface = pygame.Surface((combined_map_width, combined_map_height))
#     combined_map_surface.blit(map_surface_L, (0, 0))
#     combined_map_surface.blit(map_surface_R, (map_cols * cell_width, 0))
    
#     # Set player's starting position.
#     player_x = cell_width // 2
#     player_y = (map_rows - 1) * cell_height + cell_height // 2

#     return screen, combined_map_surface, combined_map_width, combined_map_height, player_x, player_y

# def initialize_town(cell_width, cell_height, town_map_path):

#     pygame.mixer.init()
#     #change_theme("Music\TownTheme.mp3")
    

#     screen = pygame.display.set_mode((cell_width, cell_height))
#     pygame.display.set_caption("Town Area")

#     # Load the town map.
#     town_map_surface = pygame.image.load(town_map_path).convert_alpha()

    
#     zoom_factor = 2  # Adjust for desired zoom
#     original_width, original_height = town_map_surface.get_size()
#     zoomed_width = int(original_width * zoom_factor)
#     zoomed_height = int(original_height * zoom_factor)
#     zoomed_map = pygame.transform.scale(town_map_surface, (zoomed_width, zoomed_height))
    
#     # Set the player's starting position (e.g., near the center of the zoomed map)
#     player_x = zoomed_width // 2
#     player_y = zoomed_height - cell_height // 2

#     return screen, zoomed_map, zoomed_width, zoomed_height, player_x, player_y

# def update_camera_and_draw(player, player_x, player_y, screen, combined_map_surface,
#                            combined_map_width, combined_map_height, cell_width, cell_height):
#     # Calculate camera position to center the player:
#     camera_x = player.x - cell_width // 2
#     camera_y = player.y - cell_height // 2

#     # Clamp the camera to the bounds of the combined map:
#     camera_x = max(0, min(camera_x, combined_map_width - cell_width))
#     camera_y = max(0, min(camera_y, combined_map_height - cell_height))
#     camera_rect = pygame.Rect(camera_x, camera_y, cell_width, cell_height)

#     # Draw the visible portion of the combined map.
#     screen.blit(combined_map_surface, (0, 0), camera_rect)

#     # Draw the player with the correct offset relative to the camera.
#     # player_draw_x = player.x - camera_rect.x - (player.sprite.sprite_shape[player.sprite.current_animation]["width"] * player.sprite.scale_factor) // 2
#     # player_draw_y = player.y - camera_rect.y - (player.sprite.sprite_shape[player.sprite.current_animation]["height"] * player.sprite.scale_factor) // 2
#     # player.sprite.update_frame()
#     # player.sprite.draw(screen, player_draw_x, player_draw_y)

#     return camera_rect


# def initialize_main_menu():
    
#     pygame.mixer.init()
#     change_theme("Music\MainMenuTheme.mp3")

    
#     screen = initialize_screen(1600, 800, "Main Menu")
    
#     # Load and scale the background image.
#     background = pygame.image.load("Backgrounds\MainMenu.png").convert() 
#     background = pygame.transform.scale(background, (1600, 800))
    
#     clock = pygame.time.Clock()  # Create a local clock
#     menu_running = True
    
    
#     font = pygame.font.SysFont("Arial", 40)
#     # Define button dimensions 
#     button_rect = pygame.Rect(700, 550, 200, 80)
    
#     while menu_running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             # Check for mouse click within button area.
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 mouse_pos = pygame.mouse.get_pos()
#                 if button_rect.collidepoint(mouse_pos):
#                     menu_running = False  # Exit the menu

#         # Draw main menu background image
#         screen.blit(background, (0, 0))
#         # Draw start button
#         pygame.draw.rect(screen, (0, 200, 0), button_rect)
#         # Render text
#         text_surface = font.render("Start Game", True, (255, 255, 255))
#         # Center text on button
#         text_rect = text_surface.get_rect(center=button_rect.center)
#         screen.blit(text_surface, text_rect)
#         pygame.display.update()
#         clock.tick(30)
    
#     return screen

# class MusicManager:
#     def __init__(self):
#         self.current_theme = None
#         self.previous_theme = None

#     def change_theme(self, theme_file):
#         self.previous_theme = self.current_theme
#         self.current_theme = theme_file
#         pygame.mixer.music.stop()
#         pygame.mixer.music.load(theme_file)
#         pygame.mixer.music.set_volume(0.2)
#         pygame.mixer.music.play(-1)

#     def revert_theme(self):
#         if self.previous_theme:
#             self.change_theme(self.previous_theme)

# music_manager = MusicManager()

# def change_theme(theme_file):
#     music_manager.change_theme(theme_file)

# def revert_theme():
#     music_manager.revert_theme()

# # def check_map_transition(player, combined_map_surface, combined_map_width, combined_map_height, cell_width, cell_height, prev_pos):

# #     # Define the target colors. Adjust these as necessary.
# #     obstacle_color = (0, 0, 0)
# #     town_color = (0, 65, 120)
# #     dungeon_color = (0, 9, 36)

# #     check_x = int(player.x)
# #     check_y = int(player.y)
    
#     # # Ensure we are within bounds.
#     # if 0 <= check_x < combined_map_width and 0 <= check_y < combined_map_height:
#     #     current_color = combined_map_surface.get_at((check_x, check_y))[:3]
        
#     #     if current_color == obstacle_color:
#     #         # Revert player's position.
#     #         player.x, player.y = prev_pos
#     #         return None
#     #     elif current_color == town_color:
#     #         # Transition into the town area.
#     #         return initialize_town(cell_width, cell_height, "Backgrounds/TownMap.png")
#     #     elif current_color == dungeon_color:
#     #         # Transition into the dungeon area.
#     #         return initialize_dungeon(cell_width, cell_height, 5, 6, "Backgrounds/Map-L.png", "Backgrounds/Map-R.png")
#     # return None