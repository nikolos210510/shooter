import pygame as pg
from ui import HUD
from asset import Asset_manager, Player
from enemy import Enemy, Enemy_Soldier
from random import *



class Game:
    def __init__(self):
        pg.init()
        self.win_w = 2000
        self.win_h = 1300
        self.screen = pg.display.set_mode((self.win_w, self.win_h))
        self.clock = pg.time.Clock()
        self.FPS = 90
        self.runnig = True
        self.game_area_w = self.win_w * 0.85
        self.hud_area_w = self.win_w * 0.15
        self.hud = HUD(self.hud_area_w, self.win_h)
        self.game_rect = pg.Rect(self.hud_area_w, 0, self.game_area_w, self.win_h)
        
        self.main_timer = 0
        self.score = 0

        self.ammo = 30
        self.cur_weapon = 'Blaster'
        self.weapon_energy = 1.0

        self.all_enemies = pg.sprite.Group()
        self.enemy_bullet_group = pg.sprite.Group()
        self.player_bullet_group = pg.sprite.Group()

        self.spawn_delay = 1000
        self.last_generating = pg.time.get_ticks()
        self.start_game_time = pg.time.get_ticks()
        self.is_game_active = True

        self.asset_manager = Asset_manager('player_sprite.png')
        self.player = Player(self.win_w // 2, self.win_h - 300, self.asset_manager.data, self.player_bullet_group)
    
    
    def draw(self):
        pg.draw.rect(self.screen, (0, 0, 0), self.game_rect) 
        self.hud.draw(self.score, round(self.main_timer/1000, 2), self.ammo, self.cur_weapon, self.weapon_energy)
        self.screen.blit(self.hud.surface, (0, 0))

        self.all_enemies.draw(self.screen)
        self.screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
        self.enemy_bullet_group.draw(self.screen)
        self.player_bullet_group.draw(self.screen)

        pg.display.flip()

    def choose_enemy(self):
        self.enemy_spawn_area_x = randint(int(self.hud_area_w), int(self.game_area_w))
        chance = randint(0,100)
        if chance <= 30 or chance > 80:
            return Enemy('enemy4.png', 128, 128, self.enemy_spawn_area_x, -200, self.win_h)  #есть ли смысл создание самх врагов в свойства вносить?
        elif 40 > chance >= 30:
            return Enemy('enemy5.png', 128, 128, self.enemy_spawn_area_x, -200, self.win_h, 2/3, 1.5, 2 )
        elif 70 > chance >= 40:
            return Enemy('enemy6.png', 128, 128, self.enemy_spawn_area_x, -200, self.win_h, 1.5, 0.5, 2/3 )
        elif 80 >= chance >= 70:
            return Enemy_Soldier('enemy2.png', 180, 180, self.win_w//2, 0, self.game_rect.right, self.game_rect.left, 2000, self.enemy_bullet_group)

    def spawn_enemy(self):
        now = pg.time.get_ticks()    
        if now - self.last_generating >= self.spawn_delay:
            new_enemy = self.choose_enemy()
            self.all_enemies.add(new_enemy)
            self.last_generating = now

    def collide_manager(self):
        collided_bullets = pg.sprite.spritecollide(self.player, self.enemy_bullet_group, True)
        if not self.player.shield_active:
            if collided_bullets:
                for bullet in collided_bullets:                    
                    self.player.health -= bullet.dmg
                    if self.player.health <= 0:
                        print('death')
                        self.is_game_active = False

        if pg.sprite.spritecollide(self.player, self.all_enemies, True):
            if self.player.shield_active:
                self.player.shield_active = False
            else:
                self.is_game_active = False

        collided_dict = pg.sprite.groupcollide(self.player_bullet_group, self.all_enemies, True, False)
        if collided_dict:
            print(collided_dict)
            for bullet in collided_dict:
                for enemy in collided_dict[bullet]:
                    enemy.health -= bullet.dmg
        

        
    def run(self):

        while self.runnig:            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.runnig = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        self.player.toggle_shield()
                    if event.key == pg.K_c:
                        self.player.normal_fire()
                

            if self.is_game_active:
                self.all_enemies.update()
                self.enemy_bullet_group.update()
                self.player_bullet_group.update()
                self.player.update()
                self.collide_manager()
                self.spawn_enemy()

                
                if self.player.rect.left < self.hud_area_w:
                    self.player.rect.left = self.hud_area_w
                if self.player.rect.right > self.win_w:
                    self.player.rect.right = self.win_w


                self.draw()
                self.clock.tick(self.FPS)
                self.main_timer = pg.time.get_ticks() - self.start_game_time


game = Game()
game.run()
