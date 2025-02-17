import pygame

def initialize_screen(cell_width, cell_height, title="Dragon Quest-like RPG"):

    screen = pygame.display.set_mode((cell_width, cell_height))
    pygame.display.set_caption(title)
    return screen

def initialize_dungeon(cell_width, cell_height, map_rows, map_cols, map_left_path, map_right_path):
  
    COMBINED_COLS = map_cols * 2  # two maps side-by-side
    combined_map_width = COMBINED_COLS * cell_width
    combined_map_height = map_rows * cell_height

    # Load and scale the map files.
    map_surface_L = pygame.image.load(map_left_path)
    map_surface_R = pygame.image.load(map_right_path)
    scaled_map_size = (map_cols * cell_width, map_rows * cell_height)
    map_surface_L = pygame.transform.scale(map_surface_L, scaled_map_size)
    map_surface_R = pygame.transform.scale(map_surface_R, scaled_map_size)

    # Combine the two maps side-by-side into one surface.
    combined_map_surface = pygame.Surface((combined_map_width, combined_map_height))
    combined_map_surface.blit(map_surface_L, (0, 0))
    combined_map_surface.blit(map_surface_R, (map_cols * cell_width, 0))
    
    # Start at the center of the bottom left cell of Map-L.
    player_x = cell_width // 2
    player_y = (map_rows - 1) * cell_height + cell_height // 2

    return combined_map_surface, combined_map_width, combined_map_height, player_x, player_y

def initialize_town(cell_width, cell_height, town_map_path):

    screen = pygame.display.set_mode((cell_width, cell_height))
    pygame.display.set_caption("Town Area")

    # Load the town map.
    town_map_surface = pygame.image.load(town_map_path).convert_alpha()

    # Zoom factor: increase the size of the town map to "zoom in"
    zoom_factor = 2  # Adjust for desired zoom
    original_width, original_height = town_map_surface.get_size()
    zoomed_width = int(original_width * zoom_factor)
    zoomed_height = int(original_height * zoom_factor)
    zoomed_map = pygame.transform.scale(town_map_surface, (zoomed_width, zoomed_height))
    
    # Set the player's starting position (e.g., near the center of the zoomed map)
    player_x = zoomed_width // 2
    player_y = zoomed_height - cell_height // 2

    return screen, zoomed_map, zoomed_width, zoomed_height, player_x, player_y

def update_camera_and_draw(player, player_x, player_y, screen, combined_map_surface,
                           combined_map_width, combined_map_height, cell_width, cell_height):
    # Calculate camera position to center the player:
    camera_x = player_x - cell_width // 2
    camera_y = player_y - cell_height // 2

    # Clamp the camera to the bounds of the combined map:
    camera_x = max(0, min(camera_x, combined_map_width - cell_width))
    camera_y = max(0, min(camera_y, combined_map_height - cell_height))
    camera_rect = pygame.Rect(camera_x, camera_y, cell_width, cell_height)

    # Draw the visible portion of the combined map.
    screen.blit(combined_map_surface, (0, 0), camera_rect)

    # Draw the player with the correct offset relative to the camera.
    player_draw_x = player_x - camera_rect.x - (player.sprite.sprite_width * player.sprite.scale_factor) // 2
    player_draw_y = player_y - camera_rect.y - (player.sprite.sprite_height * player.sprite.scale_factor) // 2
    player.sprite.update_frame()
    player.sprite.draw(screen, player_draw_x, player_draw_y)

    return camera_rect


def initialize_main_menu():
    import sys
    # Create the screen using your initialize_screen function
    screen = initialize_screen(800, 600, "Main Menu")
    clock = pygame.time.Clock()  # Create a local clock
    
    menu_running = True
    # Create a simple font
    font = pygame.font.SysFont("Arial", 40)
    # Define button dimensions
    button_rect = pygame.Rect(300, 250, 200, 80)  # Adjust position/size as needed

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Check for mouse click within button area.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    menu_running = False  # Exit the menu

        # Draw main menu
        screen.fill((50, 50, 50))  # Gray background
        # Draw start button
        pygame.draw.rect(screen, (0, 200, 0), button_rect)  # Green button
        # Render text
        text_surface = font.render("Start Game", True, (255, 255, 255))
        # Center text on button
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        clock.tick(30)
    
    return screen

