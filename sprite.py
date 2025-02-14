import pygame

class Sprite:
    def __init__(self, sprite_paths, sprite_width, sprite_height, scale_factor, num_frames_dict, animation_speed):
        """
        sprite_paths: A dictionary of animation states (e.g., {"walk": "path1", "attack": "path2"}).
        """
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.scale_factor = scale_factor
        self.num_frames_dict = num_frames_dict
        self.animation_speed = animation_speed
        self.current_frame = 0
        self.is_flipped = False
        self.animations = {}  # Store different animation frames
        self.current_animation = "Walk"  # Default animation state

        # Load all animations
        for state, path in sprite_paths.items():
            animation_type = path.split("/")[-1].replace(".png", "").split("-")[-1]
            sprite_sheet = pygame.image.load(path)
            self.num_frames = self.num_frames_dict[animation_type]
            frames = []
            for i in range(self.num_frames):
                frame = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
                frame.blit(sprite_sheet, (0, 0), (i * sprite_width, 0, sprite_width, sprite_height))
                frame = pygame.transform.scale(frame, (sprite_width * scale_factor, sprite_height * scale_factor))
                frames.append(frame)
            self.animations[state] = frames  # Store frames for each animation state
        
    def set_animation(self, state):
        """Change animation state (e.g., 'walk', 'attack')."""
        if state in self.animations:
            self.current_animation = state
            self.current_frame = 0  # Reset animation frame

    def update_frame(self):
        """Update the animation frame for movement."""
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
                new_size = (self.sprite_width * self.scale_factor, self.sprite_height * self.scale_factor)
                resized_frames.append(pygame.transform.scale(frame, new_size))
            self.animations[state] = resized_frames

    def force_last_frame(self):
        """Freeze the animation at the last frame."""
        if self.current_animation == "Death":
            self.current_frame = self.num_frames_dict["Death"] - 1  # Stay on the last frame