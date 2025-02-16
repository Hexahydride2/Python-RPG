import pygame
import random
import math
from character import Character
from utilities import check_collision
from battle import Battle


# Function to create multiple enemies
def create_enemies(num_enemies, player_x, player_y, x_id, y_id, WIDTH, HEIGHT):
    enemies = []
    min_distance_from_player = 60  # Minimum distance between player and enemy
    min_distance_between_enemies = 80  # Minimum distance between enemies

    while len(enemies) < num_enemies:
        enemy_x = random.randint(50, WIDTH - 50)
        enemy_y = random.randint(50, HEIGHT - 50)
        
        # Ensure enemy is at least 60 pixels away from the player
        distance_to_player = math.sqrt((enemy_x - player_x) ** 2 + (enemy_y - player_y) ** 2)
        if distance_to_player < min_distance_from_player:
            continue  # Skip this position and try again
        
        # Ensure enemy does not overlap with other enemies
        too_close = False
        for enemy in enemies:
            distance_to_enemy = math.sqrt((enemy_x - enemy["x"]) ** 2 + (enemy_y - enemy["y"]) ** 2)
            if distance_to_enemy < min_distance_between_enemies:
                too_close = True
                break  # No need to check further

        if too_close:
            continue  # Skip this position and try again

        # Create new enemy if all conditions are met
        new_enemy = Character(name="Orc",
                              level=random.randint(3, 7),
                              hp=random.randint(30, 60),
                              mp=random.randint(50, 100),
                              atk=random.randint(30, 50),
                              dfn=random.randint(5, 15),
                              spd=random.randint(5, 15),
                              inventory={},
                              folder_paths=[fR".\timefantasy_characters\timefantasy_characters\frames\chara\chara{x_id}_{y_id}", fR".\tf_svbattle\singleframes\set{x_id}\{y_id}"]
                              )
        new_enemy.sprite.set_animation(state='Idle')
        enemies.append({"character": new_enemy, "x": enemy_x, "y": enemy_y})
    return enemies


# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Character Animation")

# Scale images (adjust the size as needed)
SCALE_FACTOR = 2  # Change this to make the character bigger or smaller

# Animation variables
clock = pygame.time.Clock()
frame = 0
frame_delay = 8  # Adjust this to make animation slower
frame_counter = 0  # Controls when to switch frames
player_x, player_y = 100, 300  # Position of the character
speed = 5
moving = False  # Track movement state
current_direction = "down"  # Default direction

# Battle window settings
battle_screen = False  # Track whether battle is in progress
current_enemy = None

playerID_x, playerID_y = 2, 1

player = Character(
                   name="Hero",
                   level=10,
                   hp=100,
                   mp=50,
                   atk=30,
                   dfn=20,
                   spd=30,
                   inventory={"Potion": 2, "Mana Crystal": 3}, 
                   folder_paths=[fR".\timefantasy_characters\timefantasy_characters\frames\chara\chara{playerID_x}_{playerID_y}", fR".\tf_svbattle\singleframes\set{playerID_x}\{playerID_y}"]
                   )



# Create enemies in the random location
enemies = create_enemies(num_enemies=3, player_x=player_x, player_y=player_y, x_id=5, y_id=8, WIDTH=WIDTH, HEIGHT=HEIGHT)
for enemy in enemies:
    enemy["character"].sprite.set_animation("down_stand")

running = True
while running:
    screen.fill((255, 255, 255))  # Clear screen

    # Event handling
    keys = pygame.key.get_pressed()  # Get currently pressed keys

    if keys[pygame.K_LEFT]:  
        player_x -= speed
        moving = True
        current_direction = "left"
       
    elif keys[pygame.K_RIGHT]:  
        player_x += speed
        moving = True
        current_direction = "right"
        
    elif keys[pygame.K_UP]:  
        player_y -= speed
        moving = True
        current_direction = "up"
        
    elif keys[pygame.K_DOWN]:  
        player_y += speed
        moving = True
        current_direction = "down"
       
    else:
        moving = False  # Stop animation if no key is pressed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Go to battle window
    if battle_screen and current_enemy:
        battle = Battle(screen, player, current_enemy["character"], background_image=".\craftpix-net-270096-free-forest-battle-backgrounds\PNG\game_background_4\game_background_4.png")
        result = battle.run()

        if result == "win":
            enemies.remove(current_enemy)
            battle_screen = False  # Exit battle screen
            player_x += 60  # Move player away to prevent instant re-entry

        elif result == "lose":
            battle_screen = False  # Exit battle screen
            player_x += 60  # Move player away to prevent instant re-entry

        elif result == "escape":
            battle_screen = False  # Exit battle screen
            player_x += 60  # Move player away to prevent instant re-entry

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check for collisions with enemies
    for enemy in enemies:
        if check_collision(player_x, player_y, enemy["x"], enemy["y"]):
            battle_screen = True
            current_enemy = enemy  # Store current enemy for battle
            break  # Only trigger one battle at a time
    
    # Display Walk motion only moving
    if moving == True:
        player.sprite.set_animation(f"{current_direction}_walk")
    else:
        player.sprite.set_animation(f"{current_direction}_stand")


    # Draw enemies
    for enemy in enemies:
        enemy["character"].sprite.update_frame()
        enemy["character"].sprite.draw(screen, enemy["x"], enemy["y"])

    # Display the current frame
    player.sprite.is_flipped = False
    player.sprite.update_frame()
    player.sprite.draw(screen, player_x, player_y)




    pygame.display.update()
    clock.tick(30)  # Control animation speed (10 FPS)

pygame.quit()
