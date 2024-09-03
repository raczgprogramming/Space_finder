import pygame
import sys
import random

WIDTH = 1280
HEIGHT = 720

pygame.init()

#set screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Fighter")
clock = pygame.time.Clock()

#images loading
ship_surf = pygame.image.load('pics/ships/playerShip1_blue_left.png').convert_alpha()
thruster_surf = pygame.image.load('pics/thrusters/fire09_left.png').convert_alpha()
noz_slow_surf = pygame.image.load('pics/thrusters/nozzle_slow.png').convert_alpha()
noz_down_surf = pygame.image.load('pics/thrusters/nozzle_down.png').convert_alpha()
noz_up_surf = pygame.image.load('pics/thrusters/nozzle_up.png').convert_alpha()

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

    def draw(self, screen): # images display
        screen.blit(self.ship_surf, self.ship_rect)
        if keys[pygame.K_d]:
            screen.blit(self.thruster_surf,self.thruster_rect)
        if keys[pygame.K_a]:
            screen.blit(self.noz_slow_surf,self.noz_slow_rect)
        if keys[pygame.K_s]:
            screen.blit(self.noz_down_surf,self.noz_down_rect)
        if keys[pygame.K_w]:
            screen.blit(self.noz_up_surf,self.noz_up_rect)
        

    def move(self, x, y): # image moving
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
        ship.move(1,0)
    if keys[pygame.K_a]:
        ship.move(-1,0)
    if keys[pygame.K_w]:
        ship.move(0,-1)
    if keys[pygame.K_s]:
        ship.move(0,1)

    # Clear screen
    screen.fill((0,0,0))
    # display image
    ship.draw(screen)

    #update screen
    pygame.display.update()

    # set FPS
    clock.tick(60)

pygame.quit()
sys.exit()