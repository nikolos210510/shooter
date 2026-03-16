import pygame as pg
pg.init()

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, speed, height, width, damage, direction, color):
        super().__init__()
        
        self.image = pg.Surface((width, height))
        if direction == -1:
            self.image = pg.transform.scale(pg.image.load('bullet.png'),(width, height))
            
        else:
            self.image.fill(color)
        self.rect = self.image.get_rect(center = (x, y))
        self.speed = speed * direction
        self.dir = direction
        self.dmg = damage
        self.poison_dmg = 1.5

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 1350 or self.rect.y <= -50:
            self.kill()

        
class Rocket(Bullet):
    def __init__(self, x, y, speed, height, width, damage, direction, color):
        super().__init__(x, y, speed, height, width, damage, direction, color)
        self.image.fill(color)

    def explode(self, effects_group):
        explosion = Effect_sprite('explosion.png', self.rect.centerx, self.rect.centery, self.rect.width, self.rect.height, 'temp')
        effects_group.add(explosion)

class Poison_rocket(Bullet):
    def __init__(self, x, y, speed, height, width, damage, direction, color):
        super().__init__(x, y, speed, height, width, damage, direction, color)
        self.image.fill(color)

    def poison(self, effects_group):
        poison = Effect_sprite('poison.png', self.rect.centerx, self.rect.centery, self.rect.width, self.rect.height, 'area')
        effects_group.add(poison)

        

class Effect_sprite(pg.sprite.Sprite):
    def __init__(self, img, x, y, width, height, kind):
        super().__init__()
        self.height = height
        self.width = width
        self.kind = kind

        self.size = width   

        
        self.original_image = pg.image.load(img).convert_alpha()    
        self.image = pg.transform.scale(self.original_image, (self.size, self.size))
        self.rect = self.image.get_rect(center =(x, y))
        self.k_grow = 3
        self.now = pg.time.get_ticks()
        

    def update(self):

        if self.size < 400: 
            self.size += self.k_grow
            center = self.rect.center
            self.image = pg.transform.scale(self.original_image, (self.size, self.size))
            self.rect = self.image.get_rect(center = center)
        if self.size > 400:
            if self.kind == 'temp': 
                self.kill()
            else:
                if pg.time.get_ticks() - self.now > 5000:
                    self.kill()



        



class Laser(Effect_sprite):
    def __init__(self, img, x, y, width, height, kind):
        super().__init__(img, x, y, width, height, kind)
        self.k_grow = 15
        self.y = y
        
    def update(self):
        if self.rect.top > 0:
            self.height += self.k_grow
            self.rect.bottom = self.y

        center = self.rect.center
        self.image = pg.transform.scale(self.original_image, (self.width, self.height))
        self.rect = self.image.get_rect(center = center)
            

        if self.rect.top <= 0:
                self.rect.y -= self.k_grow






        
