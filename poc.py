from game_manager import GameManager
import pygame


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))  # Set screen size

# Create GameManager instance
game_manager = GameManager(screen)

# Run the main menu
game_manager.main_menu()

# Start the main game loop after selecting an option
running = True
while running:
    screen.fill((0, 0, 0))  # Clear the screen

    # Your game logic here (draw player, handle movement, etc.)
    if game_manager.player:
        print(f"Current Player: {game_manager.player.name}, Level: {game_manager.player.level}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()  # Update the screen

pygame.quit()