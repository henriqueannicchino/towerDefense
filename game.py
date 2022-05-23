#continue from 11:28:00
import pygame
import os
from enemies.scorpion import Scorpion
from enemies.club import Club
from enemies.wizard import Wizard
from towers.archerTower import ArcherTowerLong, ArcherTowerShort
from towers.supportTower import DamageTower, RangeTower
from menu.menu import VerticalMenu, PlayPauseButton
import time
import random
pygame.font.init()
pygame.init()

path = [(-10, 234), (19, 234), (177, 235), (282, 293), (526, 290), (607, 217), (641, 105), (717, 57), (796, 83), (855, 222), (973, 284), (1046, 366), (1040, 458), (894, 492), (740, 504), (580, 542), (148, 541), (10, 442), (-20, 335), (-75, 305), (-100, 345)]

lives_img = pygame.image.load(os.path.join("game_assets","heart.png"))
star_img = pygame.image.load(os.path.join("game_assets/menu","star.png"))
side_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu","side.png")), (120, 500))

buy_archer = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","buy_archer.jpg")), (50, 50))
buy_archer_2 = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","buy_archer_2.jpg")), (50, 50))
buy_damage = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","buy_damage.png")), (50, 50))
buy_range = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","buy_range.png")), (50, 50))

play_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu","button_play.png")), (75, 75))
pause_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu","button_pause.png")), (75, 75))

sound_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","button_sound.png")), (75, 75))
sound_btn_off = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","button_sound_off.png")), (75, 75))

wave_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu","menu.png")), (225, 70))

attack_tower_names = ["archer", "archer2"]
support_tower_names = ["range", "damage"]

#load music
pygame.mixer.music.load(os.path.join("game_assets", "music.mp3"))

#waves are in form
#frequency of enemies
#(#scorpions, #wizards, #clubs)
waves = [
    [20, 0, 0],
    [50, 0, 0],
    [100, 0, 0],
    [0, 20, 0],
    [0, 50, 0],
    [0, 100, 0],
    [20, 100, 0],
    [50, 100, 0],
    [100, 100, 0],
    [0, 0, 50],
    [20, 0, 100],
    [20, 0, 150],
    [200, 100, 200],
]

class Game:
    def __init__(self, win):
        self.width = 1350
        self.height = 700
        self.win = win
        self.enemys = []
        self.attack_towers = []
        self.support_towers = []
        self.lives = 10
        self.money = 2000
        self.bg = pygame.image.load(os.path.join("game_assets", "bg.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.timer = time.time()
        self.life_font = pygame.font.SysFont("comicsans", 40)
        self.selected_tower = None
        self.menu = VerticalMenu(self.width - side_img.get_width() + 70, 250, side_img)
        self.menu.add_btn(buy_archer_2, "buy_archer_2", 500)
        self.menu.add_btn(buy_archer, "buy_archer", 750)
        self.menu.add_btn(buy_damage, "buy_damage", 1000)
        self.menu.add_btn(buy_range, "buy_range", 1000)
        self.moving_object = None
        self.wave = 0
        self.current_wave = waves[self.wave][:]
        self.pause = True
        self.music_on = True
        self.playPauseButton = PlayPauseButton(play_btn, pause_btn, 10, self.height - 85)
        self.soundButton = PlayPauseButton(sound_btn, sound_btn_off, 90, self.height - 85)

    def gen_enemies(self):
        """
        generate the next enemy or enemies to show
        :return: enemy
        """
        if sum(self.current_wave) == 0:
            if len(self.enemys) == 0:
                self.wave += 1
                self.current_wave = waves[self.wave]
                self.pause = True
                self.playPauseButton.paused = self.pause
        else:
            wave_enemies = [Scorpion(), Wizard(), Club()]
            for x in range(len(self.current_wave)):
                if self.current_wave[x] != 0:
                    self.enemys.append(wave_enemies[x])
                    self.current_wave[x] = self.current_wave[x] -1
                    break
        
    def run(self):
        pygame.mixer.music.play(loops=-1)
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)

            if self.pause ==  False:
                #gen monsters
                if time.time() - self.timer >= random.randrange(1,6)/3:
                    self.timer = time.time()
                    self.gen_enemies()

            pos = pygame.mouse.get_pos()

            #check for moving object
            if self.moving_object:
                self.moving_object.move(pos[0], pos[1])
                tower_list = self.attack_towers[:] + self.support_towers[:]
                collide = False
                for tower in tower_list:
                    if tower.collide(self.moving_object):
                        collide = True
                        tower.place_color = (255,0,0,100)
                        self.moving_object.place_color = (255,0,0,100)
                    else:
                        tower.place_color = (0,255,0,100)
                        if not collide:
                            self.moving_object.place_color = (0,255,0,100)

            #main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False


                if event.type == pygame.MOUSEBUTTONUP:
                    #if you're moving an object and click
                    if self.moving_object:
                        not_allowed =  False
                        tower_list = self.attack_towers[:] + self.support_towers[:]
                        for tower in tower_list:
                            if tower.collide(self.moving_object):
                                not_allowed = True

                        if not not_allowed and self.point_to_line(self.moving_object):
                            if self.moving_object.name in attack_tower_names:
                                self.attack_towers.append(self.moving_object)
                            elif self.moving_object.name in support_tower_names:
                                self.support_towers.append(self.moving_object)

                            self.moving_object.moving = False
                            self.moving_object = None
                            
                    else:
                        #check for play or pause
                        if self.playPauseButton.click(pos[0], pos[1]):
                            self.pause = not(self.pause)
                            self.playPauseButton.paused = self.pause

                        if self.soundButton.click(pos[0], pos[1]):
                            self.music_on = not(self.music_on)
                            self.soundButton.paused = self.music_on
                            if self.music_on:
                                pygame.mixer.music.unpause()
                            else:
                                pygame.mixer.music.pause()
                        
                        #look if you click on side menu
                        side_menu_button = self.menu.get_clicked(pos[0], pos[1])
                        if side_menu_button:
                            cost =  self.menu.get_item_cost(side_menu_button)
                            if self.money >= cost:
                                self.money -= cost
                                self.add_tower(side_menu_button)

                        #look if you clicked on attack tower or support tower
                        btn_clicked = None
                        if self.selected_tower:
                            btn_clicked = self.selected_tower.menu.get_clicked(pos[0], pos[1])
                            if btn_clicked:
                                if btn_clicked == "Upgrade":
                                    cost = self.selected_tower.get_upgrade_cost()
                                    if self.money >= cost:
                                        self.money -= cost
                                        self.selected_tower.upgrade()
                                        
                        if not(btn_clicked):
                            for tw in self.attack_towers:
                                if tw.click(pos[0], pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False
                            
                            #look if you clicked on support tower
                            for tw in self.support_towers:
                                if tw.click(pos[0], pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False   
            # loop through enemies
            if not self.pause:
                to_del = []
                for en in self.enemys:
                    en.move()
                    if en.x < -15:
                        to_del.append(en)

                # delete all enemies off the screen
                for d in to_del:
                    self.lives -= 1
                    self.enemys.remove(d)

                #loop through attack_towers
                for tw in self.attack_towers:
                    self.money += tw.attack(self.enemys)

                #loop through support_towers
                for tw in self.support_towers:
                    tw.support(self.attack_towers)

                #if you lose
                if self.lives <= 0:
                    print("You Lose")
                    run = False
            
            self.draw()


    def point_to_line(self, tower):
        """
        returns if you can place tower based on distance from path
        :param tower: Tower
        :return: Bool
        """
        #find two closest points
        """
        closest = []
        for point in path:
            dis = math.sqrt((tower.x - point[0])**2 + (tower.y - point[1])**2)
            closest.append([dis, point])

        closest.sort(key=lambda x: x[0])

        x = closest[0][1]
        y = closest[1][1]

        #Calculate the coefficients. This line answers the initial question.
        coefficients = np.polyfit(x, y, 1)

        a = coefficients[0]
        b = coefficients[1]

        c = a*x[0] + b*x[1]

        dis = abs((a * x[0] + b * x[1])) / (math.sqrt((a**2) + (b**2))
        """
        return True

    def draw(self):
        self.win.blit(self.bg, (0,0))

        #draw placement rings
        if self.moving_object:
            for tower in self.attack_towers:
                tower.draw_placement(self.win)

            for tower in self.support_towers:
                tower.draw_placement(self.win)

            self.moving_object.draw_placement(self.win)

        # draw attack_towers
        for tw in self.attack_towers:
            tw.draw(self.win)

        # draw support_towers
        for tw in self.support_towers:
            tw.draw(self.win)
        
        # draw enemies
        for en in self.enemys:
            en.draw(self.win)

        #redraw selected tower
        if self.selected_tower:
            self.selected_tower.draw(self.win)
        
        #draw moving object
        if self.moving_object:
            self.moving_object.draw(self.win)

        #draw menu
        self.menu.draw(self.win)

        #draw play and pause buttons
        self.playPauseButton.draw(self.win)

        #draw music toggle button
        self.soundButton.draw(self.win)

        #draw lives
        text = self.life_font.render(str(self.lives), 1, (255,255,255))
        life = pygame.transform.scale(lives_img,(50,50))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() - 10, 0))
        self.win.blit(life, (start_x, 10))

        #draw money
        text = self.life_font.render(str(self.money), 1, (255,255,255))
        money = pygame.transform.scale(star_img,(50,50))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() - 10, 65))
        self.win.blit(money, (start_x, 75))

        #draw wave
        self.win.blit(wave_bg, (10,10))
        text = self.life_font.render("Wave #" + str(self.wave), 1, (255,255,255))
        self.win.blit(text, (10 + wave_bg.get_width()/2 - text.get_width()/2, 15))
            
        pygame.display.update()

    def add_tower(self, name):
        x, y = pygame.mouse.get_pos()
        name_list = ["buy_archer", "buy_archer_2", "buy_damage", "buy_range"]
        object_list = [ArcherTowerLong(x,y), ArcherTowerShort(x,y), DamageTower(x,y), RangeTower(x,y)]

        try:
            obj = object_list[name_list.index(name)]
            self.moving_object = obj
            obj.moving = True
        except Exception as e:
            print(str(e) + "NOT VALID NAME")

