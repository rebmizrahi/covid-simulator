import pygame, sys
import numpy as np
import matplotlib.pyplot as plt

black = (0, 0, 0)
white = (255, 255, 255)
red = (255,110,180)
green = (70,250,154)
blue = (100,149,237)
purple = (159,121,238)
background = white

#SET UP SIR MODEL VARIABLES

#variables
    #MODEL 1: no social distancing -- num susc = 198, num_quarantined = 0, num_inf = 2
    #MODEL 2: minor social distancing -- num susc = 148, num_quarantined = 50, num_inf = 2
    #MODEL 3: moderate social distancing -- num susc = 50, num_quarantined = 148, num_inf = 2
    #MODEL 4: extensive social distancing -- num susc = 20, num_quarantined = 178, num_inf = 2

num_susc = 148
num_inf = 2
num_quarantined = 50
recovery_time = 8000

class dot(pygame.sprite.Sprite):

    def __init__(self,x,y,width,height,colour=black,radius=5,velocity=[0,0],randomize=False):
        super().__init__()

        #MAKE DOT - person representation
        self.width = width
        self.height = height
        
        self.image = pygame.Surface([radius * 2, radius * 2])
        self.image.fill(background)
        pygame.draw.circle(self.image, colour, (radius,radius), radius)
        self.time = 0

        self.rect = self.image.get_rect()
        self.pos = np.array([x, y], dtype=np.float64)
        self.vel = np.asarray(velocity, dtype=np.float64)


    def update(self):
        #DOT MOVEMENT
        self.pos += self.vel
        x,y = self.pos

        #loop screen
        if x < 0:
            self.pos[0] = self.width
            x = self.width
        if y < 0 :
            self.pos[1] = self.height
            y = self.height
        if x > self.width:
            self.pos[0] = 0
            x = 0
        if y > self.height:
            self.pos[1] = 0
            y = 0
            
        self.rect.x = int(x)
        self.rect.y = int(y)


width = 800
height = 480
 
    
class simulation:

    def __init__(self, width=800, height=480):
        self.width = width
        self.height = height

        self.container = pygame.sprite.Group()
        self.susc_container = pygame.sprite.Group()
        self.inf_container = pygame.sprite.Group()
        self.quarantined_container = pygame.sprite.Group()
        self.recovered_container = pygame.sprite.Group()
    
    def start(self, randomize=False):
        pygame.init()
        font = pygame.font.SysFont(None, 25)

        window = pygame.display.set_mode([self.width, self.height])
        #pygame.time.delay(10000)

        #ADD SUSCEPTIBLE PEOPLE TO CONTAINER
        for i in range(num_susc):
            x = np.random.randint(0, (width+1))
            y = np.random.randint(0, (height+1))
            #2 random numbers between -2,2
            vel = 2*(np.random.rand(2) * 2 - 1)

            susc_person = dot(x,y,width,height,colour=green,velocity=vel)
            self.container.add(susc_person)
            self.susc_container.add(susc_person)

        #ADD QUARANTINED - FROZEN DOTS - TO CONTAINER
        for i in range(num_quarantined):
            x = np.random.randint(0, (width+1))
            y = np.random.randint(0, (height+1))

            vel = 0

            quarantined_person = dot(x,y,width,height,colour=green,velocity=vel)
            self.container.add(quarantined_person)
            self.quarantined_container.add(quarantined_person)
    
        #ADD INFECTED PERSON(S) TO CONTAINER
        for i in range(num_inf):
            x = np.random.randint(0, (width+1))
            y = np.random.randint(0, (height+1))
            #to ensure the first infected people aren't still (with vel = 0)
            vel = [3,3]

            inf_person = dot(x,y,width,height,colour=purple,velocity=vel)
            self.container.add(inf_person)
            self.inf_container.add(inf_person)
            self.time = pygame.time.get_ticks()

        T=2000
        clock = pygame.time.Clock()
        for i in range(T):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()        
            self.container.update()
            window.fill(background)
            
        #CHECK FOR COLLISIONS
            #kill susceptible
            collisions_1 = pygame.sprite.groupcollide(self.susc_container,self.inf_container,True,False)
            collisions_2 = pygame.sprite.groupcollide(self.quarantined_container,self.inf_container,True,False)
            #replace with infected
            for person in collisions_1:
                x = person.pos[0]
                y = person.pos[1]
                vel = person.vel
                original_vel = person.vel
                new_person = dot(x,y,width,height,colour=purple,radius=5,velocity=vel)
                self.inf_container.add(new_person)
                self.container.add(new_person)
                new_person.time = pygame.time.get_ticks()
            for person in collisions_2:
                x = person.pos[0]
                y = person.pos[1]
                vel = person.vel
                original_vel = person.vel
                new_person = dot(x,y,width,height,colour=purple,radius=5,velocity=vel)
                self.inf_container.add(new_person)
                self.container.add(new_person)
                new_person.time = pygame.time.get_ticks()

            for person in self.inf_container:
                #slow down
                if ((pygame.time.get_ticks() - person.time) > recovery_time*0.75) and (pygame.time.get_ticks() - person.time) < recovery_time:
                    #either keep same velocity or slow to stop
                    person.vel = (person.vel)/(1 + np.random.randint(0,2))
                #recover
                elif (pygame.time.get_ticks() - person.time) > recovery_time:
                    self.inf_container.remove(person)
                    pygame.sprite.Sprite.kill(person)
                    x = person.pos[0]
                    y = person.pos[1]
                    vel = 2*(np.random.rand(2) * 2 - 1)
                    new_recovered_person = dot(x,y,width,height,colour=red,radius=5,velocity=vel)
                    self.recovered_container.add(new_recovered_person)
                    self.container.add(new_recovered_person)

            #SHOW STATS
            total_num_susc = len(self.susc_container) + len(self.quarantined_container)
            total_stats = font.render(("Population size: " + str(len(self.container))),True,black) 
            infected_stats = font.render(("Number of infected: " + str(len(self.inf_container))),True,black) 
            susc_stats = font.render(("Number of susceptible: " + str(total_num_susc)),True,black) 
            recovered_stats = font.render(("Number of recovered: " + str(len(self.recovered_container))),True,black) 

            window.blit(total_stats,(int(300),int(10)))
            window.blit(infected_stats,(int(300),int(40)))
            window.blit(susc_stats,(int(300),int(70)))
            window.blit(recovered_stats,(int(300),int(100)))

            self.container.draw(window)
            pygame.display.flip()
            clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    covid = simulation(800, 480)

    covid.start()
