import pygame
import time
from character import Character, NPC
from text_manager import TextManager
from map_manager import Map
from battle import Battle
from utilities import change_theme, revert_theme


class Scene:
    def __init__(self, screen, characters, actions, speed=5, top_left_x=0, top_left_y=0, background_image=None, scale_factor=None):
        """
        Initialize the scene with characters and a list of actions.
        
        :param characters: List of Character objects involved in the scene.
        :param actions: List of dictionaries defining the actions.
                        Example: [{"character": character1, "direction": "left", "distance": 100}]
        """
        self.screen = screen
        self.characters = characters
        self.actions = actions
        self.current_action_index = 0
        self.is_scene_active = False
        self.speed = speed
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.view_width, self.view_height = screen.get_width(), screen.get_height()
        if background_image:
            self.background = pygame.image.load(background_image)
        else:
            self.background = None
        if scale_factor:
            self.background = pygame.transform.scale(self.background, (self.background.get_width()*scale_factor, self.background.get_height()*scale_factor))

        self.text_manager = TextManager(screen)
        self.waiting_for_dialogue = False # Track if the scene is waiting for dialogue
        self.action_timer = 0 # Timer for wait actions
        self.waiting_for_enter = False  # Flag to wait for ENTER

        self.clock = pygame.time.Clock()

        self.player_party = None
        self.running = True

    def start(self):
        """Start the scene."""
        self.is_scene_active = True
        self.current_action_index = 0

    def update(self, event):
        """Update the scene by executing the next action incrementally."""
        if not self.is_scene_active or self.current_action_index >= len(self.actions):
            return
        
        if self.background:
            self.screen.blit(self.background, (0,0), (self.top_left_x, self.top_left_y, self.view_width, self.view_height))
        else:
            # Fill the screen with black
            self.screen.fill((0, 0, 0))
       
    
        action = self.actions[self.current_action_index]
        action_type = action["type"]

        if action_type == "move":
            self.handle_move(action)
        elif action_type == "talk":
            self.handle_talk(action, event)
        elif action_type == "wait":
            self.handle_wait(action)
        elif action_type == "battle":
            self.handle_battle(action)
        elif action_type == "animation":
            self.handle_animation(action)

        # self.text_manager.update()
        # self.text_manager.draw()

    def handle_move(self, action):
        action = self.actions[self.current_action_index]
        character = action["character"]
        direction = action["direction"]
        distance = action["distance"]

        character.move(direction)
    
        # Check if the character has reached the target position
        if self._is_action_complete(character, direction, distance):
            # Set the standing animation when the movement is complete
            character.initial_x, character.initial_y = character.x, character.y
            character.sprite.set_animation(f"{direction}_stand")
            self.current_action_index += 1

    def handle_talk(self, action, event):
        """Handle talk action and trigger text manager."""
        character = action["character"]
        message = action["message"]

        if not self.text_manager.messages:
            if character:
                self.text_manager.add_message(message, speaker=character.name)
            else:
                self.text_manager.add_message(message)
        

        if event != None:
            # If message is complete and waiting for Enter, we proceed
            if self.text_manager.message_finished:
                self.waiting_for_enter = True

        # If ENTER is pressed and we're waiting, move to the next action
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if not self.text_manager.message_finished:
                        self.text_manager.skipping = True
                    elif self.text_manager.waiting_for_next:
                        if len(self.text_manager.messages) > 1:
                            # If there are more messages, go to the next one
                            self.text_manager.next_message()
                            self.waiting_for_enter = False
                        else:
                            # If no more messages, move to the next action
                            self.text_manager.next_message()
                            self.waiting_for_enter = False
                            self.current_action_index += 1  # Move to the next action
       
        

    def handle_wait(self, action):
        """Handle wait action for a specific duration."""
        duration = action["duration"]
        frame_duration = 1000 /30 # Frame duration based on 30 FPS
        self.action_timer += frame_duration

        if self.action_timer >= duration:
            self.action_timer = 0
            self.current_action_index += 1

    def handle_battle(self, action):
        """handle a battle action."""
        enemies = action["enemies"]
        self.player_party = action["player_party"]
        background_image = action.get("background_image", None)  # Optional background image
        
        # Start the battle
        battle = Battle(self.screen, self.player_party.members, enemies, background_image, escape_chance=0)
        self.battle_result = battle.run()
        self.battle_screen = False  # Exit battle 

        if self.battle_result == "Victory":
            pass     
                    
        elif self.battle_result == "Defeat":
            self.running = False
        
        self.player_party.leader.sprite.is_flipped = False
        self.current_action_index += 1  

        revert_theme()

    def handle_animation(self, action):
        """handle a pose of character"""
        character = action["character"]
        animation = action["pose"]
        character.sprite.set_animation(animation)
        self.current_action_index  += 1

    def _is_action_complete(self, character, direction, distance):
        """Check if the character has completed the movement."""
        if direction == "left":
            return character.x <= character.initial_x - distance
        elif direction == "right":
            return character.x >= character.initial_x + distance
        elif direction == "up":
            return character.y <= character.initial_y - distance
        elif direction == "down":
            return character.y >= character.initial_y + distance
        return False

    def run(self):
        """Run the scene's game loop"""
        self.start()

        # Handling UnboundLocalError event is not asscociated with a value
        event = None
        while self.running:
            self.screen.fill((255,255,255))
              
            self.update(None)
            
            # Draw characters and update the display
            for character in self.characters:
                character.sprite_is_fliped = False
                character.sprite.update_frame()
                character.sprite.draw(self.screen, character.x, character.y)
            
            # Check if the scene is finished
            if self.current_action_index >= len(self.actions):
                self.running = False

            self.text_manager.update()
            self.text_manager.draw()
            
            pygame.display.flip()
            self.clock.tick(30)


#################################################
# pygame.init()
# screen_width = 1280
# screen_height = 720
# screen = pygame.display.set_mode((screen_width, screen_height))
# clock = pygame.time.Clock()

# military_paths = [R".\timefantasy_characters\timefantasy_characters\frames\military\military1_8",
#                   R".\tf_svbattle\singleframes\military1\8"]
# # Create a player
# player = Character(
#     name="Hero",
#     x=500,
#     y=500,
#     level=10,
#     hp=100,
#     mp=50,
#     atk=40,
#     dfn=20,
#     spd=30,
#     inventory={},
#     folder_paths=military_paths
# )

# npc_path = [R".\timefantasy_characters\timefantasy_characters\frames\npc\npc1_1"]
# npc = Character(
#     name="NPC",
#     x=200,
#     y=200,
#     level=10,
#     hp=100,
#     mp=50,
#     atk=40,
#     dfn=20,
#     spd=30,
#     inventory={},
#     folder_paths=npc_path
# )


# # Define the actions for the scene

# actions = [
#     {"type": "move", "character": player, "direction": "left", "distance": 100},
#     {"type": "move", "character": npc, "direction": "right", "distance": 50},
#     {"type": "wait", "duration": 500},  # Wait for 500ms before the next action
#     {"type": "talk", "character": npc, "message": "Hello, Hero! I have something to tell you. Nice to meet you."},
#      {"type": "wait", "duration": 5000},  # Wait for 5000ms before the next action
#     {"type": "move", "character": player, "direction": "right", "distance": 100},
#     {"type": "move", "character": npc, "direction": "down", "distance": 50},
#     {"type": "move", "character": npc, "direction": "left", "distance": 50},
#     {"type": "move", "character": npc, "direction": "up", "distance": 50},
# ]


# # Create the scene
# scene = Scene(screen, [player, npc], actions, top_left_x=600, top_left_y=100, background_image=".\Backgrounds\map.png", scale_factor=3)


# # Start the scene
# scene.start()



# running = True
# while running:
#     screen.fill((255,255,255))
#     events = pygame.event.get()
#     keys = pygame.key.get_pressed()

#     for event in events:
#         if event.type == pygame.QUIT:
#             running = False

    
#     # Update the scene
#     if scene.is_scene_active:
#         scene.update(event)
#         #print(scene.current_action_index)
  
#     # Draw characters and update the display
#     for character in scene.characters:
#         character.sprite.update_frame()
#         character.sprite.draw(screen, character.x, character.y)

#     pygame.display.flip()
#     clock.tick(30)
# pygame.quit()