import pygame
import random
from pygame.locals import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH,SCREEN_HEIGHT ))
SPEED = 14
GRAVITY = 2
GAME_SPEED = 6
GROUD_WIDTH = 2*SCREEN_WIDTH
GROUD_HEIGHT = 100
PIPE_WIDTH = 120
PIPE_HEIGHT = 500
PIPE_GAP = 200


class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load("assets/sprites/bluebird-upflap.png").convert_alpha(),
                       pygame.image.load("assets/sprites/bluebird-midflap.png").convert_alpha(),
                       pygame.image.load("assets/sprites/bluebird-downflap.png").convert_alpha()]
        
        self.speed = SPEED

        self.current_image = 0
        

        self.image = pygame.image.load("assets/sprites/bluebird-midflap.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect[1] = SCREEN_HEIGHT / 2
        self.rect[0] = SCREEN_WIDTH / 2
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

        self.speed += GRAVITY

        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets\sprites\pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH,PIPE_HEIGHT))
        
        self.rect= self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED
        
class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("assets/sprites/base.png")
        self.image = pygame.transform.scale(self.image, (GROUD_WIDTH, GROUD_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] =  xpos
        self.rect[1] = SCREEN_HEIGHT - GROUD_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED  
        pass

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(150, 550)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT ))

#grupos
bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUD_WIDTH*i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])


clock = pygame.time.Clock()

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()
    
    screen.blit(BACKGROUND, (0,0))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_groud = Ground(GROUD_WIDTH - 10)
        ground_group.add(new_groud)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])
        
        pipes = get_random_pipes((SCREEN_WIDTH * 2)-100)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])
    
    bird_group.update()
    ground_group.update()
    pipe_group.update()

    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)
    

    if pygame.sprite.groupcollide(bird_group, ground_group, False, False,  pygame.sprite.collide_mask):
        break

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False,  pygame.sprite.collide_mask):
        
        break

    pygame.display.update()

