import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *
from playsound import *


# Initialize Pygame
pg.init()

# Set up the screen
screen_width = 1600
screen_height = 900
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Crosshair Example")

# Set colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up variables for the crosshair
crosshair_size = 20
crosshair_thickness = 2

# Function to draw the crosshair
def draw_crosshair(x, y):
    pg.draw.line(screen, white, (x - crosshair_size, y), (x + crosshair_size, y), crosshair_thickness)
    pg.draw.line(screen, white, (x, y - crosshair_size), (x, y + crosshair_size), crosshair_thickness)

class Game:
    def __init__(self):
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill(black)  # Clear the screen before drawing
        self.object_renderer.draw()
        self.weapon.draw()
        self.player.draw()  # Add player drawing if necessary
        draw_crosshair(screen_width // 2, screen_height // 2)  # Draw the crosshair
        pg.display.flip()  # Update the display

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

# Main game loop
if __name__ == '__main__':
    game = Game()
    game.run()

pg.quit()
sys.exit()
