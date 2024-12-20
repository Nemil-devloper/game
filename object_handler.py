from npc import *
from sprite import *
from random import choices, randrange
import pygame as pg

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        self.npc_positions = {}
        self.enemies = 50  # NPC count
        self.npc_types = [SoldierNPC, CacoDemonNPC, CyberDemonNPC]
        self.weights = [70, 20, 10]
        self.restricted_area = {(i, j) for i in range(min(10, self.game.map.cols))
                                for j in range(min(10, self.game.map.rows))}
        self.spawn_npc()
        self.initialize_sprites()

    def initialize_sprites(self):
        add_sprite = self.add_sprite
        add_sprite(AnimatedSprite(self.game))
        add_sprite(AnimatedSprite(self.game, pos=(1.5, 1.5)))
        add_sprite(AnimatedSprite(self.game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 7.5)))

    def spawn_npc(self):
        max_attempts = 100  # Prevent infinite loops
        for i in range(self.enemies):
            attempts = 0
            npc = choices(self.npc_types, self.weights)[0]
            pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
            while ((pos in self.game.map.world_map) or (pos in self.restricted_area)) and attempts < max_attempts:
                pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                attempts += 1
            if attempts < max_attempts:
                self.add_npc(npc(self.game, pos=(x + 0.5, y + 0.5)))
            else:
                print(f"Failed to spawn NPC after {max_attempts} attempts.")

    def check_win(self):
        if not self.npc_positions and self.game.running:
            self.game.object_renderer.win()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        for sprite in self.sprite_list:
            sprite.update()
        for npc in self.npc_list:
            npc.update()
        self.check_win()

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)