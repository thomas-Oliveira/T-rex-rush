from pygame import *
import pygame
import os

from load_sprite_sheet import load_sprite_sheet

class ground(pygame.sprite.Sprite): 
    def __init__(self, startpos, sizex=-1,sizey=-1): 
        pygame.sprite.Sprite.__init__(self) 
        #direcao: 1=direita, -1=esquerda 
        self.direction = -1 #carrega a imagem e a posiciona na tela 
        self.images, self.rect = load_sprite_sheet("ground.png",1,1,sizex,sizey,-1)
        self.images1, self.rect1 = load_sprite_sheet("ground.png",1,1,sizex,sizey,-1)
        self.images, self.images1 = self.images[0], self.images1[0]
        self.speed = -5
        self.rect1.left = self.rect.right
        self.rect.centerx = startpos[0]
        self.rect.centery = startpos[1]
        self.rect1.centerx = self.rect.right
        self.rect1.centery = startpos[1]
    
    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right
            if self.speed < 10:
                self.speed += -1

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right
            if self.speed < 10:
                self.speed += -1


    def draw(self, screen):
        screen.blit(self.images, self.rect)
        screen.blit(self.images1, self.rect1)

        