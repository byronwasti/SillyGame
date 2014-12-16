import pygame, sys
import random
from pygame.locals import *
from pygame.sprite import Sprite
#import itertools

pygame.init()
pygame.font.init()

fpsClock = pygame.time.Clock()
screen = [1200,600]
font = pygame.font.SysFont("ubuntumono",screen[0]/8)
w = pygame.display.set_mode(screen)
#pygame.display.toggle_fullscreen()

ian = pygame.image.load('IanFace.png')
ian = pygame.transform.scale(ian, (100,120))

violin = pygame.image.load('violin.png')
violin = pygame.transform.scale(violin,(120,60))

bicycle = pygame.image.load('bicycle.png')
bicycle_rain = pygame.transform.scale(bicycle,(120,60))
bicycle = pygame.transform.scale(bicycle,(150,80))

keenan = pygame.image.load('keenan.png')
keenan_pic = pygame.transform.scale(keenan,(200,260))

puzzle = pygame.image.load('puzzle.png')
puzzle = pygame.transform.scale(puzzle,screen)

chicken = pygame.image.load('chicken.png')
chicken = pygame.transform.scale(chicken,(200,100))

bananasub = pygame.image.load('bananasub.png')
bananasub = pygame.transform.scale(bananasub,(200,100))

emu = pygame.image.load('emu.png')
emu = pygame.transform.scale(emu,(600,600))

spaceship = pygame.image.load('spaceship.png')
spaceship = pygame.transform.scale(spaceship,(100,100))

image_lib = { 0: ian, 1: violin, 2: bicycle, 3: keenan_pic, 4: chicken, 5: bananasub, 6: emu, 7: spaceship }

red = pygame.Color(255,0,0)
green = pygame.Color(0,100,0)
blue = pygame.Color(0,0,200)
white = pygame.Color(200,200,200)
black = pygame.Color(000,000,000)

tint_dict = { 0:red, 1: green, 2: blue, 3: blue, 4: red, 5:green}
tint_surface = pygame.Surface(screen)
tint_surface.set_alpha(100)
tinter = 0
tint_timer = 10
make_brick = 0
make_keenan = 0
score = 0
score_reset = False
score_old = 0
keenan_rotate = 50
game = True
game_cont = False
win = False
chicken_text = 10
start_seq = True

emu_timer = 50

class object_class:
    def __init__(self):
        self.pos = (0,0)
    def draw(self):
        w.blit( image_lib[self.image], self.pos)

class brick_class:
    def __init__(self, color):
        self.color = color
        self.dimen = [40,screen[1]]
        self.center = random.randrange(100,screen[1]-100)
        self.pos1 = [screen[0], self.center +100]
        self.pos2 = [screen[0], self.center - screen[1]- 100 ]

    def draw(self):
        pygame.draw.rect(w,self.color,self.pos1 + self.dimen)
        pygame.draw.rect(w,self.color,self.pos2 + self.dimen)

    def move(self):
        self.pos1[0] -= 10
        self.pos2[0] -= 10
        if self.pos1[0] < 0:
            return 1
        else: 
            return 0


class ian_class(object_class):
    def __init__(self, body_color, image ):

        self.pos_init = [200,screen[1]-200]
        self.pos = [200,screen[1]-200]
        self.image = image
        self.jump_check = 0
        
    def check_collide(self, center, xdim):
        if not center - 50 < self.pos[1]+60 < center +50 and xdim-1 < self.pos[0] < xdim +10:
            return False
        else: return True

    def check_keenan(self, pos):
        if pos[0] - 10 < self.pos[0] < pos[0] +10 and pos[1] - 10 < self.pos[0] < pos[0] +10:
            return False
        return True
    def move(self, key_in):
        pass 
    def jump(self):
        self.pos[1] -= 10 
        self.jump_check -=1

    def key(self):
        if event.key == K_SPACE and self.pos[1] > 0:
            self.jump_check = 10
           

class keenan_class(object_class):
    def __init__(self,body_color,image):
        self.pos = [screen[0] + random.randrange(-100,100),0]
        self.image = image
        self.updown = 1
    def bobble(self):
        if self.updown == 1:
            self.pos[1] -= 10
            if self.pos[1] <-10: self.updown = 0 
        else:
            self.pos[1] += 10
            if self.pos[1] > screen[1] - 300: self.updown = 1
    def move(self):
        self.pos[0] -= 5
        if self.pos[0] < 0: self.pos[0] = screen[0]

    def collide(self,pos):
        #if pos[0] -1 < self.pos[0] < pos[0] + 100 and pos[1] - 100 < self.pos[1] < pos[1] + 10:
        if self.pos[0] <= pos[0] + 120 <= self.pos[0] + 200 and self.pos[1] <= pos[1] + 30 <= self.pos[1] + 260:
            return 1
        else: return 0

class violin_class(object_class):
    def __init__(self, image):
        self.pos = [-100,-100]
        self.image = image
        self.firing = 0
    def key(self, pos):
        if event.key == K_f and self.firing < 50:
            self.pos[1] = pos[1]
            self.pos[0] = pos[0]
            self.firing = 100
    def fire(self):
        if self.firing !=0:
            self.pos[0] += 10 
            self.firing -= 1
    
class bicycle_class(object_class):
    def __init__(self, image):
        self.pos = [0,screen[1]-150]
        self.image = image
        self.direc = 1
    def bike(self):
        self.pos[0] += 4
        if self.pos[0] > screen[0]: self.pos[0] = -100
    def collide(self, pos):
        if self.pos[0]-1 < pos[0] < self.pos[0] + 20 and self.pos[1]-100 < pos[1] < self.pos[1] + 40:
            return 1
        else: return 0

    def bounce(self):
        if self.direc == 1:
            self.pos[1] += 10
            if self.pos[1] > screen[1] -150: self.direc = 0
        else:
            self.pos[1] -= 10
            if self.pos[1] < 0: self.direc = 1
            

class chicken_class(object_class):
    def __init__(self, image):
        self.pos = [random.randrange(0,screen[0]),-40]
        
        if random.randrange(0,20) == 10:
            self.image = 7
            
        else:
            self.image = image

        self.delete = False
        self.speedx = random.randrange(0,5)
        self.speedy = random.randrange(4, 20)
    def rain(self):
        self.pos[1] += self.speedy
        self.pos[0] -= self.speedx
        if self.pos[1] > screen[1]:
            self.delete = True

class sub_class(object_class):
    def __init__(self, image):
        self.pos = [0,0]
        self.image = image
        self.x = 10
        self.y = 1
    def move(self):
        if self.pos[0] < 0 or self.pos[0] > screen[0]:
            self.x = - 1 * self.x
        if self.pos[1] < 0 or self.pos[1] > screen[1]-150:
            self.y = -1 * self.y

        if random.randrange(1, 20) == 10 :
            self.x = random.randrange(-10,10)
            self.y = random.randrange(-10,10)
        self.pos[0] += self.x
        self.pos[1] += self.y

class emu_class(object_class):
    def __init__(self, image):
        self.pos = [random.randrange(0,screen[0]), screen[1]-10]
        self.image = image
        self.up = True
    def peak(self):
        if self.up == True:
            self.pos[1] -= 10
            if self.pos[1] < 0: 
                self.up = False
        else:
            self.pos[1] += 10
            if self.pos[1] > screen[1]:
                self.pos[0] = random.randrange(0,screen[0])
                self.up = True
                   
        
ian = ian_class(red, 0)
violin = violin_class(1)
keenan = keenan_class(blue, 3)
brick = brick_class(red)
bicycle = bicycle_class(2)
chicken = chicken_class(4)
chicken1 = chicken_class(4)
chicken2 = chicken_class(4)
chicken3 = chicken_class(4)
chicken4 = chicken_class(4)

bansub = sub_class(5)
emu = emu_class(6)

while True:
    w.fill(pygame.Color(200,200,200))
    w.blit( puzzle, [0,0])
    if make_brick == 1:
        del brick
        brick = brick_class(red)
        score += 1
        make_brick = 0
    if chicken.delete:
        del chicken
        chicken = chicken_class(4)
    if chicken1.delete:
        del chicken1
        chicken1 = chicken_class(4)
    if chicken2.delete:
        del chicken2
        chicken2 = chicken_class(4)
    if chicken3.delete:
        del chicken3
        chicken3 = chicken_class(4)
    if chicken4.delete:
        del chicken4
        chicken4 = chicken_class(4)


    if make_keenan == 1:
        score += 1
        del keenan
        keenan = keenan_class(blue,3)
        make_keenan = 0
    if score_reset:
        score = 0
        score_reset = False
    if keenan_rotate != 0:
        keenan_rotate -= 1
    else:
        keenan_pic = pygame.transform.rotate(keenan_pic, 90)
        image_lib[3] = keenan_pic 
        keenan_rotate = 20
    if score > 50:
        win = True

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
            if event.key == K_SPACE and start_seq == True:
                start_seq = False
            ian.key()
            violin.key(ian.pos)
            if event.key == K_r:
                game = True
                if score > 50:
                    game_cont = True
            if event.key == K_k:
                keenan_pic = pygame.transform.rotate(keenan_pic, 90)
                image_lib[3] = keenan_pic 
                w.blit(keenan_pic, (0,0))


    pygame.mouse.set_visible(False)
    if ian.jump_check != 0:
        ian.jump() 
    elif ian.pos[1] != ian.pos_init[1]:
        ian.pos[1] += 5

    if start_seq == True:
        
        w.fill(white)
        msg = font.render('SPACE to jump',0,black)
        w.blit(msg,(0,0))
         
        msg = font.render('F to shoot',0,black)
        w.blit(msg,(0,100))

        msg = font.render('Merry Christmas',0,black)
        w.blit(msg,(0,200))

        msg = font.render('Ian!',0,black)
        w.blit(msg,(0,300))
    elif win == True and game_cont == False:
        w.fill(white)
        msg = font.render('Congrats!', 0, black)
        w.blit(msg, (0,0))
        msg = font.render('You Won!', 0, black)
        w.blit(msg, (0,100))
        msg = font.render('Made By:', 0, black)
        w.blit(msg, (0,200))
        msg = font.render('Byron', 0, black)
        w.blit(msg, (0,300))
        msg = font.render('Press R to Cont.', 0, black)
        w.blit(msg, (0,400))

    elif game == True:

        msg = font.render(str(score), 0, black)
        w.blit(msg, (0,0))

        if score > 40:
            emu.draw()
            emu.peak()
                

        if score > 5:
            chicken.draw()
            chicken.rain()

        if score > 20:
            chicken1.draw()
            chicken1.rain()
            chicken2.draw()
            chicken2.rain()
            chicken3.draw()
            chicken3.rain()
            chicken4.draw()
            chicken4.rain()
            if chicken_text != 0:
                chicken_text -= 1
            else:
                msg = font.render('CHICKEN!!', 0, pygame.Color(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))
                w.blit(msg, (screen[0]/3,0))
                chicken_text = 2


    
        violin.draw()
        violin.fire()
        if score > 10:
            keenan.draw()
            keenan.bobble()
            keenan.move()

        bicycle.draw()
        bicycle.bike()
        if score > 15:
            bicycle.bounce()
        score += bicycle.collide(ian.pos)

        #make_keenan = keenan.collide(violin.pos)
        if keenan.collide(violin.pos):
            make_keenan = True
            violin.pos = [0,-100]
        
        brick.draw()
        make_brick = brick.move()

        if not ian.check_collide(brick.center, brick.pos1[0]) or not ian.check_keenan(keenan.pos):
            game = False
    

        ian.draw()

        pygame.draw.rect(w,green,[0, screen[1]-80, screen[0], 100])
        if score > 25:
            bansub.draw()
            bansub.move()
            msg = font.render('BANANA SUBMARINE', 0, pygame.Color(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))
            w.blit(msg,(0, screen[1] - 150))

        if score > 30:
            if tint_timer != 0: tint_timer -= 1
            else:
                tinter = random.randrange(0,5)
                tint_timer = 10
            tint_surface.fill(tint_dict[tinter])
            #tint_surface.fill((100,100,100))
            w.blit(tint_surface,(0,0))

    elif game == False:
        make_brick = 1
        make_keenan = 1
        score_reset = True
        #score_old = 0
        if score > 0:
            score_old = score

        w.fill(white)
        msg = font.render('Game Over', 0, black)
        w.blit(msg, (0,0))
        msg = font.render('Press R', 0, black)
        w.blit(msg, (0, 100)) 
        msg = font.render('To Restart', 0, black)
        w.blit(msg, (0, 200)) 
        msg = font.render('Score:' + str(score_old), 0, black)
        w.blit(msg, (0,300))
    else:
        w.fill(white)
        msg = font.render('You broke something!', 0, black)
        w.blit(msg, (0,0))

    pygame.display.update()
    fpsClock.tick(60)
