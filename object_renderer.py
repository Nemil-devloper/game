import pygame as pg
import os
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(10)]
        self.digits = dict(zip(map(str, range(10)), self.digit_images))
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('resources/textures/win.png', RES)

    def draw_player_health(self):
        health = str(getattr(self.game.player, 'health', '0'))  # Fallback to '0' if health is missing
        for i, char in enumerate(health):
            self.screen.blit(self.digits.get(char, self.digits['0']), (i * self.digit_size, 0))

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        rel = getattr(self.game.player, 'rel', 0)  # Use 0 if 'rel' attribute is unavailable
        self.sky_offset = (self.sky_offset + 4.5 * rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    def draw_score(self):
        score = str(getattr(self.game, 'score', 0))  # Ensure score is valid
        font = pg.font.Font(None, 36)
        text = font.render(f'Score: {score}', True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            i: self.get_texture(f'resources/textures/{i}.jpg')
            for i in range(1, 6)
        }
