import pygame

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors (for debugging)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)  # Player
RED = (255, 0, 0)  # NPC

# Load player sprite (replace with actual image)
player_sprite = pygame.Surface((32, 48), pygame.SRCALPHA)  # Placeholder sprite
player_sprite.fill(BLUE)

# Load NPC sprite (replace with actual image)
npc_sprite = pygame.Surface((32, 48), pygame.SRCALPHA)  # Placeholder sprite
npc_sprite.fill(RED)

# Player settings
player = {"sprite": player_sprite, "rect": pygame.Rect(100, 100, 32, 48), "hitbox": pygame.Rect(100, 132, 32, 16)}
player_speed = 4

# NPC settings (each has a sprite, rect, and hitbox)
npcs = [
    {"sprite": npc_sprite, "rect": pygame.Rect(200, 200, 32, 48), "hitbox": pygame.Rect(200, 232, 32, 16)},
    {"sprite": npc_sprite, "rect": pygame.Rect(400, 300, 32, 48), "hitbox": pygame.Rect(400, 332, 32, 16)},
]

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)

    # Movement handling
    keys = pygame.key.get_pressed()
    new_x, new_y = player["rect"].x, player["rect"].y  # Store new position

    if keys[pygame.K_LEFT]:
        new_x -= player_speed
    if keys[pygame.K_RIGHT]:
        new_x += player_speed
    if keys[pygame.K_UP]:
        new_y -= player_speed
    if keys[pygame.K_DOWN]:
        new_y += player_speed

    # Create a new hitbox for future position check
    new_player_hitbox = pygame.Rect(new_x, new_y + 32, 32, 16)  # Lower part of player

    # Check collision with NPC hitboxes
    if not any(new_player_hitbox.colliderect(npc["hitbox"]) for npc in npcs):
        player["rect"].x, player["rect"].y = new_x, new_y  # Move only if no collision
        player["hitbox"].x, player["hitbox"].y = new_x, new_y + 32  # Update hitbox position

    # Sort characters by Y-coordinate (for proper layering)
    characters = [player] + npcs
    characters.sort(key=lambda char: char["rect"].y)

    # Draw characters in correct order
    for char in characters:
        screen.blit(char["sprite"], (char["rect"].x, char["rect"].y))

    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(30)

pygame.quit()
