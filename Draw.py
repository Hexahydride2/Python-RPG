import pygame

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


def initialize_screen_and_map(cell_width, cell_height, map_rows, map_cols, map_left_path, map_right_path):
    
    #Initializes the pygame screen, loads and scales two maps, combines them,
    #and sets the starting player position.
    
    COMBINED_COLS = map_cols * 2  # two maps side-by-side
    combined_map_width = COMBINED_COLS * cell_width
    combined_map_height = map_rows * cell_height
    screen = pygame.display.set_mode((cell_width, cell_height))
    pygame.display.set_caption("Dragon Quest-like RPG")
    
    # Load and scale the map files directly.
    map_surface_L = pygame.image.load("Map-L.png")
    map_surface_R = pygame.image.load("Map-R.png")
    scaled_map_size = (map_cols * cell_width, map_rows * cell_height)
    map_surface_L = pygame.transform.scale(map_surface_L, scaled_map_size)
    map_surface_R = pygame.transform.scale(map_surface_R, scaled_map_size)
    
    # Combine the two maps side-by-side into one surface.
    combined_map_surface = pygame.Surface((combined_map_width, combined_map_height))
    combined_map_surface.blit(map_surface_L, (0, 0))
    combined_map_surface.blit(map_surface_R, (map_cols * cell_width, 0))
    
    # Start at the center of the bottom left cell of Map-L
    player_x = cell_width // 2
    player_y = (map_rows - 1) * cell_height + cell_height // 2

    #Returns:
        #screen: the pygame display surface,
        #combined_map_surface: the surface with both maps combined,
        #combined_map_width: width of the combined map,
        #combined_map_height: height of the combined map,
        #player_x: starting x position,
        #player_y: starting y position
    
    return screen, combined_map_surface, combined_map_width, combined_map_height, player_x, player_y

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
    
    # Do not crop – allow the map to be larger than the screen so the camera can pan.
    # Set the player's starting position (e.g., near the center of the zoomed map)
    player_x = zoomed_width // 2
    player_y = zoomed_height - cell_height // 2

    return screen, zoomed_map, zoomed_width, zoomed_height, player_x, player_y
