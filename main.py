import pygame as pg
from ui import HUD
from asset import Asset_manager, Player
from enemy import Enemy, Enemy_Soldier



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

        self.time = 0
        self.score = 0

        self.ammo = 30
        self.cur_weapon = 'Blaster'
        self.weapon_energy = 1.0

        self.asset_manager = Asset_manager('player_sprite.png')
        self.player = Player(self.win_w // 2, self.win_h - 300, self.asset_manager.data)

        self.all_sprite = pg.sprite.Group()

        self.enemy_bullet_group = pg.sprite.Group()

    def draw(self):
        pg.draw.rect(self.screen, (0, 0, 0), self.game_rect) 
        self.hud.draw(self.score, self.time, self.ammo, self.cur_weapon, self.weapon_energy)
        self.screen.blit(self.hud.surface, (0, 0))

        self.all_sprite.draw(self.screen)
        self.screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
        self.enemy_bullet_group.draw(self.screen)

        pg.display.flip()

    def spawn_enemy(self):
        new_enemy_common = Enemy('enemy4.png', 128, 128, self.win_w//2, -100, self.win_h)
        new_enemy_elite = Enemy_Soldier('enemy2.png', 180, 180, self.win_w//2, 0, self.game_rect.right, self.game_rect.left, 2000, self.enemy_bullet_group)
        new_enemy_fat =  Enemy('enemy5.png', 128, 128, self.win_w//2+200, -100, self.win_h, 2/3, 1.5, 2 )
        new_enemy_agile =  Enemy('enemy6.png', 128, 128, self.win_w//2-200, -100, self.win_h, 1.5, 2/3, 2/3 )
        self.all_sprite.add(new_enemy_common)
        self.all_sprite.add(new_enemy_elite)
        self.all_sprite.add(new_enemy_fat)
        self.all_sprite.add(new_enemy_agile)
        

    def run(self):
        game.spawn_enemy()

        while self.runnig:            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.runnig = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        self.player.toggle_shield()

            self.all_sprite.update()
            self.enemy_bullet_group.update()
            self.player.update()

            

            if self.player.rect.left < self.hud_area_w:
                self.player.rect.left = self.hud_area_w
            if self.player.rect.right > self.win_w:
                self.player.rect.right = self.win_w

            self.draw()
            self.clock.tick(self.FPS)


game = Game()
game.run()
