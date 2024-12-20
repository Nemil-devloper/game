import pygame as pg
from settings import *

class HomeScreen:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.running = True
        self.background_image = pg.image.load('resources/background/bg.jpg')
        self.bg_music = pg.mixer.Sound("resources/background/bg.mp3")
        self.bg_music.set_volume(0.5)  # Adjust volume if necessary
        self.background_image = pg.transform.scale(self.background_image, RES)

    def stop_music(self):
        self.bg_music.stop()  # Stop the home screen music

    def play_music(self):
        self.bg_music.play(-1)  # Play the home screen music

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        font = pg.font.Font(None, 74)
        title_text = font.render('Home Screen', True, (255, 255, 255))
        start_text = font.render('Press Enter to Start', True, (255, 255, 255))
        quit_text = font.render('Press Q to Quit', True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 100))
        start_rect = start_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        quit_rect = quit_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 100))
        self.screen.blit(title_text, title_rect)
        self.screen.blit(start_text, start_rect)
        self.screen.blit(quit_text, quit_rect)
        pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "quit"
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    return "start_game"
                elif event.key == pg.K_q:
                    return "quit"

    def run(self):
        self.play_music()  # Ensure home screen music is playing
        while True:
            result = self.handle_events()
            if result:
                self.stop_music()  # Ensure music is stopped when leaving the home screen
                return result
            self.draw()
            self.clock.tick(60)