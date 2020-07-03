from pygame import *
import pygame
import random
import os

from load_sprite_sheet import load_sprite_sheet

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self,startpos, sizex=-1,sizey=-1, speed=5):
        self.sprite_tip = False # 0: ptera 1:cacti_small 2:cacti_big
        if random.randint(0,2) == 0:
            self.images, self.rect = load_sprite_sheet('cacti-small.png',3,1,sizex,sizey,-1)
            self.sprite_tip = 100
        elif random.randint(0,2) == 1:
            self.images, self.rect = load_sprite_sheet('cacti-big.png',3,1,sizex,sizey+20,-1)
            self.sprite_tip = 200
        else:
            self.images, self.rect = load_sprite_sheet('ptera.png',2,1,sizex,sizey,-1)
            self.sprite_tip = 300
        self.sizex = sizex
        self.sizey = sizey
        self.state_image = 0 if self.sprite_tip == 300 else random.randrange(0,3)
        self.image = self.images[self.state_image]
        self.wait = self.wait_base = 5
        self.movement = [-1*speed,0]
        self.rect.centerx = startpos[0]
        self.rect.centery = startpos[1]
        if self.sprite_tip == 300:
            self.rect.centery = startpos[1] - random.randrange(1,10)*10
        self.startpos = startpos
        self.speed = -1*speed
        self.dino_passado = []

    def reset(self):
        self.rect.centerx = self.startpos[0]
        self.rect.centery = self.startpos[1]
        if random.randint(0,2) == 0:
            self.images, self.rect = load_sprite_sheet('cacti-small.png',3,1,self.sizex,self.sizey,-1)
            self.sprite_tip = 100
        elif random.randint(0,2) == 1:
            self.images, self.rect = load_sprite_sheet('cacti-big.png',3,1,self.sizex,self.sizey+20,-1)
            self.sprite_tip = 200
        else:
            self.images, self.rect = load_sprite_sheet('ptera.png',2,1,self.sizex,self.sizey,-1)
            self.sprite_tip = 300
        self.state_image = 0 if self.sprite_tip == 300 else random.randrange(0,3)
        self.image = self.images[self.state_image]
        self.rect.centerx = self.startpos[0]
        self.rect.centery = self.startpos[1]
        if self.sprite_tip == 300:
            self.rect.centery = self.startpos[1] - random.randrange(1,10)*10

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def obstaculo_set_speed(self, speed):
        self.speed = speed

    def update(self):
        self.rect.left += self.speed
        if self.sprite_tip == 300:
            self.rect.left += self.speed
            self.state_image = (self.state_image + 1) % len(self.images) if self.wait < 0 or self.wait == self.wait_base   else self.state_image
            self.image = self.images[self.state_image]
            self.wait = self.wait - 1 if self.wait > 0 else self.wait_base
        else:
            self.wait = self.wait_base

        if self.rect.right < 0:
            if random.randint(0,2) == 0:
                self.images, self.rect = load_sprite_sheet('cacti-small.png',3,1,self.sizex,self.sizey,-1)
                self.sprite_tip = 100
            elif random.randint(0,2) == 1:
                self.images, self.rect = load_sprite_sheet('cacti-big.png',3,1,self.sizex,self.sizey+20,-1)
                self.sprite_tip = 200
            else:
                self.images, self.rect = load_sprite_sheet('ptera.png',2,1,self.sizex,self.sizey,-1)
                self.sprite_tip = 300
            self.state_image = 0 if self.sprite_tip == 300 else random.randrange(0,3)
            self.image = self.images[self.state_image]
            self.rect.centerx = self.startpos[0]
            self.rect.centery = self.startpos[1]
            if self.sprite_tip == 300:
                self.rect.centery = self.startpos[1] - random.randrange(1,10)*10
            self.dino_passado = []