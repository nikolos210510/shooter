import pygame as pg
from ui import HUD
from asset import Asset_manager, Player
from enemy import Enemy, Enemy_Soldier, Enemy_Elite, Loot, Loot_ship
from sprites import Bullet, Rocket, Effect_sprite
from random import *
pg.mixer.init()



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

        self.all_enemies = pg.sprite.Group()
        self.enemy_bullet_group = pg.sprite.Group()
        self.player_bullet_group = pg.sprite.Group()
        self.effects_group = pg.sprite.Group()
        self.allloot_group = pg.sprite.Group()

        self.k_spawn = 1
        self.spawn_delay = 900
        self.last_generating = pg.time.get_ticks()
        self.start_game_time = pg.time.get_ticks()
        self.is_game_active = True

        self.asset_manager = Asset_manager('player_sprite.png')
        self.player = Player(self.win_w // 2, self.win_h - 300, self.asset_manager.data, self.player_bullet_group)
        self.last_speed = 0
        self.last_shield = 0
        self.is_boosted = False
        self.hit_sd = pg.mixer.Sound('hit_sd.wav')
        pg.mixer.music.load('main.wav')


    
    def draw(self):
        pg.draw.rect(self.screen, (0, 0, 0), self.game_rect) 
        self.hud.draw(self.score, round(self.main_timer/1000, 2), self.player.health, self.player.rocket_amount, self.player.laser_amount)
        self.screen.blit(self.hud.surface, (0, 0))

        self.all_enemies.draw(self.screen)
        self.allloot_group.draw(self.screen)
        self.screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
        self.enemy_bullet_group.draw(self.screen)
        self.player_bullet_group.draw(self.screen)
        self.effects_group.draw(self.screen)

        pg.display.flip()

    def choose_enemy(self):
        self.enemy_spawn_area_x = randint(int(self.hud_area_w), int(self.game_area_w))
        chance = randint(0,120)
        if chance <= 40:
            return Enemy('enemy4.png', 128, 128, self.enemy_spawn_area_x, -200, self.win_h)  
        elif 60 > chance > 40:
            return Enemy('enemy5.png', 128, 128, self.enemy_spawn_area_x, -200, self.win_h, 2/3, 1.5, 2, 250)
        elif 80 > chance >= 60:
            return Enemy('enemy6.png', 128, 128, self.enemy_spawn_area_x, -200, self.win_h, 1.5, 0.5, 2/3, 250)
        elif 95 >= chance >= 80:
            return Enemy_Soldier('elite_2.png', 150, 150, self.win_w//2, 50, self.game_rect.right, self.game_rect.left, 2000, self.enemy_bullet_group, 500)
        elif 105 >= chance > 95:
            return Enemy_Elite('enemy2.png', 180, 180, self.win_w//2, 0, self.game_rect.right, self.game_rect.left, 1500, self.enemy_bullet_group, 1000)
        elif  120 >= chance > 105:
            return Loot_ship('box.png', 128, 128, self.enemy_spawn_area_x, -200, self.win_h)
        

    def spawn_enemy(self):
        now = pg.time.get_ticks()    
        if now - self.last_generating >= self.spawn_delay * self.k_spawn:
            new_enemy = self.choose_enemy()
            self.all_enemies.add(new_enemy)
            self.last_generating = now

    def collide_manager(self):
        collided_bullets = pg.sprite.spritecollide(self.player, self.enemy_bullet_group, True)
        if not self.player.shield_active:
            if collided_bullets:
                for bullet in collided_bullets:                    
                    self.player.health -= bullet.dmg
                    self.hit_sd.play()
                    if self.player.health <= 0:
                        self.is_game_active = False

        collided_enemies = pg.sprite.spritecollide(self.player, self.all_enemies, True)
        if collided_enemies:
            if self.player.shield_active:
                self.player.shield_active = False
            else:
                for enemy in collided_enemies:
                    if enemy.k_size == 2:
                        self.player.health -= 100
                    else:
                        self.player.health -=  50
                    if self.player.health <= 0:
                        self.is_game_active = False

        collided_dict = pg.sprite.groupcollide(self.player_bullet_group, self.all_enemies, True, False)
        if collided_dict:
            for bullet in collided_dict:
                if isinstance(bullet, Rocket):
                    bullet.explode(self.effects_group)
                for enemy in collided_dict[bullet]:
                    enemy.health -= bullet.dmg
                    if enemy.health <= 0:
                        if isinstance(enemy, Loot_ship):
                            self.allloot_group.add(enemy.loot_generate())
                        self.score += enemy.score
                        self.spawn_manager()


        collided_dict = pg.sprite.groupcollide(self.effects_group, self.all_enemies, False, False)
        if collided_dict:
            for effect in collided_dict:
                for enemy in collided_dict[effect]:
                    enemy.kill()
                    if isinstance(enemy, Loot_ship):
                            self.allloot_group.add(enemy.loot_generate())
                    self.score += enemy.score

        collided_boosts = pg.sprite.spritecollide(self.player, self.allloot_group, True)
        if collided_boosts:
            for boost in collided_boosts:
                if boost.loot_type == 'shield':
                    self.last_shield = pg.time.get_ticks()
                    self.player.shield_active = True
                elif boost.loot_type  == 'speed_boost':                             
                    if not self.is_boosted: self.player.speed *= 1.5  
                    self.last_speed = pg.time.get_ticks()
                    self.is_boosted = True
                elif boost.loot_type == 'rocket':
                    self.player.rocket_amount += 3              #иногда засчитыввает 2 раза
                elif boost.loot_type == 'laser':
                    self.player.laser_amount += 3              #иногда засчитыввает 2 раза
                    



        

    def spawn_manager(self):
        if 5000 <= self.score < 10000:
            self.k_spawn = 0.65
        elif 10000 <= self.score < 15000:
            self.k_spawn = 0.45



    def run(self):
        
        pg.mixer.music.play()


        while self.runnig:            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.runnig = False

                if event.type == pg.KEYDOWN:
                    ''' if event.key == pg.K_x:
                        self.player.toggle_shield()'''
                    if event.key == pg.K_c and self.player.fire_time_checker():
                        self.player.normal_fire()
                    if event.key == pg.K_v and self.player.fire_time_checker():
                        self.player.rocket_fire()
                    if event.key == pg.K_x and self.player.fire_time_checker():
                        self.player.laser_fire(self.effects_group)
                

            if self.is_game_active:
                self.all_enemies.update()
                self.enemy_bullet_group.update()
                self.player_bullet_group.update()
                self.effects_group.update()
                self.player.update()
                self.allloot_group.update()
                self.collide_manager()
                self.spawn_enemy()

                
                if self.player.rect.left < self.hud_area_w:
                    self.player.rect.left = self.hud_area_w
                if self.player.rect.right > self.win_w:
                    self.player.rect.right = self.win_w


                self.draw()
                self.clock.tick(self.FPS)

                self.main_timer = pg.time.get_ticks() - self.start_game_time

                if self.is_boosted: 
                    if pg.time.get_ticks() - self.last_speed >= 10000:
                        self.player.speed *= 3/4
                        self.is_boosted = False

                if self.player.shield_active:
                    if pg.time.get_ticks() - self.last_shield >= 10000:
                        self.player.shield_active = False

                if not self.is_game_active: 
                    pg.mixer.music.stop()




game = Game()
game.run()
