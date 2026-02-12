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



    def explode(self):
        self.image = pg.Surface((self.rect.height, self.rect.height))
        self.update = self.exp_update
        print('привет артур')

    def exp_update(self):
        pg.draw.circle(self.image, (255, 0, 0), (self.rect.x, self.rect.y), self.rect.height//2)
    
        



