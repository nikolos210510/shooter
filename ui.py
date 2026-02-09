import pygame as pg

class HUD:
    def __init__(self, w, h):
        self.surface = pg.Surface((w, h))
        self.width = w
        self.height = h
        self.font = pg.font.SysFont('Roboto', 22)
        self.bg_color = (40, 40, 45)
        self.font_color = (255, 255, 255)

    def draw(self, score, time, ammo, weapon_name, weapon_timer):
        self.surface.fill(self.bg_color)

        score_img = self.font.render(f'SCORE:      {score}', True, self.font_color)
        self.surface.blit(score_img, (20, 20))

        time_img = self.font.render(f'Timer:      {time}', True, self.font_color)
        self.surface.blit(time_img, (20, 100))


