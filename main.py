import pygame
import random

from pygame.locals import(
    K_w,
    K_a,
    K_s,
    K_d,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    K_RETURN,
    QUIT,
)

pygame.init()

#Setup screen

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((255, 255, 255))


#Import variables

clock = pygame.time.Clock()


#Classes for sprites

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((0,0, 255))
        self.rect = self.surf.get_rect(center = (x, y))

    def update(self, pressed_keys):
        if pressed_keys[K_a]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_d]:
            self.rect.move_ip(5, 0)
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -5)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0


class Fruit(pygame.sprite.Sprite):
    def __init__(self):
        super(Fruit, self).__init__()
        self.surf = pygame.Surface((5,5))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(
            center= (
            random.randint(0, SCREEN_WIDTH), 0,
            )
        )

    def update(self):
        self.rect.move_ip(0, 5)

        if self.rect.centery == SCREEN_HEIGHT:
            self.kill()
        


#Custom Events

ADDFRUIT = pygame.USEREVENT + 1
pygame.time.set_timer(ADDFRUIT, 250)


#initialize player

player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT)

#Creating Sprite Groups

fruits = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

#adding player to all_sprites group

all_sprites.add(player)


#Game Loop

running = True

while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == ADDFRUIT:
            new_fruit = Fruit()
            fruits.add(new_fruit)
            all_sprites.add(new_fruit)

    

    #update player
    
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    #update fruit

    fruits.update()

    #collision control

    if pygame.sprite.spritecollideany(player, fruits):
        player.kill()
        running = False
    
    screen.fill((255, 255, 255))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    pygame.display.flip()

    clock.tick(30)
