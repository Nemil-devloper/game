import pygame as pg
import sys
from homescreen import *
from object_handler import *
from object_renderer import *
from pathfinding import *
from player import *
from raycasting import *
from npc import *
from sound import *
from weapon import * 
from map import *
from sprite import *

# Game settings
FPS = 60  # Frames per second
RES = (800, 600)  # Resolution
HALF_WIDTH = RES[0] // 2
HALF_HEIGHT = RES[1] // 2


class Game:
    def __init__(self):
        pg.init()
        print("Initializing Game...")
        self.screen = pg.display.set_mode(RES)
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.score = 0
        self.paused = False

        # Pause menu assets
        self.pause_music = pg.mixer.Sound("resources/background/pause.mp3")
        self.pause_image = pg.image.load('resources/background/pause.jpg')
        self.pause_image = pg.transform.scale(self.pause_image, RES)

        # Initialize game components
        self.new_game()

    def new_game(self):
        print("Starting new game...")
        self.map = Map(self)
        self.player = Player(self)
        self.sprite_objects = [SpriteObject(self)]
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        

        # Background music
        pg.mixer.music.load("resources/sound/theme1.mp3")
        pg.mixer.music.play(-1)

    def update(self):
        if not self.paused:
            self.player.update()
            self.raycasting.update()
            self.object_handler.update()
            self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        if not self.paused:
            self.object_renderer.draw()
            self.weapon.draw()
            self.object_renderer.draw_player_health()
            self.object_renderer.draw_score()
            self.draw_crosshair()
        else:
            self.draw_pause_menu()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.paused = not self.paused
                    if self.paused:
                        self.pause_game()
                    else:
                        self.unpause_game()

            if not self.paused:
                self.player.single_fire_event(event)

            if event.type == self.global_event:
                self.global_trigger = True

    def pause_game(self):
        pg.mixer.music.pause()
        pg.mixer.pause()
        self.pause_music.play(-1)

    def unpause_game(self):
        pg.mixer.music.unpause()
        pg.mixer.unpause()
        self.pause_music.stop()

    def draw_crosshair(self):
        crosshair_size = 10
        crosshair_thickness = 2
        crosshair_color = (255, 255, 255)

        pg.draw.line(self.screen, crosshair_color,
                     (HALF_WIDTH - crosshair_size, HALF_HEIGHT),
                     (HALF_WIDTH + crosshair_size, HALF_HEIGHT),
                     crosshair_thickness)

        pg.draw.line(self.screen, crosshair_color,
                     (HALF_WIDTH, HALF_HEIGHT - crosshair_size),
                     (HALF_WIDTH, HALF_HEIGHT + crosshair_size),
                     crosshair_thickness)

    def draw_pause_menu(self):
        self.screen.blit(self.pause_image, (0, 0))
        font = pg.font.Font(None, 74)
        text = font.render('PAUSED', True, (255, 0, 0))
        text_rect = text.get_rect(center=(HALF_WIDTH, HALF_HEIGHT - 50))
        self.screen.blit(text, text_rect)

        menu_font = pg.font.Font(None, 50)
        resume_text = menu_font.render('Press ESC to Resume', True, (255, 255, 255))
        home_text = menu_font.render('Press H to Home Screen', True, (255, 255, 255))

        self.screen.blit(resume_text, (HALF_WIDTH - resume_text.get_width() // 2, HALF_HEIGHT + 10))
        self.screen.blit(home_text, (HALF_WIDTH - home_text.get_width() // 2, HALF_HEIGHT + 70))

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    while True:
        try:
            print("Starting HomeScreen...")
            home_screen_instance = HomeScreen()
            result = home_screen_instance.run()
            print(f"Result received in main loop: {result}")

            if result == "start_game":
                print("Starting Game...")
                game = Game()
                game.run()
            elif result == "quit":
                print("Quitting the game...")
                pg.quit()
                sys.exit()

        except Exception as e:
            print(f"Error: {e}")
            pg.quit()
            sys.exit()

        pg.time.delay(1000)  # Adds a delay of 1 second
