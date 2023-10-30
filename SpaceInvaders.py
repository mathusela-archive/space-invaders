import pygame
from pygame.locals import *
pygame.init()

pygame.display.set_caption("Space Invaders")
screen = pygame.display.set_mode((600,700))

global invaderMove
global step
global invaderDown
global invaderAnimation
global invaderDeathCount
invaderDeathCount = 0
invaderAnimation = 0
invaderDown = False
step = 0
invaderMove = "R"

invaderMove1 = pygame.mixer.Sound("./assets/sounds/invaderMove1.wav")
invaderMove2 = pygame.mixer.Sound("./assets/sounds/invaderMove2.wav")
invaderDeath = pygame.mixer.Sound("./assets/sounds/invaderDeath.wav")
playerShoot = pygame.mixer.Sound("./assets/sounds/playerShoot.wav")

class shot(pygame.sprite.Sprite):
    def __init__(self):
        self.move = False
        super(shot, self).__init__()
        self.surf = pygame.Surface((3,20))
        self.surf.fill((175,175,255))
        self.rect = self.surf.get_rect()

    def update(self, pressedKeys):
        if pressedKeys[K_SPACE]:
            if self.move == False:
                playerShoot.play()
                self.rect.center = (player.rect.center)
                self.move = True
        if self.rect.top == 0:
            self.move = False
            self.rect.center = (600,700)
        if self.move == True:
            self.rect.move_ip(0, -2.5)

    def collide(self):
        self.move = False
        self.rect.center = (500,700)

class player(pygame.sprite.Sprite):
    def __init__(self):
        super(player, self).__init__()
        self.image = pygame.image.load("./assets/textures/player.png")
        self.rect = self.image.get_rect()

    def update(self, pressedKeys):
        if pressedKeys[K_a]:
            self.rect.move_ip(-1,0)
        if pressedKeys[K_d]:
            self.rect.move_ip(1,0)

class invader(pygame.sprite.Sprite):
    def __init__(self):
        super(invader, self).__init__()
        self.image1 = pygame.image.load("./assets/textures/invader1.png")
        self.image2 = pygame.image.load("./assets/textures/invader2.png")
        self.death = pygame.image.load("./assets/textures/invaderDeath.png")
        self.rect = self.image1.get_rect()
        self.show = True
        self.dead = False

    def update(self):
        global invaderDeathCount

        if self.rect.colliderect(shot.rect):
            invaderDeath.play()
            shot.collide()
            if self.dead == False:
                invaderDeathCount += 1
            self.dead = True

        if step == 0:
            if self.dead == True:
                self.show = False
                self.rect.center = (300,700)

        global invaderMove
        global invaderDown

        if noOfInv-invaderDeathCount > 0:
            speed = ((10/(noOfInv-invaderDeathCount))*4)+18.18
        else:
            speed = 0

        print(speed)

        if invaderDown == True:
            self.rect.move_ip(0,25)

        if invaderMove == "R":
            if step == 0 and self.show == True:
                self.rect.move_ip(speed,0)

        if invaderMove == "L":
            if step == 0 and self.show == True:
                self.rect.move_ip(-speed,0)

    def side(self):
        global invaderMove
        global invaderDown

        if step == 110:
            if self.rect.right >= 575:
                invaderMove = "L"
                invaderDown = True
        if step == 110:
            if self.rect.left <= 25:
                invaderMove = "R"
                invaderDown = True

    def downReset(self):
        global invaderDown
        invaderDown = False

    def draw(self):
        global invaderAnimation
        if self.show == True:
            if self.dead == True:
                screen.blit(self.death,self.rect)
            else:
                if invaderAnimation == 0:
                    screen.blit(self.image1,self.rect)
                if invaderAnimation == 1:
                    screen.blit(self.image2,self.rect)

player = player()
width = 9
hight = 5
noOfInv = width*hight
invaders = []
for member in range(noOfInv):
    member = invader()
    invaders.append(member)
shot = shot()


player.rect.center = (300,650)
for l in range(1,hight+1):
    for i in range(width):
        invaders[(width*(l-1))+i].rect.center = (25+i*55,25+l*50)
shot.rect.center = (600,700)

screenRect = screen.get_rect()
clock = pygame.time.Clock()

gameloop = True

while gameloop == True:
    player.rect.clamp_ip(screenRect)
    for i in range(noOfInv):
        invaders[i].rect.clamp_ip(screenRect)
    shot.rect.clamp_ip(screenRect)

    screen.fill((0,0,0))
    if shot.move == True:
        screen.blit(shot.surf,shot.rect)
    screen.blit(player.image, player.rect)
    if step == 0:
        if invaderAnimation == 0:
            invaderAnimation = 1
        elif invaderAnimation == 1:
            invaderAnimation = 0

    if invaderDeathCount != noOfInv:
        if step == 0:
            if invaderAnimation == 0:
                invaderMove1.play()
            elif invaderAnimation == 1:
                invaderMove2.play()

    for i in range(noOfInv):
        invaders[i].draw()

    pygame.display.flip()

    pressedKeys = pygame.key.get_pressed()
    player.update(pressedKeys)
    shot.update(pressedKeys)
    for i in range(noOfInv):
        invaders[i].update()
    step += 1
    if step == 220:
        step = 0
    for i in range(noOfInv):
        invaders[i].downReset()
    for i in range(noOfInv):
        invaders[i].side()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                gameloop = False
                pygame.quit()
        elif event.type == QUIT:
            gameloop = False
            pygame.quit()

    clock.tick(300)
