from pygame import *
import pygame
import os
import numpy as np

from load_sprite_sheet import load_sprite_sheet


class dino_IA(pygame.sprite.Sprite): 
    def __init__(self, id, startpos, sizex=-1,sizey=-1, neuronios=np.random.uniform(-10, 10, (3, 9))): 
        #direcao: 1=direita, -1=esquerda 
        self.id = id
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
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery
        self.score = 0
        self.update_flag = True
        self.startpos = startpos

        self.best = False
        self.fitness = 0
        self.neuronios = neuronios
        self.bias = 0.01
        self.proximo_obstaculo_ind = 0


    def reset(self):
        self.update_flag = True
        self.score = 0
        self.rect.centerx = self.startpos[0]
        self.rect.centery = self.startpos[1]

    def update_score(self, obstaculo):
        if self.update_flag:
            if self.rect.centerx > obstaculo.rect.centerx and self.id not in obstaculo.dino_passado:
                self.score += 1
                obstaculo.dino_passado.append(self.id)

        if self.score >= self.fitness:
            self.fitness = self.score

    def is_collided_with(self, sprite):
        return self.rect.collidepoint(sprite.rect.centerx, sprite.rect.centery)

    def dino_dead(self, obstaculo):
        if self.is_collided_with(obstaculo):
            self.rect.centerx = 120
            self.rect.centery = 40
            self.update_flag = False
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_neuronios(self, populacao):
        self.neuronios = populacao[self.id]

    def obj_proximo(self, obstaculo, obstaculo2):
        xb1, yb1 = obstaculo.rect.centerx, obstaculo.rect.centery
        xb2, yb2 = obstaculo2.rect.centerx, obstaculo2.rect.centery
        if np.sqrt( (xb1 - self.rect.centerx)**2 + (yb1 - self.rect.centery)**2) < np.sqrt( (xb2 - self.rect.centerx)**2 + (yb2 - self.rect.centery)**2):
            self.proximo_obstaculo_ind = 0
        else:
            self.proximo_obstaculo_ind = 1

    def update(self, obstaculo):
        self.dino_dead(obstaculo)

        if self.update_flag:
            xd, yd = self.rect.centerx, self.rect.centery
            xb1, yb1 = obstaculo.rect.centerx, obstaculo.rect.centery

            estado = np.array([
                self.rect.centery,
                self.jump_force,
                obstaculo.rect.centerx,
                obstaculo.rect.centery,
                obstaculo.sprite_tip,
                obstaculo.speed,
                np.sqrt( (xb1 - xd)**2 + (yb1 - yd)**2)
            ])

            estado_norm = estado / np.linalg.norm(estado)

            somatorio = np.max((self.neuronios @ estado_norm.T) + self.bias)
            sigmoid = 1/(1+np.exp(-somatorio))
            
            if sigmoid <= 0.33:
                self.jump = True
            elif sigmoid < 0.66:
                self.jump = False
                self.down = False
            else:
                self.down = True
                
                

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
