from pygame import *
import pygame
import os

from load_sprite_sheet import load_sprite_sheet


class dino(pygame.sprite.Sprite): 
    def __init__(self, startpos, sizex=-1,sizey=-1): 
        pygame.sprite.Sprite.__init__(self) 
        #direcao: 1=direita, -1=esquerda 
        self.direction = -1 #carrega a imagem e a posiciona na tela 
        self.images, self.rect = load_sprite_sheet("dino.png",5,1,sizex,sizey,-1)
        self.images1,self.rect1 = load_sprite_sheet('dino_ducking.png',2,1,59,sizey,-1)
        self.down = False
        self.jump = False
        self.jump_force = self.jump_force_base = 20
        self.state_image = 0
        self.wait = self.wait_base = 5
        self.state_time_image = self.state_time_image_base = 3
        self.image = self.images[self.state_image]
        self.rect.centerx = startpos[0]
        self.rect.centery = startpos[1]
        self.centery = self.rect.centery
        self.score = 0
        self.update_flag = True
    
    def update_score(self, obstaculo):
        if self.rect.centerx > obstaculo.rect.centerx and obstaculo.rect.centerx < 0 and self.update_flag:
            self.score += 1

    def is_collided_with(self, sprite):
        return self.rect.collidepoint(sprite.rect.centerx, sprite.rect.centery)

    def dino_dead(self):
        self.rect.centerx = 40
        self.rect.centery = 40
        self.update_flag = False

    def update(self):
        if self.update_flag:
            if self.jump and self.jump_force >= -self.jump_force_base :
                self.rect.centery -= (self.jump_force * abs(self.jump_force)) * 0.03
                self.jump_force -= 1
            else:
                self.rect.centery = self.centery
                self.jump_force = self.jump_force_base 
                self.jump = False

            if self.down:
                self.jump = False
                self.rect.centery = self.centery
                self.state_image = ((self.state_image + 1) % len(self.images1)) if self.wait < 0 or self.wait == self.wait_base else self.state_image
                self.image = self.images1[self.state_image]
                self.wait = self.wait - 1 if self.wait > 0 else self.wait_base
            else:
                self.state_image = (self.state_image + 1)%len(self.images)
                self.image = self.images[self.state_image]
                self.wait = self.wait_base


        