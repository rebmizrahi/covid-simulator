import pygame
import numpy as np
import random

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
pink = (255,110,180)
green = (70,250,154)
blue = (100,149,237)
purple = (159,121,238)
win_width = 800
win_height = 600
WIN = pygame.display.set_mode((win_width,win_height))
background = white
num_susc = 35
num_inf = 2
title_font = pygame.font.SysFont("comicsans", 60)


class Person(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,colour=blue,radius=5):
        super().__init__()

        self.width = width
        self.height = height
        
        self.image = pygame.Surface([radius * 2, radius * 2])
        self.image.fill(background)
        pygame.draw.circle(self.image, colour, (radius,radius), radius)

        self.rect = self.image.get_rect()
        self.pos_x = x
        self.pos_y = y
        self.vel_x = 0
        self.vel_y = 0

    def update(self):
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        if self.pos_x < 0:
            self.pos_x = win_width
            self.rect.x = win_width
        if self.pos_y < 0 :
            self.pos_y = win_height
            self.rect.y = win_height
        if self.pos_x > win_width:
            self.pos_x = 0
            self.rect.x = 0
        if self.pos_y > win_height:
            self.pos_y = 0
            self.rect.y =0
            
        self.rect.x =int(self.pos_x)
        self.rect.y =int(self.pos_y)
        
class Player(Person):
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

            
pygame.init()

win = pygame.display.set_mode([win_width,win_height])

list_inf = pygame.sprite.Group()
list_susc = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle()
list_all_sprites = pygame.sprite.Group()

def main():

    for i in range(num_susc):
        x = np.random.randint(0, win_width)
        y = np.random.randint(0, win_height)
        susc_person = Person(x,y,15,15)
        susc_person.vel_x = random.randrange(-2,3)
        susc_person.vel_y = random.randrange(-2,3)
       
        list_susc.add(susc_person)
        list_all_sprites.add(susc_person)
        
    for i in range(num_inf):
        x = np.random.randint(0, win_width)
        y = np.random.randint(0, win_height)
        inf_person = Person(x,y,10,10,colour=green)
        inf_person.vel_x = random.randrange(-2,3)
        inf_person.vel_y = random.randrange(-2,3)
        
        list_inf.add(inf_person)
        list_all_sprites.add(inf_person)

        
    x = np.random.randint(0, (win_width))
    y = np.random.randint(0, (win_height))
    player = Player(x,y,10,10,colour=pink)
    list_all_sprites.add(player)
    player_group.add(player)

    clock = pygame.time.Clock()

    run = True
    start = pygame.time.get_ticks()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
        win.fill(background)
        list_inf.update()
        list_susc.update()
        list_all_sprites.update()
        
        collisions = pygame.sprite.groupcollide(list_susc,list_inf, True, False)             
        for person in collisions:
            x = person.pos_x
            y = person.pos_y
            new_person = Person(x,y,10,10,colour=green,radius=5)
            new_person.vel_x = person.vel_x
            new_person.vel_y = person.vel_y
            list_inf.add(new_person)
            list_all_sprites.add(new_person)
            
        now = pygame.time.get_ticks() 
        if (now - start) > 2000:
            start = now
            x = np.random.randint(0, win_width)
            y = np.random.randint(0, win_height)
            new_person = Person(x,y,10,10,radius=5)
            new_person.vel_x = random.randrange(-2,3)
            new_person.vel_y = random.randrange(-2,3)
            list_susc.add(new_person)
            list_all_sprites.add(new_person)

        
        game_over = pygame.sprite.groupcollide(player_group,list_inf, True, False)
        if len(game_over) > 0:
            print(str(len(list_all_sprites)) + " sprites")
            print(str(pygame.time.get_ticks()/1000) + " seconds")
            pygame.time.delay(1000)
            lost_screen = pygame.Surface([win_width,win_height])
            lost_screen.fill(background)
            WIN.blit(lost_screen, (0,0))
            title_label = title_font.render("GAME OVER",True,black)
            title_label2 = title_font.render(("Score: " + str(int(pygame.time.get_ticks())/1000)),True,black)

            WIN.blit(title_label, (int(win_width/2 - title_label.get_width()/2),30))
            WIN.blit(title_label2, (int(win_width/2 - title_label.get_width()/2),80))

            pygame.display.update()

            run = False
            pygame.time.delay(1000)
            pygame.quit()
            
        
        list_all_sprites.draw(win)
        list_susc.draw(win)
        list_inf.draw(win)

        clock.tick(60)
        pygame.display.update()
        
def start_screen():
    run = True
    while run:     
        image = pygame.Surface([win_width,win_height])
        image.fill(background)
        WIN.blit(image, (0,0))
        title_label = title_font.render("Press the mouse to begin...",True,black)
        WIN.blit(title_label, (int(win_width/2 - title_label.get_width()/2), int(250)))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    
    pygame.quit()

start_screen()

