import pygame
import sys
import random

WIDTH = 1280
HEIGHT = 720
STARSPEED_BG = 1
STARSPEED_FG = 2

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (80,80,80)

pygame.init()

#set screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Fighter")
clock = pygame.time.Clock()

#images loading
ship_surf = pygame.image.load('pics/ships/playerShip1_blue_left.png').convert_alpha()
thruster_surf = pygame.image.load('pics/thrusters/fire09_left.png').convert_alpha()
noz_slow_surf = pygame.image.load('pics/thrusters/nozzle_slow.png').convert_alpha()
noz_down_surf = pygame.image.load('pics/thrusters/nozzle_down.png').convert_alpha()
noz_up_surf = pygame.image.load('pics/thrusters/nozzle_up.png').convert_alpha()
big_star_surf = pygame.image.load('pics/interstellar_obj/star2.png').convert_alpha()
big_star_surf = pygame.transform.scale(big_star_surf,(6,6)) # resizing


class Ships:
    def __init__(self,ship_surf,thruster_surf,noz_slow_surf,noz_down_surf,noz_up_surf):
        self.ship_surf = ship_surf
        self.thruster_surf = thruster_surf
        self.noz_slow_surf = noz_slow_surf
        self.noz_down_surf = noz_down_surf
        self.noz_up_surf = noz_up_surf

        # images rect
        self.ship_rect = self.ship_surf.get_rect()
        self.thruster_rect = self.thruster_surf.get_rect()
        self.noz_slow_rect = self.noz_slow_surf.get_rect()
        self.noz_down_rect = self.noz_down_surf.get_rect()
        self.noz_up_rect = self.noz_up_surf.get_rect()

        # ship position set on screen
        self.ship_rect.midleft = (30,HEIGHT//2)

        # thruster and nozzles position set to the ship
        self.thruster_rect.midright = (self.ship_rect.midleft[0],self.ship_rect.midleft[1])
        self.noz_slow_rect.midleft = (self.ship_rect.midright[0],self.ship_rect.midright[1])
        self.noz_down_rect.midbottom = (self.ship_rect.midtop[0],self.ship_rect.midtop[1])
        self.noz_up_rect.midtop = (self.ship_rect.midbottom[0],self.ship_rect.midbottom[1])

        # All ship object rect
        self.player_ship_rect = self.ship_rect.union(self.thruster_rect).union(self.noz_slow_rect).union(self.noz_down_rect).union(self.noz_up_rect)

    def draw_ship(self, screen, keys): # images display
        screen.blit(self.ship_surf, self.ship_rect)
        if keys[pygame.K_d]:
            screen.blit(self.thruster_surf,self.thruster_rect)
        if keys[pygame.K_a]:
            screen.blit(self.noz_slow_surf,self.noz_slow_rect)
        if keys[pygame.K_s]:
            screen.blit(self.noz_down_surf,self.noz_down_rect)
        if keys[pygame.K_w]:
            screen.blit(self.noz_up_surf,self.noz_up_rect)
        

    def move_ship(self, x, y): # image moving
        new_ship_rect = self.ship_rect.move(x,y) # position control reference
        
        # position check method
        if (30 <= new_ship_rect.left and new_ship_rect.right <= WIDTH-300 and 
            0 <= new_ship_rect.top and new_ship_rect.bottom <= HEIGHT):
            self.ship_rect.move_ip(x, y)
            self.thruster_rect.move_ip(x, y)
            self.noz_slow_rect.move_ip(x, y)
            self.noz_down_rect.move_ip(x, y)
            self.noz_up_rect.move_ip(x, y)
            self.player_ship_rect.move_ip(x, y)

class Stars:
    def __init__(self, color, x, y, size=1):
        self.color = color
        self.x = x
        self.y = y
        self.size = size
        self.speed = random.uniform(0.5, 1.5) # changeing speed

    def move_star (self, dx):
        self.x += dx*self.speed  # moving from right to left
        if self.x < 0:   # repositioning on right side
            self.x = WIDTH + random.randint(0,50)
            self.y = random.randint(0,HEIGHT)
    
    def draw_star(self, screen): # display stars
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
    
class StarBGLayer:
    def __init__(self, color, num_stars, speed, big_star_surf=None):
        self.color = color
        self.num_stars = num_stars
        self.speed = speed
        self.stars = []
        self.big_star_surf = big_star_surf
    
        for _ in range(num_stars): # random position stars creating
            x = random.randint(0,WIDTH)
            y = random.randint(0,HEIGHT)
            if self.big_star_surf and random.random() < 0.5: # 10% chance big_star_surf
                self.stars.append(Stars(self.color, x, y))
            else:
                self.stars.append(Stars(self.color, x, y, size=2))
    
    def update(self): # background refresh
        for star in self.stars:
            star.move_star(-self.speed)
    
    def draw_starbg(self, screen):
        for star in self.stars:
            if self.big_star_surf and star.size > 1:
                screen.blit(self.big_star_surf,(star.x, star.y))
            else:
                star.draw_star(screen)

# Creating background layers
back_layer = StarBGLayer(GREY, 150, 0.5)
front_layer = StarBGLayer(WHITE, 50, 1, big_star_surf)

# Create ship object
ship = Ships(ship_surf,thruster_surf,noz_slow_surf,noz_down_surf,noz_up_surf)

# Main cycle
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Keyboard control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        ship.move_ship(5,0)
    if keys[pygame.K_a]:
        ship.move_ship(-5,0)
    if keys[pygame.K_w]:
        ship.move_ship(0,-5)
    if keys[pygame.K_s]:
        ship.move_ship(0,5)

    # Clear screen
    screen.fill(BLACK)
    
    # display and update star bg layers
    back_layer.update()
    back_layer.draw_starbg(screen)
    front_layer.update()
    front_layer.draw_starbg(screen)
    
    # display ship image
    ship.draw_ship(screen,keys)

    #update screen
    pygame.display.update()

    # set FPS
    clock.tick(60)

pygame.quit()
sys.exit()