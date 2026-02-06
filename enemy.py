import pygame as pg
from random import *
from sprites import Bullet

class Enemy(pg.sprite.Sprite):
    def __init__(self, img, height, width, x, y, end, k_speed=1, k_health=1, k_size=1):
        super().__init__()
        
        self.img = img
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.k_speed = k_speed
        self.k_health = k_health
        self.k_size = k_size
        self.end = end

        self.base_health = 100
        self.base_speed = 3.5

        self.stats_init()
        self.sized_scale()

    def reset(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def stats_init(self):
        self.speed = self.base_speed * self.k_speed
        self.health = self.base_speed * self.k_health

    def sized_scale(self):
        self.image = pg.transform.scale(pg.image.load(self.img), (self.width*self.k_size, self.height*self.k_size))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= self.end:
            self.kill()




class Enemy_Soldier(Enemy):
    def __init__(self, img, height, width, x, y, start, end, delay, bullet_group):
        super().__init__(img, height, width, x, y, end)
        self.health = self.base_health * 3
        self.armor_value = 1000
        self.direction = choice(['right', 'left'])
        self.start = start
        self.end = end
        self.delay = delay
        self.last_shot_time = pg.time.get_ticks()
        self.bullet_group = bullet_group
        

    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom, 10, 30 ,30, 34, 1)
        self.bullet_group.add(bullet)
        

    def update(self):
        if self.direction == 'right':
            self.rect.x += self.base_speed
            if self.rect.right >= self.start:
                self.direction = 'left'
        else:
            self.rect.x -= self.base_speed
            if self.rect.left <= self.end:
                self.direction = 'right'
                
        now = pg.time.get_ticks()
        if now - self.last_shot_time >= self.delay:
            self.last_shot_time = now
            self.fire()