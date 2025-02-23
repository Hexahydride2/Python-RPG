import pygame
import glob
import os
from utilities import split_animation_name


class Sprite:
    def __init__(self, folder_paths, scale_factor, animation_speed):
        """
        sprite_paths: A dictionary of animation states (e.g., {"walk": "path1", "attack": "path2"}).
        """
        self.sprite_shape = {}
        self.scale_factor = scale_factor
        self.num_frames_dict = {}
        self.animation_speed = animation_speed
        self.current_frame = 0
        self.is_flipped = False
        self.animations = {}  # Store different animation frames
        self.current_animation = "down_stand"  # Default animation state
        self.num_frames_dict = {}
        self.frames = {}


        self.load_animations(folder_paths, scale_factor)
            
    def load_animations(self, folder_paths, scale_factor):
        """
        Loads all animations from the specified folder.
        
        :param folder_path: Folder containing animation images.
        :param sprite_width: Width of each frame.
        :param sprite_height: Height of each frame.
        :param scale_factor: Factor to scale the images.
        """
        for folder_path in folder_paths:
            sprite_paths = glob.glob(os.path.join(folder_path, "*.png"))  # Load all images
            for path in sprite_paths:
                filename = os.path.basename(path).replace(".png", "")  # Extract filename
                state, num = split_animation_name(filename)

                if state not in self.frames:
                    self.frames[state] = [path]
                else:
                    self.frames[state].append(path)

                # Update the number of frames in each motion
                self.num_frames_dict[state] = max(1, int(num))

            for state, paths in self.frames.items():
                frames = []
                for path in sorted(paths):
                    image = pygame.image.load(path)
                    frame = pygame.transform.scale(image, (image.get_width() * scale_factor, image.get_height() * scale_factor))
                    frames.append(frame)
                    self.sprite_shape[state] = {"width": image.get_width(), "height": image.get_height()}
                self.animations[state] = frames
        

    def set_animation(self, state):
        """Change animation state (e.g., 'walk', 'attack')."""
        if state in self.animations:
            self.current_animation = state
            if "walk" not in state:
                self.current_frame = 0  # Reset animation frame except for walk motion

    def update_frame(self):
        """Update the animation frame for movement."""
        self.num_frames = self.num_frames_dict[self.current_animation]
        self.current_frame = (self.current_frame + 1) % (self.num_frames * self.animation_speed)

    def draw(self, screen, x, y):
        """Draw the current frame with optional flipping."""
        frame_index = self.current_frame // self.animation_speed
        frame = self.animations[self.current_animation][frame_index]

        if self.is_flipped:
            frame = pygame.transform.flip(frame, True, False)

        screen.blit(frame, (x, y))

    def rescale(self, new_scale_factor):
        """Rescales all animation frames to a new size dynamically."""
        self.scale_factor = new_scale_factor
        for state in self.animations:
            resized_frames = []
            for frame in self.animations[state]:
                new_size = (self.sprite_shape[state]["width"] * self.scale_factor, self.sprite_shape[state]["height"] * self.scale_factor)
                resized_frames.append(pygame.transform.scale(frame, new_size))
            self.animations[state] = resized_frames

    def force_last_frame(self):
        """Freeze the animation at the last frame."""
        if self.current_animation == "Death":
            self.current_frame = self.num_frames_dict["Death"] - 1  # Stay on the last frame