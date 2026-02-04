import pygame as pg

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, speed, height, width, damage, direction):
        super().__init__()
        self.image = pg.Surface((width, height))
        if direction == -1:
            self.image = pg.transform.rotate(self.image, 180)
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center = (x, y))
        self.speed = speed * direction
        self.dir = direction
        self.dmg = damage
        

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 1350 or self.rect.y <= -50:
            self.kill()

