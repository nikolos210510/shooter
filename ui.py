import pygame as pg

class HUD:
    def __init__(self, w, h):
        self.surface = pg.Surface((w, h))
        self.width = w
        self.height = h
        self.font = pg.font.SysFont('Roboto', 22)
        self.bg_color = (40, 40, 45)
        self.font_color = (255, 255, 255)

    def draw(self, score, time, health, rocket_ammo, laser_ammo):
        self.surface.fill(self.bg_color)

        score_img = self.font.render(f'SCORE:   {score}', True, self.font_color)
        self.surface.blit(score_img, (20, 20))

        time_img = self.font.render(f'TIME:   {time}', True, self.font_color)
        self.surface.blit(time_img, (20, 100))

        health_img = self.font.render(f'HEALTH:   {health}', True, self.font_color)
        self.surface.blit(health_img, (20, 180))

        rocket_ammo_img = self.font.render(f'ROCKETS:   {rocket_ammo}', True, self.font_color)
        self.surface.blit(rocket_ammo_img, (20, 260))

        laser_ammo_img = self.font.render(f'LASER:   {laser_ammo}', True, self.font_color)
        self.surface.blit(laser_ammo_img, (20, 340))


