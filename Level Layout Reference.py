#thanks to sentdex on Youtube.com for Pygame basics tutorials


                        
import pygame
import pyganim
import sys
import time
import winsound
from pygame.locals import *
from types import MethodType
import itertools

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

Tutorial = pygame.mixer.Sound('assets/sounds/Tutorial.wav')
level1 = pygame.mixer.Sound('assets/sounds/L1.wav')
pygame.mixer.music.load('assets/sounds/Boss.wav')
pygame.mixer.music.set_volume(0.45)#0.45
hit = pygame.mixer.Sound('assets/sounds/hit.wav')
explodesound = pygame.mixer.Sound('assets/sounds/explodesound.wav')
suspense = pygame.mixer.Sound('assets/sounds/anticipation.wav')
suspense.set_volume(01)#1
laser1wav = pygame.mixer.Sound('assets/sounds/lasers/Laser1.wav')
laser2wav = pygame.mixer.Sound('assets/sounds/lasers/Laser2.wav')
laser3wav = pygame.mixer.Sound('assets/sounds/lasers/Laser3.wav')
laser4wav = pygame.mixer.Sound('assets/sounds/lasers/Laser4.wav')
laser5wav = pygame.mixer.Sound('assets/sounds/lasers/Laser5.wav')
laser6wav = pygame.mixer.Sound('assets/sounds/lasers/Laser6.wav')
laser7wav = pygame.mixer.Sound('assets/sounds/lasers/Laser7.wav')
volume = 0.4#0.4
Tutorial.set_volume(01)#1
level1.set_volume(0.5)#0.5
laser1wav.set_volume(volume)
hit.set_volume(0.5)#0.5
explodesound.set_volume(0.4)#0.4
laser2wav.set_volume(volume)
laser3wav.set_volume(volume)
laser4wav.set_volume(volume)
laser5wav.set_volume(volume)
laser6wav.set_volume(volume)
laser7wav.set_volume(volume)


setDisplay = pygame.display.set_mode((640,480),FULLSCREEN)
pygame.mouse.set_visible(0)
#setDisplay = pygame.display.set_mode((640,480))
pygame.display.set_caption('Dubstep Warriors.wav')

RDOWN = 0
LDOWN = 0
ADOWN = 0
SDOWN = 0
RPRESS = 0
LPRESS = 0
ZUP = 0
fscreen = 1#1
playercaught = 1
WIN = 0

global XDOWN
global XCOOL
global ZDOWN
global ZUP
global SONG
global UDOWN
global DDOWN
global UPRESS
global DPRESS
global WIN
XDOWN = 0
XCOOL = 0
ZDOWN = 0
UDOWN = 0
DDOWN = 0
UPRESS = 0
DPRESS = 0
FPS = 30
fpsTime = pygame.time.Clock()

#checkEvent
def checkEvent():
        global LDOWN
        global RDOWN
        global ADOWN
        global SDOWN
        global ZDOWN
        global XDOWN
        global UDOWN
        global DDOWN
        global UPRESS
        global DPRESS
        global LPRESS
        global RPRESS
        global ZUP
        global fscreen
        global title
        global pause
        global RUP
        global LUP
        for event in pygame.event.get():
                #print event
                if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                if event.type == KEYDOWN:
                        if event.key == K_LEFT:
                                LDOWN = 1
                                LPRESS = 1
                        if event.key == K_RIGHT:
                                RDOWN = 1
                                RPRESS = 1
                        if event.key == K_UP:
                                UDOWN = 1
                                UPRESS = 1
                        if event.key == K_DOWN:
                                DDOWN = 1
                                DPRESS = 1
                        if event.key == K_z:
                                ZDOWN = 1
                                ZUP = 0
                        if event.key == K_x:
                                XDOWN = 1
                        if event.key == K_a:
                                ADOWN = 1
                        if event.key == K_s:
                                SDOWN = 1
                        if event.key == K_ESCAPE:
                                Tutorial.stop()#winsound.PlaySound("sounds/silencer.wav",winsound.SND_ASYNC)
                                level1.stop()
                                pygame.quit()
                                sys.exit()
                        if event.key == K_RETURN:
                                if title == 0 and pause == 0 and WIN == 0:
                                        pause = 1
                                        pygame.mixer.pause()
                                        pygame.mixer.music.pause()
                                elif title == 0:
                                        pause = 0
                                        pygame.mixer.unpause()
                                        for l in range(len(bg)):
                                                for i in range(len(bg[l].enemies)):
                                                        if bg[l].enemies[i] != 0:
                                                                bg[l].enemies[i].animflag = 1
                                        if boss != 0:
                                                boss.image.play()
                                        pygame.mixer.music.unpause()
                                else:
                                        title = 0
                                        Tutorial.play()#winsound.PlaySound("sounds/L1.wav",winsound.SND_ASYNC)
                                        global SONG
                                        SONG = 'Tutorial'
                        if event.key == K_EQUALS:
                                if fscreen == 0:
                                        setDisplay = pygame.display.set_mode((640,480),FULLSCREEN)
                                        fscreen = 1
                                        pygame.mouse.set_visible(0)
                                else:
                                        setDisplay = pygame.display.set_mode((640,480))
                                        fscreen = 0
                                        pygame.mouse.set_visible(1)
                if event.type == KEYUP:
                        if event.key == K_LEFT:
                                LDOWN = 0
                                LUP = 1
                        if event.key == K_RIGHT:
                                RDOWN = 0
                                RUP = 1
                        if event.key == K_UP:
                                UDOWN = 0
                        if event.key == K_DOWN:
                                DDOWN = 0
                        if event.key == K_z:
                                ZDOWN = 0
                                ZUP = 1
                        if event.key == K_x:
                                XDOWN = 0
#end checkEvent
#sprite
class sprite(object):
        def _init_(self,sx,sy,simage):
                self.x = sx
                self.y = sy
                self.image = pygame.image.load(simage)
                self.dimensions = self.image.get_rect().size
                self.width = self.dimensions[0]
                self.height = self.dimensions[1]
                self.yspeed = 10
                self.xspeed = 16
                self.ymovement = 'none'
                self.xmovement = 'none'
                self.xoffset = 0
                self.yoffset = 0
        def checkCollide(self, obj):
                state = 0
                selfdimensions = [self.width,self.height]
                objdimensions = [obj.width,obj.height]
                selfbottom = (self.y + self.yoffset) + selfdimensions[1]
                selfright = (self.x + self.xoffset) + selfdimensions[0]
                selfleft = self.x + self.xoffset
                selftop = self.y + self.yoffset
                objbottom = (obj.y + obj.yoffset) + objdimensions[1]
                objright = (obj.x + obj.xoffset) + objdimensions[0]
                objleft = obj.x + obj.xoffset
                objtop = obj.y + obj.yoffset
                if selfright > objleft and selfbottom > objtop and selfleft < objright and selftop < objbottom:
                        state = 1
                return state
        
        def update(self):
                setDisplay.blit(self.image,(self.x,self.y))
#end sprite

#enemy
class enemy(sprite):
        def _init_(self,sx,sy,limitx1,limitx2,scene):
                self.yspeed = 5
                self.xspeed = 0.5
                self.speedlimit = 4
                self.health = 3
                self.xoffset = 0
                self.yoffset = 0
                self.anim = 'left'
                self.animflag = 1

                #vars for collision and movement limits
                self.scene = scene
                self.grosslx1 = limitx1
                self.grosslx2 = limitx2
                
                

                self.gib = 0
                self.explosion = 0
                
                self.dead = 0
                self.x = self.scene.x + sx
                self.y = self.scene.y + sy
                self.image = pygame.image.load('assets/sprites/enemy/enemy1.png').convert_alpha()
                self.shadow = self.shadow = pygame.image.load('assets/sprites/player/shadow.png').convert_alpha()

                self.dimensions = self.image.get_rect().size
                self.width = self.dimensions[0]
                self.height = self.dimensions[1]
                
                self.ymovement = 'none'
                self.xmovement = 'right'
                self.dx = 0
                self.dy = 0
                self.anim = 'right'
        def chase(self, obj):
                self.limitx1 = self.scene.x + self.grosslx1
                self.limitx2 = self.scene.x + self.grosslx2
                
                if obj.y < self.y + self.height and obj.y + obj.height > self.y:
                        self.speedlimit = 10
                        if obj.x > self.x:
                                if self.x + self.width > 0 and self.x < 640:
                                        self.xmovement = 'right'
                                        if self.anim == 'left':
                                                self.anim = 'right'
                                                self.animflag = 1
                        elif obj.x < self.x:
                                if self.x + self.width > 0 and self.x < 640:
                                        self.xmovement = 'left'
                                        if self.anim == 'right':
                                                self.anim = 'left'
                                                self.animflag = 1
                else:
                        if self.x > self.limitx2 - 1:
                                self.xmovement = 'left'
                                self.dx = 0
                                self.anim = 'left'
                                self.animflag = 1
                                self.speedlimit = 4
                        elif self.x < self.limitx1 + 1:
                                self.xmovement = 'right'
                                self.dx = 0
                                self.anim = 'right'
                                self.animflag = 1
                                self.speedlimit = 4
                        
                #animation
                if self.anim == 'right' and self.animflag == 1:
                        self.image = pyganim.PygAnimation([('assets/sprites/enemy/enemy1.png',0.05),('assets/sprites/enemy/enemy2.png',0.05)])
                        self.image.play()
                        self.animflag = 0
                elif self.anim == 'left' and self.animflag == 1:
                        self.image = pyganim.PygAnimation([('assets/sprites/enemy/enemy1.png',0.05),('assets/sprites/enemy/enemy2.png',0.05)])
                        self.image.flip(1,0)
                        self.image.play()
                        self.animflag = 0

                
                if self.xmovement == 'right':
                        self.dx += self.xspeed
                
                elif self.xmovement == 'left':
                        self.dx -= self.xspeed
                        
                if self.dx > self.speedlimit:
                        self.dx = self.speedlimit
                if self.dx < -self.speedlimit:
                        self.dx = -self.speedlimit
                        
                self.x += self.dx
                
                if self.x <= self.limitx1:
                        self.x -= self.dx
                        while self.x > self.limitx1:
                                self.x -= 1
                                self.dx = 3
                        if self.x < self.limitx1:
                                self.x += 1
                elif self.x >= self.limitx2:
                        self.x -= self.dx
                        while self.x < self.limitx2:
                                self.x += 1
                                self.dx = -3
                        if self.x > self.limitx2:
                                self.x -= 1
                                
                if self.health == 0:
                        self.dead = 1
                        self.gib = [gib(),gib(),gib(),gib()]
                        self.gib[0]._init_((self.x),(self.y),(-6),('assets/sprites/enemy/egib1.png'))
                        self.gib[1]._init_((self.x),(self.y + 32),(-8),'assets/sprites/enemy/egib2.png')
                        self.gib[2]._init_((self.x + self.width),(self.y),(6),'assets/sprites/enemy/egib3.png')
                        self.gib[3]._init_((self.x + self.width),(self.y + 32),(8),'assets/sprites/enemy/egib4.png')
                        self.explosion = explosion()
                        self.explosion._init_(self.x - 16,self.y)
                        explodesound.play()
                if self.dead == 1:
                        
                        self.x = -32
                        self.y = -128
                        self.health = 10
                        #self._init_(-32,-64)
        def kill(self, obj):
                if self.checkCollide(obj):
                        obj.dead = 1
        def update(self):
                if self.xmovement == 'left':
                        setDisplay.blit(self.shadow,(self.x-20,self.y-36))
                else:
                        setDisplay.blit(self.shadow,(self.x-24,self.y-36))
                self.image.blit(setDisplay,(self.x,self.y))
                self.image.blit(setDisplay,(self.x,self.y))
#end enemy

#gib
class gib(sprite):
        def _init_(self,sx,sy,xvelo,simage):
                self.x = sx
                self.y = sy
                self.image = pygame.image.load(simage).convert_alpha()
                self.dimensions = self.image.get_rect().size
                self.width = self.dimensions[0]
                self.height = self.dimensions[1]
                self.yspeed = 10
                self.xspeed = 16
                self.ymovement = 'none'
                self.xmovement = 'none'
                self.xoffset = 0
                self.yoffset = 0
                self.xvelo = xvelo
                self.fallspeed = 5
                self.dy = -20
                self.dead = 0
        def fly(self):
                self.dy += self.fallspeed
                self.x += self.xvelo
                self.y += self.dy
                if self.xvelo > 0:
                        self.rotate = 1
                else:
                        self.rotate = -1
                self.image = pygame.transform.rotate(self.image, self.rotate * 10)
                if self.y > 480:
                        self.dead = 1
#end gib

#explosion
class explosion(sprite):
        def _init_(self,sx,sy):
                self.x = sx
                self.y = sy
                self.image = pygame.image.load('assets/sprites/enemy/explode1.png')
                self.dimensions = self.image.get_rect().size
                self.width = self.dimensions[0]
                self.height = self.dimensions[1]
                self.yspeed = 10
                self.xspeed = 16
                self.ymovement = 'none'
                self.xmovement = 'none'
                self.xoffset = 0
                self.yoffset = 0
                self.dead = 0
                self.anim = 0
        def animate(self):
                if self.anim < 2:
                        self.image = pygame.image.load('assets/sprites/enemy/explode1.png')
                elif self.anim < 4:
                        self.image = pygame.image.load('assets/sprites/enemy/explode2.png')
                elif self.anim < 6:
                        self.image = pygame.image.load('assets/sprites/enemy/explode3.png')
                elif self.anim < 8:
                        self.image = pygame.image.load('assets/sprites/enemy/explode4.png')
                elif self.anim < 10:
                        self.image = pygame.image.load('assets/sprites/enemy/explode5.png')
                elif self.anim < 12:
                        self.image = pygame.image.load('assets/sprites/enemy/explode6.png')
                self.anim += 1
                if self.anim == 12:
                        self.dead = 1
#end explosion

#projectile           
class projectile(sprite):
        def _init_(self,x,y,sx,sy):
                self.yspeed = 5
                self.xspeed = 24
                
                self.xmovement = sx
                self.ymovement = sy
                self.movechange = 1
                self.health = 1
                
                self.x = x
                self.y = y
                self.image = pygame.image.load('assets/sprites/projectiles/projectile1.png').convert_alpha()

                self.color

                self.dimensions = self.image.get_rect().size
                self.xoffset = 15
                self.yoffset = 15
                self.width = self.dimensions[0] - 30
                self.height = self.dimensions[1] - 30
                
                self.dead = 0
                self.animPos = 0
        def color(self, obj):
                if obj.color == 'red':
                        self.color == 'red'
                        
        def anim(self):
                if self.xmovement == 'right' and self.movechange == 1 or self.xmovement == 'none':
                        self.image = pyganim.PygAnimation([('assets/sprites/projectiles/blue/1.png',0.1),
                                                           ('assets/sprites/projectiles/blue/2.png',0.1),
                                                           ('assets/sprites/projectiles/blue/3.png',0.1),
                                                           ('assets/sprites/projectiles/blue/1.png',0.1)])
                        self.image.play()
                        self.movechange = 0
                elif self.xmovement == 'left' and self.movechange == 1:
                        self.image = pyganim.PygAnimation([('assets/sprites/projectiles/blue/1.png',0.1),
                                                           ('assets/sprites/projectiles/blue/2.png',0.1),
                                                           ('assets/sprites/projectiles/blue/3.png',0.1),
                                                           ('assets/sprites/projectiles/blue/1.png',0.1)])
                        self.image.play()
                        self.image.flip(1,0)
                        self.movechange = 0

        def kill(self, obj):
                if self.checkCollide(obj) and self.xmovement != 'none':
                        #obj.dead = 1
                        if self.health == 0:
                                self.dead = 1
                                self.x = -64
                                self.y = -64
                                #if obj.__class__.__name__ != 'Boss':
                                        #ouch animation flag
                                #else:
                                obj.health -= 1
                                obj.dx = 0
                                self.xmovement = 'none'
                                self.ymovement = 'none'
                                hit.play()
                        if self.dead == 0:
                                
                                
                                self.health = 0
                                self.image = pyganim.PygAnimation([('assets/sprites/projectiles/flash.png',1)])
                                self.image.play()
                                
        def move(self):
                #if self.y > 592:
                 #       self.ymovement = 'up'
                #if self.y <= 0:
                 #       self.ymovement = 'down'
                if self.ymovement == 'down':
                        self.y += self.yspeed

                elif self.ymovement == 'up':
                        self.y -= self.yspeed

                #if self.x >= 576:
                 #       self.xmovement = 'left'
                #elif self.x <= 0:
                 #       self.xmovement = 'right'
                if self.xmovement == 'right':
                        self.x += self.xspeed
                elif self.xmovement == 'left':
                        self.x -= self.xspeed
        def checkOOB(self):
                if self.x < -64 or self.x > 640:
                        self.dead = 1
                        self.x = -64
                        self.y = -64
                        self.xmovement = 'none'
                        self.ymovement = 'none'
                if self.y < -64 or self.y > 480:
                        self.dead = 1
                        self.x = -64
                        self.y = -64
                        self.xmovement = 'none'
                        self.ymovement = 'none'
        def update(self):
                self.image.blit(setDisplay,(self.x,self.y))
#end projectile

#player
class player(sprite):
        def _init_(self,sx,sy,simage):
                self.image = pygame.image.load(simage).convert_alpha()
                self.yspeed = 10
                self.xspeed = 8
                self.xoffset = 0
                self.yoffset = 0
                self.jumpHeight = 4
                self.jumplimit = 25
                self.dimensions = self.image.get_rect().size
                self.width = self.dimensions[0]
                self.height = self.dimensions[1]
                self.shadow = pygame.image.load('assets/sprites/player/shadow.png').convert_alpha()
                self.fall = 0

                #flags for scrolling
                self.scrollu = 0
                self.scrolld = 0
                self.scrollr = 0
                self.scrolll = 0

                #flag for jump animation
                self.janim = 0
                
                self.jumping = 0

                #jump speed (dynamically update upon each jump)
                self.dy = 0#self.jumpHeight
                self.onGround = 1

                #stops player from moving if they hit a wall
                self.wallflag = 0

                #ladder flags
                self.ladder = 0
                self.lanim = 0

                #color for weapons
                self.color = 'blue'
                self.cs = 0
                
                self.dead = 0
                
                self.x = sx
                self.y = sy

                #y movement velocity (modified by dy during jumps)
                self.jv = 0
                
                self.canJump = 1
                self.facing = 'right'
                self.laser = [projectile()] * 5
                for i in range (len(self.laser)):
                        self.laser[i]._init_(-64,-64,'none','none')

        def colour(self):
                global ADOWN
                global SDOWN
                global LDOWN
                global LPRESS
                global RPRESS
                global RDOWN
                global LUP
                global RUP
                global UPRESS
                global DPRESS
                
                if ADOWN == 1:
                                self.cs -= 1
                                if self.cs > 5:
                                        self.cs = 0
                                elif self.cs < 0:
                                        self.cs = 5
                                
                                if self.cs == 0:
                                        self.color = 'blue'
                                        LUP = 1
                                        RUP = 1
                                        LPRESS = 1
                                        RPRESS = 1
                                        UPRESS = 1
                                        DPRESS = 1
                                        if self.onGround == 0:
                                                self.janim = 1
                                elif self.cs == 1:
                                        self.color = 'red'
                                        LUP = 1
                                        RUP = 1
                                        LPRESS = 1
                                        RPRESS = 1
                                        UPRESS = 1
                                        DPRESS = 1
                                        if self.onGround == 0:
                                                self.janim = 1
                                elif self.cs == 2:
                                        self.color = 'green'
                                        LUP = 1
                                        RUP = 1
                                        LPRESS = 1
                                        RPRESS = 1
                                        UPRESS = 1
                                        DPRESS = 1
                                        if self.onGround == 0:
                                                self.janim = 1
                                elif self.cs == 3:
                                        self.color = 'purple'
                                        LUP = 1
                                        RUP = 1
                                        LPRESS = 1
                                        RPRESS = 1
                                        UPRESS = 1
                                        DPRESS = 1
                                        if self.onGround == 0:
                                                self.janim = 1
                                elif self.cs == 4:
                                        self.color = 'yellow'
                                        LUP = 1
                                        RUP = 1
                                        LPRESS = 1
                                        RPRESS = 1
                                        UPRESS = 1
                                        DPRESS = 1
                                        if self.onGround == 0:
                                                self.janim = 1
                                elif self.cs == 5:
                                        self.color = 'orange'
                                        LUP = 1
                                        RUP = 1
                                        LPRESS = 1
                                        RPRESS = 1
                                        UPRESS = 1
                                        DPRESS = 1
                                        if self.onGround == 0:
                                                self.janim = 1
                        #else:
                                #bummersound.play()
                                ADOWN = 0
                if SDOWN == 1:
                                self.cs += 1
                                if self.cs > 5:
                                        self.cs = 0
                                elif self.cs < 0:
                                        self.cs = 5
                                if self.cs == 0:
                                        self.color = 'blue'
                                        LUP = 1
                                        RUP = 1
                                        LPRESS = 1
                                        RPRESS = 1
                                        UPRESS = 1
                                        DPRESS = 1
                                        if self.onGround == 0:
                                                self.janim = 1
                                elif self.cs == 1:
                                        self.color = 'red'
                                        LUP = 1
                                        RUP = 1
                                        LPRESS = 1
                                        RPRESS = 1
                                        UPRESS = 1
                                        DPRESS = 1
                                        if self.onGround == 0:
                                                self.janim = 1
                                elif self.cs == 2:
                                        self.color = 'green'
                                        LUP = 1
                                        RUP = 1
                                        LPRESS = 1
                                        RPRESS = 1
                                        UPRESS = 1
                                        DPRESS = 1
                                        if self.onGround == 0:
                                                self.janim = 1
                                elif self.cs == 3:
                                        self.color = 'purple'
                                        LUP = 1
                                        RUP = 1
                                        LPRESS = 1
                                        RPRESS = 1
                                        UPRESS = 1
                                        DPRESS = 1
                                        if self.onGround == 0:
                                                self.janim = 1
                                elif self.cs == 4:
                                        self.color = 'yellow'
                                        LUP = 1
                                        RUP = 1
                                        LPRESS = 1
                                        RPRESS = 1
                                        UPRESS = 1
                                        DPRESS = 1
                                        if self.onGround == 0:
                                                self.janim = 1
                                elif self.cs == 5:
                                        self.color = 'orange'
                                        LUP = 1
                                        RUP = 1
                                        LPRESS = 1
                                        RPRESS = 1
                                        UPRESS = 1
                                        DPRESS = 1
                                        if self.onGround == 0:
                                                self.janim = 1
                        #else:
                                #bummersound.play()
                                SDOWN = 0
                
                
        def anim(self):
                global LPRESS
                global RPRESS
                global RUP
                global LUP
                if self.ladder == 0:
                        #left idle
                        if self.facing == 'left' and self.canJump == 1 and LUP == 1:
                                if self.color == 'red':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/idle 180.png',1),('assets/sprites/player/rblink.png',0.1)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        LUP = 0
                                elif self.color == 'green':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/idle r120.png',1),('assets/sprites/player/gblink.png',0.1)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        LUP = 0
                                elif self.color == 'purple':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/idle g160.png',1),('assets/sprites/player/pblink.png',0.1)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        LUP = 0
                                elif self.color == 'yellow':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/idle p150.png',1),('assets/sprites/player/yblink.png',0.1)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        LUP = 0
                                elif self.color == 'orange':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/idle y-50.png',1),('assets/sprites/player/oblink.png',0.1)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        LUP = 0
                                else:
                                        
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/idle.png',1),('assets/sprites/player/blink.png',0.1)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        LUP = 0
                        #right idle
                        elif self.facing == 'right' and self.canJump == 1 and RUP == 1:
                                if self.color == 'red':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/idle 180.png',1),('assets/sprites/player/rblink.png',0.1)])
                                        self.image.play()
                                        RUP = 0
                                elif self.color == 'green':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/idle r120.png',1),('assets/sprites/player/gblink.png',0.1)])
                                        self.image.play()
                                        RUP = 0
                                elif self.color == 'purple':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/idle g160.png',1),('assets/sprites/player/pblink.png',0.1)])
                                        self.image.play()
                                        RUP = 0
                                elif self.color == 'yellow':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/idle p150.png',1),('assets/sprites/player/yblink.png',0.1)])
                                        self.image.play()
                                        RUP = 0
                                elif self.color == 'orange':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/idle y-50.png',1),('assets/sprites/player/oblink.png',0.1)])
                                        self.image.play()
                                        RUP = 0
                                else:
                                        
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/idle.png',1),('assets/sprites/player/blink.png',0.1)])
                                        self.image.play()
                                        RUP = 0
                        #left walk
                        elif self.facing == 'left' and self.canJump == 1 and LPRESS == 1 and RDOWN == 0 and LDOWN == 1:
                                if self.color == 'red':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk1r.png',0.1),
                                                                   ('assets/sprites/player/walk/walk2r.png',0.07),
                                                                   ('assets/sprites/player/walk/walk3r.png',0.07),
                                                                   ('assets/sprites/player/walk/walk4r.png',0.07),
                                                                   ('assets/sprites/player/walk/walk5r.png',0.07),
                                                                   ('assets/sprites/player/walk/walk6r.png',0.07),
                                                                   ('assets/sprites/player/walk/walk7r.png',0.07),
                                                                   ('assets/sprites/player/walk/walk8r.png',0.07)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        LPRESS = 0
                                elif self.color == 'green':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk1g.png',0.1),
                                                                   ('assets/sprites/player/walk/walk2g.png',0.07),
                                                                   ('assets/sprites/player/walk/walk3g.png',0.07),
                                                                   ('assets/sprites/player/walk/walk4g.png',0.07),
                                                                   ('assets/sprites/player/walk/walk5g.png',0.07),
                                                                   ('assets/sprites/player/walk/walk6g.png',0.07),
                                                                   ('assets/sprites/player/walk/walk7g.png',0.07),
                                                                   ('assets/sprites/player/walk/walk8g.png',0.07)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        LPRESS = 0
                                elif self.color == 'purple':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk1p.png',0.1),
                                                                   ('assets/sprites/player/walk/walk2p.png',0.07),
                                                                   ('assets/sprites/player/walk/walk3p.png',0.07),
                                                                   ('assets/sprites/player/walk/walk4p.png',0.07),
                                                                   ('assets/sprites/player/walk/walk5p.png',0.07),
                                                                   ('assets/sprites/player/walk/walk6p.png',0.07),
                                                                   ('assets/sprites/player/walk/walk7p.png',0.07),
                                                                   ('assets/sprites/player/walk/walk8p.png',0.07)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        LPRESS = 0
                                elif self.color == 'yellow':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk1y.png',0.1),
                                                                   ('assets/sprites/player/walk/walk2y.png',0.07),
                                                                   ('assets/sprites/player/walk/walk3y.png',0.07),
                                                                   ('assets/sprites/player/walk/walk4y.png',0.07),
                                                                   ('assets/sprites/player/walk/walk5y.png',0.07),
                                                                   ('assets/sprites/player/walk/walk6y.png',0.07),
                                                                   ('assets/sprites/player/walk/walk7y.png',0.07),
                                                                   ('assets/sprites/player/walk/walk8y.png',0.07)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        LPRESS = 0
                                elif self.color == 'orange':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk1o.png',0.1),
                                                                   ('assets/sprites/player/walk/walk2o.png',0.07),
                                                                   ('assets/sprites/player/walk/walk3o.png',0.07),
                                                                   ('assets/sprites/player/walk/walk4o.png',0.07),
                                                                   ('assets/sprites/player/walk/walk5o.png',0.07),
                                                                   ('assets/sprites/player/walk/walk6o.png',0.07),
                                                                   ('assets/sprites/player/walk/walk7o.png',0.07),
                                                                   ('assets/sprites/player/walk/walk8o.png',0.07)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        LPRESS = 0
                                else:
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk1.png',0.1),
                                                                   ('assets/sprites/player/walk/walk2.png',0.07),
                                                                   ('assets/sprites/player/walk/walk3.png',0.07),
                                                                   ('assets/sprites/player/walk/walk4.png',0.07),
                                                                   ('assets/sprites/player/walk/walk5.png',0.07),
                                                                   ('assets/sprites/player/walk/walk6.png',0.07),
                                                                   ('assets/sprites/player/walk/walk7.png',0.07),
                                                                   ('assets/sprites/player/walk/walk8.png',0.07)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        LPRESS = 0
                        #right walk
                        elif self.facing == 'right' and self.canJump == 1 and RPRESS == 1 and LDOWN == 0 and RDOWN == 1:
                                        #red right walk
                                        if self.color == 'red':
                                                self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk1r.png',0.1),
                                                                   ('assets/sprites/player/walk/walk2r.png',0.07),
                                                                   ('assets/sprites/player/walk/walk3r.png',0.07),
                                                                   ('assets/sprites/player/walk/walk4r.png',0.07),
                                                                   ('assets/sprites/player/walk/walk5r.png',0.07),
                                                                   ('assets/sprites/player/walk/walk6r.png',0.07),
                                                                   ('assets/sprites/player/walk/walk7r.png',0.07),
                                                                   ('assets/sprites/player/walk/walk8r.png',0.07)])
                                                self.image.play()
                                                RPRESS = 0
                                        elif self.color == 'green':
                                                self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk1g.png',0.1),
                                                                   ('assets/sprites/player/walk/walk2g.png',0.07),
                                                                   ('assets/sprites/player/walk/walk3g.png',0.07),
                                                                   ('assets/sprites/player/walk/walk4g.png',0.07),
                                                                   ('assets/sprites/player/walk/walk5g.png',0.07),
                                                                   ('assets/sprites/player/walk/walk6g.png',0.07),
                                                                   ('assets/sprites/player/walk/walk7g.png',0.07),
                                                                   ('assets/sprites/player/walk/walk8g.png',0.07)])
                                                RPRESS = 0
                                                self.image.play()
                                        elif self.color == 'purple':
                                                self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk1p.png',0.1),
                                                                   ('assets/sprites/player/walk/walk2p.png',0.07),
                                                                   ('assets/sprites/player/walk/walk3p.png',0.07),
                                                                   ('assets/sprites/player/walk/walk4p.png',0.07),
                                                                   ('assets/sprites/player/walk/walk5p.png',0.07),
                                                                   ('assets/sprites/player/walk/walk6p.png',0.07),
                                                                   ('assets/sprites/player/walk/walk7p.png',0.07),
                                                                   ('assets/sprites/player/walk/walk8p.png',0.07)])
                                                RPRESS = 0
                                                self.image.play()
                                        elif self.color == 'yellow':
                                                self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk1y.png',0.1),
                                                                   ('assets/sprites/player/walk/walk2y.png',0.07),
                                                                   ('assets/sprites/player/walk/walk3y.png',0.07),
                                                                   ('assets/sprites/player/walk/walk4y.png',0.07),
                                                                   ('assets/sprites/player/walk/walk5y.png',0.07),
                                                                   ('assets/sprites/player/walk/walk6y.png',0.07),
                                                                   ('assets/sprites/player/walk/walk7y.png',0.07),
                                                                   ('assets/sprites/player/walk/walk8y.png',0.07)])
                                                RPRESS = 0
                                                self.image.play()
                                        elif self.color == 'orange':
                                                self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk1o.png',0.1),
                                                                   ('assets/sprites/player/walk/walk2o.png',0.07),
                                                                   ('assets/sprites/player/walk/walk3o.png',0.07),
                                                                   ('assets/sprites/player/walk/walk4o.png',0.07),
                                                                   ('assets/sprites/player/walk/walk5o.png',0.07),
                                                                   ('assets/sprites/player/walk/walk6o.png',0.07),
                                                                   ('assets/sprites/player/walk/walk7o.png',0.07),
                                                                   ('assets/sprites/player/walk/walk8o.png',0.07)])
                                                RPRESS = 0
                                                self.image.play()
                                        else:
                                                self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk1.png',0.1),
                                                                   ('assets/sprites/player/walk/walk2.png',0.07),
                                                                   ('assets/sprites/player/walk/walk3.png',0.07),
                                                                   ('assets/sprites/player/walk/walk4.png',0.07),
                                                                   ('assets/sprites/player/walk/walk5.png',0.07),
                                                                   ('assets/sprites/player/walk/walk6.png',0.07),
                                                                   ('assets/sprites/player/walk/walk7.png',0.07),
                                                                   ('assets/sprites/player/walk/walk8.png',0.07)])
                                                self.image.play()
                                                RPRESS = 0
                        #left jump
                        if self.facing == 'left' and self.canJump == 0:
                                if self.color == 'red' and self.janim == 1:
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4r.png',0.5),
                                                                           ('assets/sprites/player/rjump.png',0.5)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        self.janim = 0
                                elif self.color == 'green' and self.janim == 1:
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4g.png',0.5),
                                                                           ('assets/sprites/player/gjump.png',0.5)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        self.janim = 0
                                elif self.color == 'purple' and self.janim == 1:
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4p.png',0.5),
                                                                           ('assets/sprites/player/pjump.png',0.5)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        self.janim = 0
                                elif self.color == 'yellow' and self.janim == 1:
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4y.png',0.5),
                                                                           ('assets/sprites/player/yjump.png',0.5)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        self.janim = 0
                                elif self.color == 'orange' and self.janim == 1:
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4o.png',0.5),
                                                                           ('assets/sprites/player/ojump.png',0.5)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        self.janim = 0
                                elif self.janim == 1:
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4.png',0.5),
                                                                           ('assets/sprites/player/jump.png',0.5)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        self.janim = 0
                                #left air turn
                                elif self.canJump == 0 and LPRESS == 1 and self.color == 'red':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4r.png',0.5),
                                                                           ('assets/sprites/player/rjump.png',0.5)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        LPRESS = 0
                                elif self.canJump == 0 and LPRESS == 1 and self.color == 'green':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4g.png',0.5),
                                                                           ('assets/sprites/player/gjump.png',0.5)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        LPRESS = 0
                                elif self.canJump == 0 and LPRESS == 1 and self.color == 'purple':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4p.png',0.5),
                                                                           ('assets/sprites/player/pjump.png',0.5)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        LPRESS = 0
                                elif self.canJump == 0 and LPRESS == 1 and self.color == 'yellow':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4y.png',0.5),
                                                                           ('assets/sprites/player/yjump.png',0.5)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        LPRESS = 0
                                elif self.canJump == 0 and LPRESS == 1 and self.color == 'orange':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4o.png',0.5),
                                                                           ('assets/sprites/player/ojump.png',0.5)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        LPRESS = 0
                                elif self.canJump == 0 and LPRESS == 1:
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4.png',0.5),
                                                                           ('assets/sprites/player/jump.png',0.5)])
                                        self.image.flip(1,0)
                                        self.image.play()
                                        LPRESS = 0
                        #right jump
                        elif self.facing == 'right' and self.canJump == 0:
                                if self.color == 'red' and self.janim == 1:
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4r.png',0.5),
                                                                           ('assets/sprites/player/rjump.png',0.5)])
                                        self.image.play()
                                        self.janim = 0
                                elif self.color == 'green' and self.janim == 1:
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4g.png',0.5),
                                                                           ('assets/sprites/player/gjump.png',0.5)])
                                        self.image.play()
                                        self.janim = 0
                                elif self.color == 'purple' and self.janim == 1:
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4p.png',0.5),
                                                                           ('assets/sprites/player/pjump.png',0.5)])
                                        self.image.play()
                                        self.janim = 0
                                elif self.color == 'yellow' and self.janim == 1:
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4y.png',0.5),
                                                                           ('assets/sprites/player/yjump.png',0.5)])
                                        self.image.play()
                                        self.janim = 0
                                elif self.color == 'orange' and self.janim == 1:
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4o.png',0.5),
                                                                           ('assets/sprites/player/ojump.png',0.5)])
                                        self.image.play()
                                        self.janim = 0
                                elif self.janim == 1:
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4.png',0.5),
                                                                           ('assets/sprites/player/jump.png',0.5)])
                                        self.image.play()
                                        self.janim = 0
                                #right air turn
                                elif self.canJump == 0 and RPRESS == 1 and self.color == 'red':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4r.png',0.5),
                                                                           ('assets/sprites/player/rjump.png',0.5)])
                                        self.image.play()
                                        RPRESS = 0
                                elif self.canJump == 0 and RPRESS == 1 and self.color == 'green':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4g.png',0.5),
                                                                           ('assets/sprites/player/gjump.png',0.5)])
                                        self.image.play()
                                        RPRESS = 0
                                elif self.canJump == 0 and RPRESS == 1 and self.color == 'purple':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4p.png',0.5),
                                                                           ('assets/sprites/player/pjump.png',0.5)])
                                        self.image.play()
                                        RPRESS = 0
                                elif self.canJump == 0 and RPRESS == 1 and self.color == 'yellow':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4y.png',0.5),
                                                                           ('assets/sprites/player/yjump.png',0.5)])
                                        self.image.play()
                                        RPRESS = 0
                                elif self.canJump == 0 and RPRESS == 1 and self.color == 'orange':
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4o.png',0.5),
                                                                           ('assets/sprites/player/ojump.png',0.5)])
                                        self.image.play()
                                        RPRESS = 0
                                elif self.canJump == 0 and RPRESS == 1:
                                        self.image = pyganim.PygAnimation([('assets/sprites/player/walk/walk4.png',0.5),
                                                                           ('assets/sprites/player/jump.png',0.5)])
                                        self.image.play()
                                        RPRESS = 0
                elif self.lanim and UPRESS:
                        global UPRESS
                        if self.color == 'red':
                                self.image = pyganim.PygAnimation([('assets/sprites/player/rclimb.png',0.1),('assets/sprites/player/rclimbleft.png',0.1)])
                                self.image.play()
                                self.lanim = 0
                                UPRESS = 0
                        elif self.color == 'green':
                                self.image = pyganim.PygAnimation([('assets/sprites/player/gclimb.png',0.1),('assets/sprites/player/gclimbleft.png',0.1)])
                                self.image.play()
                                self.lanim = 0
                                UPRESS = 0
                        elif self.color == 'purple':
                                self.image = pyganim.PygAnimation([('assets/sprites/player/pclimb.png',0.1),('assets/sprites/player/pclimbleft.png',0.1)])
                                self.image.play()
                                self.lanim = 0
                                UPRESS = 0
                        elif self.color == 'yellow':
                                self.image = pyganim.PygAnimation([('assets/sprites/player/yclimb.png',0.1),('assets/sprites/player/yclimbleft.png',0.1)])
                                self.image.play()
                                self.lanim = 0
                                UPRESS = 0
                        elif self.color == 'orange':
                                self.image = pyganim.PygAnimation([('assets/sprites/player/oclimb.png',0.1),('assets/sprites/player/oclimbleft.png',0.1)])
                                self.image.play()
                                self.lanim = 0
                                UPRESS = 0
                        else:
                                self.image = pyganim.PygAnimation([('assets/sprites/player/climb.png',0.1),('assets/sprites/player/climbleft.png',0.1)])
                                self.image.play()
                                self.lanim = 0
                                UPRESS = 0
                elif self.lanim and DPRESS:
                        global DPRESS
                        if self.color == 'red':
                                self.image = pyganim.PygAnimation([('assets/sprites/player/rclimb.png',0.1),('assets/sprites/player/rclimbleft.png',0.1)])
                                self.image.play()
                                self.lanim = 0
                                DPRESS = 0
                        elif self.color == 'green':
                                self.image = pyganim.PygAnimation([('assets/sprites/player/gclimb.png',0.1),('assets/sprites/player/gclimbleft.png',0.1)])
                                self.image.play()
                                self.lanim = 0
                                DPRESS = 0
                        elif self.color == 'purple':
                                self.image = pyganim.PygAnimation([('assets/sprites/player/pclimb.png',0.1),('assets/sprites/player/pclimbleft.png',0.1)])
                                self.image.play()
                                self.lanim = 0
                                DPRESS = 0
                        elif self.color == 'yellow':
                                self.image = pyganim.PygAnimation([('assets/sprites/player/yclimb.png',0.1),('assets/sprites/player/yclimbleft.png',0.1)])
                                self.image.play()
                                self.lanim = 0
                                DPRESS = 0
                        elif self.color == 'orange':
                                self.image = pyganim.PygAnimation([('assets/sprites/player/oclimb.png',0.1),('assets/sprites/player/oclimbleft.png',0.1)])
                                self.image.play()
                                self.lanim = 0
                                DPRESS = 0
                        else:
                                self.image = pyganim.PygAnimation([('assets/sprites/player/climb.png',0.1),('assets/sprites/player/climbleft.png',0.1)])
                                self.image.play()
                                self.lanim = 0
                                DPRESS = 0
        #jgravity
        def gravity(self):
                global ZUP
                global playeraught
                if self.ladder == 0:
                        #offground gravity
                        if self.onGround == 0:
                                if self.jumping:
                                        self.fall = 0
                                self.jv -= self.dy

                                #if self.jv < -4 or self.jv > 4:
                                      #  self.dy -= 1
                                #if self.jv < 4 and self.jv > -4:
                                      #  self.dy -= 50
                                #else:
                                self.dy -= 0.75
                                if self.jv > 0 and self.jv < 8:
                                        self.jv = 0.25
                                
                                
                                if self.jv > self.jumplimit:
                                        self.jv = self.jumplimit
                                if ZUP == 1 and self.jv < -6:
                                        self.jv = -6
                                        self.fall = 1
                                        ZUP = 0
                                if self.fall == 1 and self.dy > 0:
                                        self.dy = 0
                                        #self.jv = 0
                                self.y += self.jv
                if self.y > 480:
                        self.dead = 1
                

                #landing
##                if self.y > 288:
##                        self.y = 288
##                        self.jv = 0
##                        self.canJump = 1
##                        self.fall = 0
##                        LPRESS = 1
##                        RPRESS = 1
##                        self.jumping = 0
##                        self.onGround = 1
##                        playercaught = 1
        def control(self):
                global XDOWN
                global LPRESS
                global RPRESS
                global ZUP
                self.scrollr = 0
                self.scrolll = 0
                
                if LDOWN == 1 and self.wallflag == 0 and self.ladder == 0:
                        self.facing = 'left'
                        self.x -= self.xspeed
                        if self.x <= -4:
                                self.x += self.xspeed
                                while self.x > -4:
                                        self.x -= 1
                                if self.x < -4:
                                        self.x += 1
                        if self.x < 256:
                                self.scrolll = 1
                if RDOWN == 1 and self.wallflag == 0 and self.ladder == 0:
                        self.facing = 'right'
                        
                        self.x += self.xspeed
                        if self.x >= 612:
                                self.x -= self.xspeed
                                while self.x < 612:
                                        self.x += 1
                                if self.x > 612:
                                        self.x -= 1
                        if self.x > 384:
                                self.scrollr = 1
                #jumpinit
                if ZDOWN == 1 and self.canJump == 1 :
                        global ZDOWN
                        global RPRESS
                        global LPRESS
                        self.onGround = 0
                        self.jumping = 1
                        self.janim = 1
                        ZDOWN = 0
                        self.canJump = 0
                        if self.ladder == 0:
                                self.dy = self.jumpHeight
                                laser2wav.play()
                        else:
                                self.dy = 0
                                self.jv = 3
                                self.y -= 5
                                self.ladder = 0
      

                if XDOWN == 1 and XCOOL == 0:
                        global XCOOL
                        XCOOL = 5
                        XDOWN = 0
                        sound = laser5wav
                        i = 0
                        if self.laser[i].xmovement == 'none':
                                self.laser[i] = projectile()
                                if self.facing == 'right':
                                        self.laser[i]._init_((self.x + (int(self.width/8))), (self.y),'right','none')
                                        sound.play()
                                elif self.facing == 'left':
                                        self.laser[i]._init_(self.x - 40, (self.y),'left','none')
                                        sound.play()
                        elif self.laser[i+1].xmovement == 'none':
                                self.laser[i+1] = projectile()
                                if self.facing == 'right':
                                        self.laser[i+1]._init_((self.x + (int(self.width/8))), (self.y),'right','none')
                                        sound.play()
                                elif self.facing == 'left':
                                        self.laser[i+1]._init_(self.x - 40, (self.y),'left','none')
                                        sound.play()
                        elif self.laser[i+2].xmovement == 'none':
                                self.laser[i+2] = projectile()
                                if self.facing == 'right':
                                        self.laser[i+2]._init_((self.x + (int(self.width/8))), (self.y),'right','none')
                                        sound.play()
                                elif self.facing == 'left':
                                        self.laser[i+2]._init_(self.x - 40, (self.y),'left','none')
                                        sound.play()
                        elif self.laser[i+3].xmovement == 'none':
                                self.laser[i+3] = projectile()
                                if self.facing == 'right':
                                        self.laser[i+3]._init_((self.x + (int(self.width/8))), (self.y),'right','none')
                                        sound.play()
                                elif self.facing == 'left':
                                        self.laser[i+3]._init_(self.x - 40, (self.y),'left','none')
                                        sound.play()
                        elif self.laser[i+4].xmovement == 'none':
                                self.laser[i+4] = projectile()
                                if self.facing == 'right':
                                        self.laser[i+4]._init_((self.x + (int(self.width/8))), (self.y),'right','none')
                                        sound.play()
                                elif self.facing == 'left':
                                        self.laser[i+4]._init_(self.x - 40, (self.y),'left','none')
                                        sound.play()
                if self.dead == 1:
                        reset()
                        #pygame.quit()
                        #sys.exit()
        def correctPlayer(self, blk):
                blkdimensions = [blk.width,blk.height]
                selfdimensions = [self.width,self.height]
                blkbottom = (blk.y + blk.yoffset) + blkdimensions[1]
                blkright = (blk.x + blk.xoffset) + blkdimensions[0]
                blkleft = blk.x
                blktop = blk.y + blk.yoffset
                selfbottom = (self.y + self.yoffset) + selfdimensions[1]
                selfright = (self.x + self.xoffset) + selfdimensions[0]
                selfleft = self.x + self.xoffset
                selftop = self.y + self.yoffset
                global blktop
                global selfbottom
                global playercaught
                global LPRESS
                global RPRESS
                global RUP
                global LUP
                
                #keep player from falling through blocks
                if blktop - 2 <= (self.y + self.yoffset) + selfdimensions[1] and (self.y + self.yoffset) + selfdimensions[1] <= (blk.y + blk.yoffset) + blkdimensions[1] and blk.kind != 'l' and blk.kind != 'lb' and blk.kind != 'lt' and self.ladder == 0:
                        if (self.x + self.xoffset) + selfdimensions[0] > blkleft and self.x + self.xoffset < blkleft:
                                        playercaught = 1
                        elif self.x + self.xoffset < blkright and (self.x + self.xoffset) + selfdimensions[0] > blkright:
                                        playercaught = 1
                if blk.checkCollide(self) and blk.kind != 'l' and blk.kind != 'lb' and blk.kind != 'lt' and self.ladder == 0:
                        
##                        if self.ladder == 1:
##                                self.y = blk.y - self.height
##                                self.jv = 0
##                                self.canJump = 1
##                                self.fall = 0
##                                LPRESS = 1
##                                RPRESS = 1
##                                LUP = 1
##                                RUP = 1
##                                self.jumping = 0
##                                self.onGround = 1
##                                self.ladder = 0
                        self.y -= self.jv
                        
                        
                        #xcollision
                        if (self.x + self.xoffset) + selfdimensions[0] > blkleft and self.x + self.xoffset < blkleft and (self.y + self.yoffset) + selfdimensions[1] > blk.y + blk.yoffset and blk.kind != 'c': #and self.y + self.yoffset < blkbottom:
                                self.x -= self.xspeed 
                                self.wallflag = 1
                                while (self.x + self.xoffset) + selfdimensions[0] < blkleft-1:
                                        self.x += 1
                        elif self.x + self.xoffset < blkright and (self.x + self.xoffset) + selfdimensions[0] > blkright and (self.y + self.yoffset) + selfdimensions[1] > blk.y + blk.yoffset and blk.kind != 'c': #and self.y + self.yoffset < blkbottom:
                                self.x += self.xspeed
                                self.wallflag = 1
                                while self.x + self.xoffset > blkright+1:
                                        self.x -= 1
                        #ycollision
                        
                        if (self.y + self.yoffset) + selfdimensions[1] <= blktop:
                                while (self.y + self.yoffset) + selfdimensions[1] < blktop:
                                        self.y += 1
                                self.y = blk.y - self.height
                                self.jv = 0
                                self.canJump = 1
                                self.fall = 0
                                LPRESS = 1
                                RPRESS = 1
                                LUP = 1
                                RUP = 1
                                self.jumping = 0
                                self.onGround = 1
                        #hitting from bottom
                        elif self.y + self.yoffset > blkbottom and (self.x - self.xoffset) + selfdimensions[0] > (blkleft + 8) and self.x + self.xoffset < blkleft + 8 and blk.kind != 'w':
                                self.jv = 0
                        elif self.y + self.yoffset > blkbottom and self.x + self.xoffset < blkright - 5 and (self.x - self.xoffset) + selfdimensions[0] > blkright - 5 and blk.kind != 'w':
                                self.jv = 0
                        #if no prob, revert change
                        else:
                                self.y += self.jv

                #ladders
                elif blk.checkCollide(self) and blk.kind != 'c' and blk.kind != 'w' and blk.kind != 'b':
                        global UDOWN
                        global DDOWN
                        global UPRESS
                        global DPRESS
                        self.scrollu = 0
                        self.scrolld = 0
                        if UDOWN == 1 and blk.kind != 'lt':
                                self.ladder = 1
                                self.canJump = 1
                                self.ladderup = 1
                                self.x = blk.x - 2
                                if self.y < 256:
                                        self.scrollu = 1
                        elif DDOWN == 1 and blk.kind != 'lb':
                                self.ladderdown = 1
                                self.ladder = 1
                                self.canJump = 1
                                self.x = blk.x - 2
                                if self.y > 224:
                                        self.scrolld = 1
                        elif self.ladder == 1:
                                self.image.pause()
                        if UPRESS or DPRESS:
                                self.lanim = 1
##                        if (self.y + self.yoffset) + selfdimensions[1] <= blktop and blk.kind != 'l':
##                                self.y = blk.y - self.height
##                                self.jv = 0
##                                self.canJump = 1
##                                self.fall = 0
##                                LPRESS = 1
##                                RPRESS = 1
##                                LUP = 1
##                                RUP = 1
##                                self.jumping = 0
##                                self.onGround = 1
##                                self.ladder = 0
                        
        def playerFall(self, blk):
                blkdimensions = [blk.width,blk.height]
                selfdimensions = [self.width,self.height]
                blkbottom = (blk.y + blk.yoffset) + blkdimensions[1]
                blkright = (blk.x + blk.xoffset) + blkdimensions[0]
                blkright += 1
                blkleft = blk.x - blk.xoffset
                blktop = blk.y + blk.yoffset
                selfbottom = (self.y + self.yoffset) + selfdimensions[1]
                selfright = (self.x + self.xoffset) + selfdimensions[0]
                selfleft = self.x + self.xoffset
                selftop = self.y + self.yoffset
                global blktop
                global selfbottom
                global playercaught
                if self.ladder == 0:
                        if (self.x + self.xoffset) + selfdimensions[0] < blkleft or self.x + self.xoffset > blkright:
                                if playercaught == 0:
                                        self.fall = 1
                                        self.onGround = 0
                                        self.canJump = 0

        def update(self):
                if self.facing == 'left':
                        setDisplay.blit(self.shadow,(self.x-20,self.y-36))
                else:
                        setDisplay.blit(self.shadow,(self.x-24,self.y-36))
                self.image.blit(setDisplay,(self.x,self.y))
#end Player            
#Boss
class Boss(sprite):
    def _init_(self,simage):
        self.image = pygame.image.load(simage)
        self.glow = pygame.image.load('assets/sprites/boss/BOSS GLOWNEW.png')
        self.health = 60
        self.yspeed = 4
        self.xspeed = 8
        self.xoffset = 0
        self.yoffset = 0
        self.ymovement = 'none'
        self.xmovement = 'right'
        self.lasers = [bossproj(),bossproj(),bossproj()]
        
        self.dimensions = self.image.get_rect().size
        self.width = self.dimensions[0]
        self.height = self.dimensions[1]

        self.image = pyganim.PygAnimation([('assets/sprites/boss/BOSS TESTNEW1.png',0.05),('assets/sprites/boss/BOSS TESTNEW.png',0.05),('assets/sprites/boss/BOSS TESTNEW2.png',0.05),('assets/sprites/boss/BOSS TESTNEW.png',0.05)])
        self.image.play()
        
        self.x = bg[5].x + 320 - (int(self.dimensions[0] / 2))
        self.y = bg[5].y + 240 - (int(self.dimensions[1] / 2)) - 50
        self.animPos = 0
    def move(self, obj):
        anchorx = self.x + (int(self.dimensions[0] / 2))
        anchory = self.y + (int(self.dimensions[1] / 2))

        #r
        if anchorx >= bg[5].x + 264 and anchorx <= bg[5].x + 376 and self.xmovement == 'right':
            self.ymovement = 'none'
        #rd
        if anchorx >= bg[5].x + 376 and self.xmovement == 'right':
            self.ymovement = 'down'
        #lu
        if self.xmovement == 'right' and self.ymovement == 'down' and self.x + self.width >= bg[5].x + 640:
            self.xmovement = 'left'
            self.ymovement = 'up'
        #l
        if anchorx <= bg[5].x + 376 and anchorx >= bg[5].x + 264 and self.xmovement == 'left':
            self.ymovement = 'none'
        #ld
        if anchorx <= bg[5].x + 264 and self.xmovement == 'left':
            self.ymovement = 'down'
        #ru
        if self.xmovement == 'left' and self.ymovement == 'down' and self.x <= bg[5].x:
            self.xmovement = 'right'
            self.ymovement = 'up'

        #shooting
##        if self.movement == 'right' and self.ymovement == 'none' and self.x <= 37 and self.y > 33:
##                shot = 0
##                for i in range(len(self.lasers)):
##                        if shot == 0:
##                                if self.lasers[]


        #(program fireball here)
        #if self.ymovement == 'none' and (random number thang):
            #for i in range:
            #   if boss.fireball[i].ymovement == 'none':
            #           boss.fireball[i]._init_(anchorx, self.y + self.height)

        if self.xmovement == 'right':
            self.x += self.xspeed
        elif self.xmovement == 'left':
            self.x -= self.xspeed
        if self.ymovement == 'down':
            self.y += self.yspeed
        elif self.ymovement == 'up':
            self.y -= self.yspeed
        

        if self.checkCollide(obj):
            obj.dead = 1
        if self.health <= 0:
                global WIN
                WIN = 1
                pygame.mixer.music.load('assets/sounds/youwin.wav')
                pygame.mixer.music.play()
                winimg.image.play()
                self.x = -128
                self.y = -128
                self.xspeed = 0
                self.yspeed = 0

    def update(self):
            setDisplay.blit(self.glow,(self.x-26,self.y-26))
            self.image.blit(setDisplay,(self.x,self.y))
#end boss

#bossproj
class bossproj(sprite):
        def _init_(self,x,y,sy):
                self.yspeed = 5
                self.xspeed = 24

                self.ymovement = sy
                self.movechange = 1
                self.health = 1
                
                self.x = x
                self.y = y
                self.image = pygame.image.load('assets/sprites/projectiles/projectile1.png').convert_alpha()

                self.color

                self.dimensions = self.image.get_rect().size
                self.xoffset = 0
                self.yoffset = 0
                self.width = self.dimensions[0]
                self.height = self.dimensions[1]
                
                self.dead = 0
                self.animPos = 0
        def move(self, obj, blk):
                if self.ymovement == 'down':
                        self.y += self.yspeed
                if self.checkCollide(obj) and self.dead == 0:
                        obj.dead = 1
                elif self.checkCollide(blk):
                        self.dead = 1
                        self.ymovement = 'none'
                        self.x, self.y = -32, -32
#end bossproj
            
#block
class block(sprite):
        def _init_(self,sx,sy,simage,kind):
                self.x = sx
                self.y = sy
                self.image = pygame.image.load(simage)
                self.dimensions = self.image.get_rect().size
                self.width = self.dimensions[0]
                self.height = self.dimensions[1]
                self.yspeed = 10
                self.xspeed = 16
                self.ymovement = 'none'
                self.xmovement = 'none'
                self.xoffset = 0
                self.yoffset = 0
                if kind == 0:
                    self.kind = 'b'
                elif kind == 1:
                    self.kind = 'w'
                elif kind == 2:
                    self.kind = 'c'
                elif kind == 3:
                        self.kind = 'l'
                elif kind == 4:
                        self.kind = 'lb'
                elif kind == 5:
                        self.kind = 'lt'
#end block



def scroll():
                scrollspeed = 8
                #right side
                if player1.scrollr and bg[3].x > 0 and SONG != 'Tutorial' and player1.checkCollide(bg[5]) == 0: 
                        bg[0].x -= scrollspeed
                        if boss != 0:
                                boss.x -= scrollspeed
                        for l in range(len(bg)):
                                for i in range(len(bg[l].blocks)):
                                                if bg[l].blocks[i] != 0:
                                                        bg[l].blocks[i].x -= scrollspeed
                                for i in range(len(bg[l].enemies)):
                                        if bg[l].enemies[i] != 0:
                                                bg[l].enemies[i].x -= scrollspeed
                        if RDOWN:
                                player1.x -= player1.xspeed
                        bg[1].x = bg[0].x + bg[0].width
                        bg[2].x = bg[1].x + bg[1].width
                        bg[3].x = bg[2].x
                        bg[4].x = bg[1].x
                        bg[5].x = bg[0].x
                        if player1.x > 384:
                                player1.x -= scrollspeed
                #left side
                elif player1.scrolll and bg[0].x < 0:
                        bg[0].x += scrollspeed
                        if boss != 0:
                                boss.x += scrollspeed
                        for l in range(len(bg)):
                                for i in range(len(bg[l].blocks)):
                                                 if bg[l].blocks[i] != 0:
                                                        bg[l].blocks[i].x += scrollspeed
                                for i in range(len(bg[l].enemies)):
                                        if bg[l].enemies[i] != 0:
                                                bg[l].enemies[i].x += scrollspeed
                        if LDOWN:
                                player1.x += player1.xspeed
                        bg[1].x = bg[0].x + bg[0].width
                        bg[2].x = bg[1].x + bg[1].width
                        bg[3].x = bg[2].x
                        bg[4].x = bg[1].x
                        bg[5].x = bg[0].x
                global scrolling
                if player1.checkCollide(bg[0]) == 0:
                        scrolling = 0
                #vertical up
                if player1.scrollu == 1 and bg[0].y < 480 and SONG != 'Tutorial':
                        bg[0].y += scrollspeed
                        if boss != 0:
                                boss.y += scrollspeed
                        for l in range(len(bg)):
                                for i in range(len(bg[l].blocks)):
                                                if bg[l].blocks[i] != 0:
                                                        bg[l].blocks[i].y += scrollspeed
                                for i in range(len(bg[l].enemies)):
                                        if bg[l].enemies[i] != 0:
                                                bg[l].enemies[i].y += scrollspeed
                        if UDOWN:
                                player1.y += 8
                        bg[1].y = bg[0].y
                        bg[2].y = bg[0].y
                        bg[3].y = bg[2].y - bg[3].height
                        bg[4].y = bg[3].y
                        bg[5].y = bg[4].y
                #vertical down
                if player1.scrolld == 1 and bg[0].y > 0 and SONG != 'Tutorial':
                        bg[0].y -= scrollspeed
                        if boss != 0:
                                boss.y -= scrollspeed
                        for l in range(len(bg)):
                                for i in range(len(bg[l].blocks)):
                                                if bg[l].blocks[i] != 0:
                                                        bg[l].blocks[i].y -= scrollspeed
                                for i in range(len(bg[l].enemies)):
                                        if bg[l].enemies[i] != 0:
                                                bg[l].enemies[i].y -= scrollspeed
                        if DDOWN:
                                player1.y -= 8
                        bg[1].y = bg[0].y
                        bg[2].y = bg[0].y
                        bg[3].y = bg[2].y - bg[3].height
                        bg[4].y = bg[3].y
                        bg[5].y = bg[4].y
                #tutorial scroll
                elif player1.checkCollide(bg[0]) and player1.x > 544:
                        scrolling = 1
                if scrolling and bg[0].x + bg[0].width == 96:
                        scrolling = 0
                        player1.xspeed = 8
                        if SONG == 'Tutorial':
                                global SONG
                                SONG = 'Level1'
                                level1.play()
                                Tutorial.fadeout(3000)
                if scrolling:
                        player1.xspeed = 0
                        if bg[0].x + bg[0].width > 96:
                                bg[0].x -= 32
                                if boss != 0:
                                        boss.x -= 32
                                for l in range(len(bg)):
                                        for i in range(len(bg[l].blocks)):
                                                        if bg[l].blocks[i] != 0:
                                                                bg[l].blocks[i].x -= 32
                                        for i in range(len(bg[l].enemies)):
                                                if bg[l].enemies[i] != 0:
                                                        bg[l].enemies[i].x -= 32
                                
                                player1.x -= 32
                                bg[1].x = bg[0].x + bg[0].width
                                bg[2].x = bg[1].x + bg[1].width
                                bg[3].x = bg[2].x
                                bg[4].x = bg[1].x
                                bg[5].x = bg[0].x
                                
def reset():
        pygame.mixer.stop()
        global bg
        global player1
        global boss
        global title
        global titleimg
        global pausedim
        global pause
        global block1
        global block2
        global blocks
        global RUP
        global LUP
        global bosstimer
        global winimg
        bosstimer = 0
        LUP = 0
        RUP = 1
        title = 1
        boss = 0
        block1 = 0
        block2 = 0
        bg = [sprite(),sprite(),sprite(),sprite(),sprite(),sprite()]
        #----------------------
        bg[0]._init_(0,0,'assets/sprites/bg/bg1.png')
        bg[0].enemies = [0]
        def initenemies(obj):
                if bg[0].enemies[0] == 0:
                        bg[0].enemies[0] = enemy()
                        bg[0].enemies[0]._init_(424,96,384,480,bg[0])
                elif bg[0].x + bg[0].width > 0 or bg[0].x < 640:
                        bg[0].enemies[0] = enemy()
                        bg[0].enemies[0]._init_(424,96,384,480,bg[0])
                bg[0].enemies[0] = enemy()
                bg[0].enemies[0]._init_(424,96,384,480,bg[0])
                
        bg[0].initenemies = MethodType(initenemies, bg[0])
        bg[0].initenemies()

        #----------------------
        bg[1]._init_(bg[0].x + bg[0].width,0,'assets/sprites/bg/bg2.png')
        bg[1].enemies = [enemy(),enemy()]
        def initenemies(obj):
                if bg[1].enemies == 0:
                        bg[1].enemies = [enemy(),enemy()]
                        bg[1].enemies[0]._init_(544,288,128,736,bg[1])
                        bg[1].enemies[1]._init_(480,288,128,736,bg[1])
                elif bg[1].x + bg[1].width > 0 or bg[1].x < 640:
                        bg[1].enemies = [enemy(),enemy()]
                        bg[1].enemies[0]._init_(544,288,128,736,bg[1])
                        bg[1].enemies[1]._init_(480,288,128,736,bg[1])
        bg[1].initenemies = MethodType(initenemies, bg[1])
        bg[1].initenemies
        
        #----------------------
        bg[2]._init_(bg[1].x + bg[1].width,0,'assets/sprites/bg/bg3.png')
        bg[2].enemies = [0]
        def initenemies(obj):
                h = 1
        bg[2].initenemies = MethodType(initenemies, bg[2])
        
        #----------------------
        bg[3]._init_(bg[2].x ,-480,'assets/sprites/bg/bg4.png')
        bg[3].enemies = [0]
        def initenemies(obj):
                h = 1
        bg[3].initenemies = MethodType(initenemies, bg[3])
        
        #----------------------
        bg[4]._init_(bg[3].x - 640,-480,'assets/sprites/bg/bg5.png')
        bg[4].enemies = [0]
        def initenemies(obj):
                h = 1
        bg[4].initenemies = MethodType(initenemies, bg[4])
        
        #----------------------     
        bg[5]._init_(bg[4].x - 640,-480,'assets/sprites/bg/bg6.png')
        bg[5].enemies = [0]
        def initenemies(obj):
                h = 1
        bg[5].initenemies = MethodType(initenemies, bg[5])

        
        winimg = sprite()
        winimg._init_(0,0,'assets/sprites/bg/win.png')
        winimg.image = pyganim.PygAnimation([('assets/sprites/bg/win.png',0.1),('assets/sprites/bg/win2.png',0.1)])
        player1 = player()
        player1._init_(50,288,'assets/sprites/player/idle.png')
        
        titleimg = sprite()
        titleimg._init_(0,0,'assets/sprites/bg/title.png')
        titleimg.image = pyganim.PygAnimation([('assets/sprites/bg/Title1.png',0.5),('assets/sprites/bg/Title2.png',0.5)])
        titleimg.image.play()
        pausedim = sprite()
        pausedim._init_(0,0,'assets/sprites/bg/pausedim.png')
        Tutorial.stop()#winsound.PlaySound("sounds/silencer.wav",winsound.SND_ASYNC)
        level1.stop()
        suspense.stop()
        pygame.mixer.music.stop()
        
        pause = 0
        #block1 = block()
        #block1._init_(200,240,'assets/sprites/bg/block.png')
        bg[0].blocks = [0] * 300
        blocklayout1 = [0,0,0,0,0,0,4,4,4,4,4,4,4,4,4,4,4,4,4,3,
                        0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,3,0,0,0,0,0,0,1,1,1,1,0,1,1,1,
                        4,4,4,4,4,4,1,1,0,0,0,0,0,0,0,0,0,3,0,3,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,3,
                        0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,3,0,3,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,3,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,3,
                        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,3,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3]
        col = 0
        row = 0
        for i in range(len(blocklayout1)):
                if col > 19:
                        col = 0
                        row += 1
                if row > 14:
                        row = 0
                if blocklayout1[i] == 1:
                        bg[0].blocks[i] = block()
                        bg[0].blocks[i]._init_(bg[0].x + (col*32),bg[0].y + (row*32),'assets/sprites/bg/block.png',0)
                        bg[0].blocks[i].name = "bg[0].blocks[" + str(i) + "]"
                elif blocklayout1[i] == 3:
                    bg[0].blocks[i] = block()
                    bg[0].blocks[i]._init_(bg[0].x + (col*32),bg[0].y + (row*32),'assets/sprites/bg/block.png',1)
                    bg[0].blocks[i].name = "bg[0].blocks[" + str(i) + "]"
                elif blocklayout1[i] == 4:
                    bg[0].blocks[i] = block()
                    bg[0].blocks[i]._init_(bg[0].x + (col*32),bg[0].y + (row*32),'assets/sprites/bg/block.png',2)
                    bg[0].blocks[i].name = "bg[0].blocks[" + str(i) + "]"
                col += 1
        bg[1].blocks = [0] * 300
        blocklayout2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,1,4,4,4,4,4,4,1,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                        0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        col = 0
        row = 0
        for i in range(len(blocklayout2)):
                if col > 19:
                        col = 0
                        row += 1
                if row > 14:
                        row = 0
                if blocklayout2[i] == 1:
                        bg[1].blocks[i] = block()
                        bg[1].blocks[i]._init_(bg[1].x + (col*32),bg[1].y + (row*32),'assets/sprites/bg/block.png',0)
                        bg[1].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                elif blocklayout2[i] == 3:
                    bg[1].blocks[i] = block()
                    bg[1].blocks[i]._init_(bg[1].x + (col*32),bg[1].y + (row*32),'assets/sprites/bg/block.png',1)
                    bg[1].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                elif blocklayout2[i] == 4:
                    bg[1].blocks[i] = block()
                    bg[1].blocks[i]._init_(bg[1].x + (col*32),bg[1].y + (row*32),'assets/sprites/bg/block.png',2)
                    bg[1].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                col += 1
        #1 = normal block, 2 = placeholder for debug, 3 = wall, 4 = ceiling, 5 = ladder middle, 6 = ladder bottom (up 1 block) 7 = ladder top (down 1 block)
        bg[2].blocks = [0] * 300
        blocklayout3 = [0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,
                        1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,
                        0,0,0,3,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,3,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,3,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0]
        col = 0
        row = 0
        for i in range(len(blocklayout2)):
                if col > 19:
                        col = 0
                        row += 1
                if row > 14:
                        row = 0
                if blocklayout3[i] == 1:
                        bg[2].blocks[i] = block()
                        bg[2].blocks[i]._init_(bg[2].x + (col*32),bg[2].y + (row*32),'assets/sprites/bg/block.png',0)
                        bg[2].blocks[i].name = "bg[2].blocks[" + str(i) + "]"
                elif blocklayout3[i] == 3:
                    bg[2].blocks[i] = block()
                    bg[2].blocks[i]._init_(bg[2].x + (col*32),bg[2].y + (row*32),'assets/sprites/bg/block.png',1)
                    bg[2].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                elif blocklayout3[i] == 4:
                    bg[2].blocks[i] = block()
                    bg[2].blocks[i]._init_(bg[2].x + (col*32),bg[2].y + (row*32),'assets/sprites/bg/block.png',2)
                    bg[2].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                elif blocklayout3[i] == 5:
                    bg[2].blocks[i] = block()
                    bg[2].blocks[i]._init_(bg[2].x + (col*32),bg[2].y + (row*32),'assets/sprites/bg/ladder.png',3)
                    bg[2].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                elif blocklayout3[i] == 6:
                    bg[2].blocks[i] = block()
                    bg[2].blocks[i]._init_(bg[2].x + (col*32),bg[2].y + (row*32),'assets/sprites/bg/block.png',4)
                    bg[2].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                elif blocklayout3[i] == 7:
                    bg[2].blocks[i] = block()
                    bg[2].blocks[i]._init_(bg[2].x + (col*32),bg[2].y + (row*32),'assets/sprites/bg/block.png',5)
                    bg[2].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                col += 1
        bg[3].blocks = [0] * 300
        blocklayout4 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,1,5,1,1,1,1,3,0,0,0,
                        0,1,1,1,1,0,0,0,0,0,0,5,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,0,0]
        col = 0
        row = 0
        for i in range(len(blocklayout4)):
                if col > 19:
                        col = 0
                        row += 1
                if row > 14:
                        row = 0
                if blocklayout4[i] == 1:
                        bg[3].blocks[i] = block()
                        bg[3].blocks[i]._init_(bg[3].x + (col*32),bg[3].y + (row*32),'assets/sprites/bg/block.png',0)
                        bg[3].blocks[i].name = "bg[2].blocks[" + str(i) + "]"
                elif blocklayout4[i] == 3:
                    bg[3].blocks[i] = block()
                    bg[3].blocks[i]._init_(bg[3].x + (col*32),bg[3].y + (row*32),'assets/sprites/bg/block.png',1)
                    bg[3].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                elif blocklayout4[i] == 4:
                    bg[3].blocks[i] = block()
                    bg[3].blocks[i]._init_(bg[3].x + (col*32),bg[3].y + (row*32),'assets/sprites/bg/block.png',2)
                    bg[3].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                elif blocklayout4[i] == 5:
                    bg[3].blocks[i] = block()
                    bg[3].blocks[i]._init_(bg[3].x + (col*32),bg[3].y + (row*32),'assets/sprites/bg/ladder.png',3)
                    bg[3].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                elif blocklayout4[i] == 6:
                    bg[3].blocks[i] = block()
                    bg[3].blocks[i]._init_(bg[3].x + (col*32),bg[3].y + (row*32),'assets/sprites/bg/block.png',4)
                    bg[3].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                elif blocklayout4[i] == 7:
                    bg[3].blocks[i] = block()
                    bg[3].blocks[i]._init_(bg[3].x + (col*32),bg[3].y + (row*32),'assets/sprites/bg/block.png',5)
                    bg[3].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                col += 1
        bg[4].blocks = [0] * 300
        blocklayout5 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        col = 0
        row = 0
        for i in range(len(blocklayout4)):
                if col > 19:
                        col = 0
                        row += 1
                if row > 14:
                        row = 0
                if blocklayout5[i] == 1:
                        bg[4].blocks[i] = block()
                        bg[4].blocks[i]._init_(bg[4].x + (col*32),bg[3].y + (row*32),'assets/sprites/bg/block.png',0)
                        bg[4].blocks[i].name = "bg[2].blocks[" + str(i) + "]"
                elif blocklayout5[i] == 3:
                    bg[4].blocks[i] = block()
                    bg[4].blocks[i]._init_(bg[4].x + (col*32),bg[3].y + (row*32),'assets/sprites/bg/block.png',1)
                    bg[4].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                elif blocklayout5[i] == 4:
                    bg[4].blocks[i] = block()
                    bg[4].blocks[i]._init_(bg[4].x + (col*32),bg[3].y + (row*32),'assets/sprites/bg/block.png',2)
                    bg[4].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                elif blocklayout5[i] == 5:
                    bg[4].blocks[i] = block()
                    bg[4].blocks[i]._init_(bg[4].x + (col*32),bg[3].y + (row*32),'assets/sprites/bg/ladder.png',3)
                    bg[4].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                elif blocklayout5[i] == 6:
                    bg[4].blocks[i] = block()
                    bg[4].blocks[i]._init_(bg[4].x + (col*32),bg[3].y + (row*32),'assets/sprites/bg/block.png',4)
                    bg[4].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                elif blocklayout5[i] == 7:
                    bg[4].blocks[i] = block()
                    bg[4].blocks[i]._init_(bg[4].x + (col*32),bg[3].y + (row*32),'assets/sprites/bg/block.png',5)
                    bg[4].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                col += 1
        bg[5].blocks = [0] * 300
        blocklayout6 = [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,
                        3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,
                        3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,
                        3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,
                        3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,
                        3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,
                        3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,
                        3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,
                        3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,
                        3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3]
        col = 0
        row = 0
        for i in range(len(blocklayout6)):
                if col > 19:
                        col = 0
                        row += 1
                if row > 14:
                        row = 0
                if blocklayout6[i] == 1:
                        bg[5].blocks[i] = block()
                        bg[5].blocks[i]._init_(bg[5].x + (col*32),bg[3].y + (row*32),'assets/sprites/bg/block.png',0)
                        bg[5].blocks[i].name = "bg[2].blocks[" + str(i) + "]"
                elif blocklayout6[i] == 3:
                    bg[5].blocks[i] = block()
                    bg[5].blocks[i]._init_(bg[5].x + (col*32),bg[3].y + (row*32),'assets/sprites/bg/block.png',1)
                    bg[5].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                elif blocklayout6[i] == 4:
                    bg[5].blocks[i] = block()
                    bg[5].blocks[i]._init_(bg[5].x + (col*32),bg[3].y + (row*32),'assets/sprites/bg/block.png',2)
                    bg[5].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                elif blocklayout6[i] == 5:
                    bg[5].blocks[i] = block()
                    bg[5].blocks[i]._init_(bg[5].x + (col*32),bg[3].y + (row*32),'assets/sprites/bg/ladder.png',3)
                    bg[5].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                elif blocklayout6[i] == 6:
                    bg[5].blocks[i] = block()
                    bg[5].blocks[i]._init_(bg[5].x + (col*32),bg[3].y + (row*32),'assets/sprites/bg/block.png',4)
                    bg[5].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                elif blocklayout6[i] == 7:
                    bg[5].blocks[i] = block()
                    bg[5].blocks[i]._init_(bg[5].x + (col*32),bg[3].y + (row*32),'assets/sprites/bg/block.png',5)
                    bg[5].blocks[i].name = "bg[1].blocks[" + str(i) + "]"
                col += 1
def winimgupdate():
        winimg.image.blit(setDisplay,(winimg.x,winimg.y))


reset()
scrolling = 0

#gameloop
while 1:
        setDisplay.fill((0,0,0))
        checkEvent()
        if title == 0 and pause == 0 and WIN == 0:
                
                scroll()
                for i in range(len(bg)):
                        #if bg is offscreen, all enemies therof are reset
                        if bg[i].x < 640 and bg[i].x > -640 and bg[i].y < 480 and bg[i].y > -480:
                                bg[i].update()
                        else:
                                        bg[i].initenemies()
                                #bg[i].instructions.update()
                for l in range(len(bg)):
                        for i in range(len(bg[l].enemies)):
                                if bg[l].enemies[i] != 0:
                                        bg[l].enemies[i].chase(player1)
                                        if bg[l].enemies[i].gib != 0:
                                                for j in range(len(bg[l].enemies[i].gib)):
                                                        if bg[l].enemies[i].gib[j] != 0: 
                                                                bg[l].enemies[i].gib[j].fly()
                                                                bg[l].enemies[i].gib[j].update()
                                                                if bg[l].enemies[i].gib[j].dead:
                                                                        bg[l].enemies[i].gib[j] = 0
                                                                
                                                                if bg[l].enemies[i].explosion != 0:
                                                                        bg[l].enemies[i].explosion.animate()
                                                                        bg[l].enemies[i].explosion.update()
                                                                        if bg[l].enemies[i].explosion.dead == 1:
                                                                                bg[l].enemies[i].explosion = 0
                                        if bg[l].enemies[i].x + bg[l].enemies[i].width > 0 and bg[l].enemies[i].x < 640:
                                                bg[l].enemies[i].update()
                        
                                        for j in range (len(player1.laser)):
                                                player1.laser[j].kill(bg[l].enemies[i])
                                        if bg[l].enemies[i].dead == 0:
                                                bg[l].enemies[i].kill(player1)
                
                if player1.checkCollide(bg[5]) and bg[5].x == 0 and boss == 0:
                        if bosstimer == 210:
                                boss = Boss()
                                boss._init_('assets/sprites/boss/BOSS TESTNEW.png')
                                suspense.stop()
                                pygame.mixer.music.play()
                                global SONG
                                SONG = 'Boss'
                                boss.healthbar = Rect(416,32,32,boss.health*2)
                                boss.healthbaroverlay = sprite()
                                boss.healthbaroverlay._init_(576,30,'assets/sprites/boss/healthbar.png')
                                del stone
                        elif bosstimer == 0:
                                level1.fadeout(5000)
                                block1 = block()
                                block1._init_(bg[5].x + 608,bg[5].y + 288,'assets/sprites/bg/ladder.png',1)
                                block2 = block()
                                block2._init_(bg[5].x + 608,bg[5].y + 320,'assets/sprites/bg/ladder.png',1)
                                stone = pygame.mixer.Sound('assets/sounds/stone.wav')
                                stone.play()
                                bg[5].image = pygame.image.load('assets/sprites/bg/bg62.png')
                        elif bosstimer == 60:
                                suspense.play()
                                
                        bosstimer += 1
                elif boss != 0:
                        boss.healthbar = Rect(576,150-(boss.health*2),16,boss.health*2)
                        
                        if boss.health != 0:
                                pygame.draw.rect(setDisplay, (110,60,196), boss.healthbar, 0)
                                boss.healthbaroverlay.update()
                        boss.move(player1)
                        #boss.anim()
                        boss.update()
                
                #block1.update()
        
                player1.control()
                player1.gravity()
                #block1.correctPlayer(player1)
                playercaught = 0
                player1.wallflag = 0
                player1.ladderup = 0
                player1.ladderdown = 0
                #update every block of every screen
                for l in range(len(bg)):
                        #if bg is offscreen, all enemies therof are reset
                        
                        for i in range(len(bg[l].blocks)):
                                if bg[l].blocks[i] != 0:
                                        if bg[l].blocks[i].x < 640 and bg[l].blocks[i].x > -640:
                                                player1.correctPlayer(bg[l].blocks[i])
                                                #bg[l].blocks[i].update()
                #this function must come after every block has finished the above functions
                for l in range(len(bg)):
                        for i in range(len(bg[l].blocks)):
                                if bg[l].blocks[i] != 0:
                                        if bg[l].blocks[i].x < 640 and bg[l].blocks[i].x > -640:
                                                player1.playerFall(bg[l].blocks[i])
                
                if player1.ladderup:
                        player1.y -= 8
                elif player1.ladderdown:
                        player1.y += 8
                #boss room door
                if block1 != 0:
                        player1.correctPlayer(block2)
                        player1.correctPlayer(block1)
                
                player1.colour()
                player1.anim()
                player1.update()
                for i in range (len(player1.laser)):
                        player1.laser[i].move()
                        player1.laser[i].checkOOB()
                        player1.laser[i].color(player1)
                        player1.laser[i].anim()
                        if boss != 0:
                                player1.laser[i].kill(boss)
                        if player1.laser[i].x + player1.laser[i].width > 0 and player1.laser[i].x < 640:
                                player1.laser[i].update()
                
        
        
                if XCOOL > 0:
                        XCOOL -= 1

                
                
        elif title == 1 and pause == 0 and WIN == 0:           
                titleimg.image.blit(setDisplay,(titleimg.x,titleimg.y))
        elif WIN == 0:
                for i in range(len(bg)):
                        if bg[i].x < 640 and bg[i].x > -640:
                                bg[i].update()
                
                for i in range(len(player1.laser)):
                        player1.laser[i].update()
                        player1.laser[i].image.pause()
                if boss != 0 :
                        boss.update()
                        boss.image.pause()
                player1.image.pause()
                
                for l in range(len(bg)):
                        for i in range(len(bg[l].enemies)):
                                if bg[l].enemies[i] != 0:
                                        if bg[l].enemies[i].gib != 0:
                                                for j in range(len(bg[l].enemies[i].gib)):
                                                        if bg[l].enemies[i].gib[j] != 0: 
                                                                bg[l].enemies[i].gib[j].update()
                                                                
                                                                if bg[l].enemies[i].explosion != 0:
                                                                        bg[l].enemies[i].explosion.update()
                                        if bg[l].enemies[i].x + bg[l].enemies[i].width > 0 and bg[l].enemies[i].x < 640:
                                                bg[l].enemies[i].image.pause()
                                                bg[l].enemies[i].update()

                if boss != 0:
                        pygame.draw.rect(setDisplay, (110,60,196), boss.healthbar, 0)
                        boss.healthbaroverlay.update()
                player1.update()
                #for i in range(len(bg[l].blocks)):
                        #if bg[l].blocks[i] != 0:
                                #if bg[l].blocks[i].x < 640 and bg[l].blocks[i].x > -640:
                                                #bg[l].blocks[i].update()
                pausedim.update()
        elif WIN:
                
                winimgupdate()
        pygame.display.update()
        fpsTime.tick(FPS)
quit
#reserved for projectile movement
#def move(self):
#                if self.y > 592:
#                        self.ymovement = 'up'
#                if self.y <= 0:
#                        self.ymovement = 'down'
#                if self.ymovement == 'down':
#                        self.y += self.yspeed
#
#                elif self.ymovement == 'up':
#                        self.y -= self.yspeed
#
#                if self.x >= 576:
#                        self.xmovement = 'left'
#                elif self.x <= 0:
#                        self.xmovement = 'right'
#                if self.xmovement == 'right':
#                        self.x += self.xspeed
#                elif self.xmovement == 'left':
#                        self.x -= self.xspeed
#end move()

#imgrotation
#self.image = pygame.transform.rotate(self.image, 90)
