import pygame
import sys
import glob
import re

pygame.init()


# Each cell is 800x600.
CELL_WIDTH, CELL_HEIGHT = 800, 600 
MAP_ROWS, MAP_COLS = 5, 6           # each map is 5 rows x 6 cols
COMBINED_COLS = MAP_COLS * 2        # two maps side-by-side
combined_map_width = COMBINED_COLS * CELL_WIDTH
combined_map_height = MAP_ROWS * CELL_HEIGHT

# Set window size to one cell.
screen = pygame.display.set_mode((CELL_WIDTH, CELL_HEIGHT))
pygame.display.set_caption("Combined Map - One Cell Camera")

# #Load Tile Data
# tile_paths = glob.glob("git\\Lab-Assessment2\\tiles\\*.jpg")
# pattern = re.compile(r"(\d)-(\d)-(\d)-(\d)")
# tile_data = []

# for path in tile_paths:
#     match = pattern.search(path)
#     if match:
#         doors = tuple(int(match.group(i)) for i in range(1, 5))  # (L, R, T, B)
#         img = pygame.image.load(path)
#         scaled_img = pygame.transform.scale(img, (CELL_WIDTH, CELL_HEIGHT))
#         tile_data.append({'surface': scaled_img, 'doors': doors})
#     else:
#         print("Filename does not match door scheme:", path)


#Load and Scale the Map Files directly
map_surface_L = pygame.image.load("Lab-Assessment2/Map-L.png")
map_surface_R = pygame.image.load("Lab-Assessment2/Map-R.png")
# Scale each map to the expected grid size: 6 columns by 5 rows.
scaled_map_size = (MAP_COLS * CELL_WIDTH, MAP_ROWS * CELL_HEIGHT)
map_surface_L = pygame.transform.scale(map_surface_L, scaled_map_size)
map_surface_R = pygame.transform.scale(map_surface_R, scaled_map_size)

#Combine the two maps side-by-side into one surface
combined_map_surface = pygame.Surface((combined_map_width, combined_map_height))
combined_map_surface.blit(map_surface_L, (0, 0))
combined_map_surface.blit(map_surface_R, (MAP_COLS * CELL_WIDTH, 0))

#Load Player Sprite
sprite_sheet = pygame.image.load("Lab-Assessment2/Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Soldier/Soldier/Soldier-Walk.png")
SPRITE_WIDTH = 100
SPRITE_HEIGHT = 100
SPRITE_INDEX = 0

player_sprite = pygame.Surface((SPRITE_WIDTH, SPRITE_HEIGHT), pygame.SRCALPHA)
player_sprite.blit(sprite_sheet, (0, 0), (SPRITE_INDEX * SPRITE_WIDTH, 0, SPRITE_WIDTH, SPRITE_HEIGHT))
player_sprite = pygame.transform.scale(player_sprite, (SPRITE_WIDTH * 4, SPRITE_HEIGHT * 4))

# Start at the center cell of Map-L
player_x = (MAP_COLS // 2) * CELL_WIDTH
player_y = (MAP_ROWS // 2) * CELL_HEIGHT
player_speed = 5

clock = pygame.time.Clock()

while True:
    clock.tick(60)  # 60 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Save the current position before applying movement.
    prev_x, prev_y = player_x, player_y

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Prevent the player from moving off the screen.
    player_x = max(0, min(player_x, combined_map_width - 1))
    player_y = max(0, min(player_y, combined_map_height - 1))

    # Check the color at the player's new position on the combined map.
    collision_color = combined_map_surface.get_at((int(player_x), int(player_y)))
    if collision_color[:3] == (0, 0, 12):
        # If blackish, stop the player.
        player_x, player_y = prev_x, prev_y

    # Calculate camera position so that the player stays centered.
    camera_x = player_x - CELL_WIDTH // 2
    camera_y = player_y - CELL_HEIGHT // 2
    # Clamp the camera so it doesn't scroll out of the combined map.
    camera_x = max(0, min(camera_x, combined_map_width - CELL_WIDTH))
    camera_y = max(0, min(camera_y, combined_map_height - CELL_HEIGHT))
    camera_rect = pygame.Rect(camera_x, camera_y, CELL_WIDTH, CELL_HEIGHT)

    # Draw the visible portion of the combined map.
    screen.blit(combined_map_surface, (0, 0), camera_rect)
    # Draw the player relative to the camera.
    player_draw_x = player_x - camera_rect.x - (player_sprite.get_width() // 2)
    player_draw_y = player_y - camera_rect.y - (player_sprite.get_height() // 2)
    screen.blit(player_sprite, (player_draw_x, player_draw_y))
    
    pygame.display.update()