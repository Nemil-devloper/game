import pygame as pg

class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = "resources\\sound\\"
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun.mp3')
        self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav')
        self.npc_death = pg.mixer.Sound(self.path + 'npc_death.wav')
        self.npc_shot = pg.mixer.Sound(self.path + 'npc_attack.wav')
        self.npc_shot.set_volume(0.5)
        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav')
        pg.mixer.music.load(self.path + 'theme.mp3')
        pg.mixer.music.set_volume(0.6)

    def play_shotgun(self):
        self.shotgun.play()

    def play_npc_pain(self):
        self.npc_pain.play()

    def play_npc_death(self):
        self.npc_death.play()

    def play_npc_shot(self):
        self.npc_shot.play()

    def play_player_pain(self):
        self.player_pain.play()

    def play_background_music(self):
        pg.mixer.music.play(-1, 0.0)  # Loop music
