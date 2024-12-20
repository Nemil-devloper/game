from sound import *
from sprite import *
from settings import *


class Weapon(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/0.png', scale=0.3, animation_time=30):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 80

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False  # Prevent further shots during reload
            if self.animation_trigger:  # Trigger the animation after the set time
                self.images.rotate(-1)  # Rotate images for animation
                self.image = self.images[0]  # Set the current frame
                self.frame_counter += 1
                if self.frame_counter == self.num_images:  # Reload complete
                    self.reloading = False
                    self.frame_counter = 0

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()
