import pygame as pg

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, speed, height, width, damage, direction, color):
        super().__init__()
        self.image = pg.Surface((width, height))
        if direction == -1:
            self.image = pg.transform.rotate(self.image, 180)
            self.image.fill((0, 0, 255))
        else:
            self.image.fill(color)
        self.rect = self.image.get_rect(center = (x, y))
        self.speed = speed * direction
        self.dir = direction
        self.dmg = damage

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 1350 or self.rect.y <= -50:
            self.kill()

        
class Rocket(Bullet):
    def __init__(self, x, y, speed, height, width, damage, direction, color):
        super().__init__(x, y, speed, height, width, damage, direction, color)
        self.image.fill(color)

    def explode(self, effects_group):
        explosion = Effect_sprite('explosion.png', self.rect.centerx, self.rect.centery, self.rect.width, self.rect.height)
        effects_group.add(explosion)
        

class Effect_sprite(pg.sprite.Sprite):
    def __init__(self, img, x, y, width, height):
        super().__init__()
        self.height = height
        self.width = width

        self.size = width   
        self.original_image = pg.image.load(img).convert_alpha()    
        self.image = pg.transform.scale(self.original_image, (self.size, self.size))
        self.rect = self.image.get_rect(center =(x, y))
        self.k_grow = 1
        

    def update(self):
        self.size += self.k_grow

        center = self.rect.center
        self.image = pg.transform.scale(self.original_image, (self.size, self.size))
        self.rect = self.image.get_rect(center = center)

        if self.size >= 400:
            self.kill()


class Laser(Effect_sprite):
    def __init__(self, img, x, y, width, height):
        super().__init__(img, x, y, width, height)
        self.k_grow = 10
        self.y = y
        
    def update(self):
        self.height += self.k_grow

        center = self.rect.center
        self.image = pg.transform.scale(self.original_image, (self.width, self.height))
        self.rect = self.image.get_rect(center = center)
        self.rect.bottom = self.y

        if self.rect.top <= -100:
            self.kill()





        
