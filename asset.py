import pygame as pg
from sprites import Bullet

class Asset_manager:
    def __init__(self, filename):
        self.sheet = pg.image.load(filename).convert_alpha()
        self.title_size = 256
        self.data = dict()
        self.sprite_slicer()

    def get_image(self, row, col):
        rect = pg.Rect(col * self.title_size, row * self.title_size, self.title_size, self.title_size)
        return pg.transform.scale(self.sheet.subsurface(rect), (128, 128)) 
    def sprite_slicer(self):
        self.data['body'] = [self.get_image(0,0), self.get_image(0,1), self.get_image(0,2)]
        self.data['engine'] = [self.get_image(1,0), self.get_image(1,1), self.get_image(1,2)]
        self.data['shield'] = [self.get_image(2,i) for i in range(4)]

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, assets_data, bullet_group):
        super().__init__()
        
        self.assets = assets_data
        self.state_idx = 1
        self.shield_active = False
        self.shield_frame = 0
        self.health = 100
        self.bullet_group = bullet_group

        self.speed = 8
        self.shield_speed = 0.2
        self.image = pg.Surface((128, 128), pg.SRCALPHA)
        self.rect = self.image.get_rect(center = (x, y))

    def build_image(self):
        self.image.fill((0, 0, 0, 0))

        engine_img = self.assets['engine'][self.state_idx]
        self.image.blit(engine_img, (0, 0))

        body_img = self.assets['body'][self.state_idx]
        self.image.blit(body_img, (0, 0))
        
        if self.shield_active:
            shield_idx = int(self.shield_frame)
            shield_img = self.assets['shield'][shield_idx]
            self.image.blit(shield_img, (0, 0))

    def normal_fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom, 15, 30 ,20, 50, -1)
        self.bullet_group.add(bullet)

    def update(self):
        keys = pg.key.get_pressed()
        
        if keys[pg.K_LEFT]:
            self.rect.x -= self.speed
            self.state_idx = 0

        elif keys[pg.K_RIGHT]:
            self.rect.x += self.speed
            self.state_idx = 2

        else:
            self.state_idx = 1

        if self.shield_active:
            self.shield_frame += self.shield_speed
            if self.shield_frame >= len(self.assets['shield']):
                self.shield_frame = 0

        self.build_image()

    def toggle_shield(self):
        self.shield_active = not self.shield_active
        if self.shield_active:
            self.shield_frame = 0

    def death(self):
        pass






































































