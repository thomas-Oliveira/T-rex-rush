from pygame import *
import pygame
import os
import numpy as np

from load_sprite_sheet import load_sprite_sheet

class Inf(pygame.sprite.Sprite): 
	def __init__(self, startpos, sizex,sizey, qtd_inputs, width, height, qtd_neuronios): 
		pygame.sprite.Sprite.__init__(self) 
		#direcao: 1=direita, -1=esquerda
		
		self.images, self.rect = load_sprite_sheet("rede2.png",1,1,sizex,sizey,-1)
		self.images1, self.rect1 = load_sprite_sheet("perceptron.png",1,1,sizex - int(sizex/7),sizey - int(sizey/7),-1)
		self.rede, self.percptron = self.images[0], self.images1[0]
		
		self.pesos = [0]*qtd_inputs
		self.sigmoid = 0
		self.somatorio = 0
		self.inputs = [0]*qtd_inputs
		self.bias = 0
		self.output = 2
		self.escolhido_neuronio = 0
		self.qtd_neuronios = qtd_neuronios

		self.rect.centerx = startpos[0] + 60
		self.rect.centery = startpos[1]
		self.rect1.centerx = self.rect.left - 350
		self.rect1.centery = startpos[1] - 20
		self.inputs_name = ["altura dino", "força do pulo", "local obstaculo", "altura obstaculo", "tipo obstaculo", "Velocidade Obstaculo", "Distancia do obstaculo"]
		self.saidas_name = ["Pular", "Nada", "Abaixar"]
		
		pygame.font.init()
		font = pygame.font.SysFont('Comic Sans MS', 24)
		font_input_name = pygame.font.SysFont('Comic Sans MS', 14) 
		color = (0,0,0)
		
		self.text_pesos = [font.render("{:>5}".format(f"{i}"), True, color) for i in self.pesos]
		self.text_inputs = [font.render(f"{i}", True, color) for i in self.inputs]
		self.text_inputs_name = [font_input_name.render(f"{i}", True, color) for i in self.inputs_name]
		self.text_saidas_name = [font_input_name.render(f"{i}", True, (255,255,255)) for i in self.saidas_name]
		
		self.text_score = font.render(f"Score: 0", True, color) 
		self.text_Hi = font.render(f"Hi: 0", True, color) 
		self.text_geracao = font.render(f"Geração: 0", True, color) 
		self.text_qtd_dinos_vivos = font.render(f"Qtd dinos vivos: 0", True, color) 
	
		self.reac_text_pesos = [i.get_rect() for i in self.text_pesos]
		self.reac_text_inputs = [i.get_rect() for i in self.text_inputs]
		self.reac_text_inputs_name = [i.get_rect() for i in self.text_inputs_name]
		self.reac_text_saidas_name = [i.get_rect() for i in self.text_inputs_name]
		
		self.reac_text_score = self.text_score.get_rect()
		self.reac_text_Hi = self.text_Hi.get_rect()
		self.reac_text_geracao = self.text_geracao.get_rect()
		self.reac_text_qtd_dinos_vivos = self.text_qtd_dinos_vivos.get_rect()

		consX = 400
		self.reac_text_score.center = (consX, 30) 
		self.reac_text_Hi.center = (consX + 100, 30) 
		self.reac_text_geracao.center = (consX + 200,30) 
		self.reac_text_qtd_dinos_vivos.center = (consX + 400, 30) 

	def draw_rede(self, screen):
		consX_cir = 1070
		consy_cir = 15 + 300%self.qtd_neuronios
		consX_cir_saida = 1250
		consy_cir_saida = 70 + 300%self.qtd_neuronios
		consX = 230
		consy = 70 + 300%self.qtd_neuronios
		color = (0,0,0)

		for i in range(len(self.reac_text_pesos)):
			self.reac_text_pesos[i].center = (consX + 580, consy+(i*25))
			self.reac_text_inputs[i].center = (consX + 325, consy+(i*25)) 
			self.reac_text_inputs_name[i].center = (consX + 465, consy+(i*25))
			for j in range(self.qtd_neuronios):
				color_aux = (0,255,0) if j == self.escolhido_neuronio else color
				pygame.draw.line(screen, color_aux, (consX + 635, consy+(i*25)), (consX_cir, consy_cir+(j*40)))

		for i in range(3):			
			for j in range(self.qtd_neuronios):
				color_aux2 = (0,255,0) if j == self.escolhido_neuronio and i == self.output else color
				pygame.draw.line(screen, color_aux2, (consX_cir_saida, consy_cir_saida+(i*70)), (consX_cir, consy_cir+(j*40)))

			color_aux = (0,255,0) if i == self.output else color
			pygame.draw.circle(screen, color_aux, (consX_cir_saida, consy_cir_saida+(i*70)), 30, 30)
			self.reac_text_saidas_name[i].center = (consX_cir_saida+20, consy_cir_saida+(i*70))
			screen.blit(self.text_saidas_name[i], self.reac_text_saidas_name[i])

		for i in range(self.qtd_neuronios):
			color_aux = (0,255,0) if i == self.escolhido_neuronio else color
			pygame.draw.circle(screen, color_aux, (consX_cir, consy_cir+(i*40)), 15, 30)
	

	def update(self,  dino, obstaculo, best_score, ger, qtd_dino_em_jogo):
		obstaculo = obstaculo[dino.proximo_obstaculo_ind]
		xd, yd = dino.rect.centerx, dino.rect.centery
		xb1, yb1 = obstaculo.rect.centerx, obstaculo.rect.centery

		self.inputs = np.array([
				dino.rect.centery,
				dino.jump_force,
				obstaculo.rect.centerx,
				obstaculo.rect.centery,
				obstaculo.sprite_tip,
				obstaculo.speed,
				np.sqrt( (xb1 - xd)**2 + (yb1 - yd)**2)
			])

		self.inputs = self.inputs / np.linalg.norm(self.inputs)

		self.pesos = dino.neuronios
		self.bias = dino.bias

		self.somatorio = (self.pesos @ self.inputs.T) + self.bias
		self.escolhido_neuronio = np.argmax(self.somatorio)
		
		self.sigmoid = 1/(1+np.exp(-np.max(self.somatorio)))
		 
		self.output = 0 if self.sigmoid <= 0.33 else 1 if self.sigmoid < 0.66 else 2

		font = pygame.font.SysFont('Comic Sans MS', 19)
		font_input_name = pygame.font.SysFont('Comic Sans MS', 12) 
		color = (0,0,0)
		self.text_pesos = [font.render("{:>5}".format(f"{round(i, 4)}"), True, color) for i in self.pesos[self.escolhido_neuronio]]
	
		self.text_inputs = [font.render("{:>5}".format(f"{round(i,3)}"), True, color) for i in self.inputs]
		
		self.text_output = font.render(f"{self.output}", True, color) 
		self.text_score = font.render(f"Score: {dino.score}", True, color) 
		self.text_Hi = font.render(f"Hi: {best_score}", True, color) 
		self.text_geracao = font.render(f"Geração: {ger}", True, color) 
		self.text_qtd_dinos_vivos = font.render(f"Qtd dinos vivos: {qtd_dino_em_jogo}", True, color)

	def draw(self, screen):
		self.draw_rede(screen)
	
		screen.blit(self.percptron, self.rect1)
		for elem1, elem2 in list(zip(self.text_pesos, self.reac_text_pesos)):
			screen.blit(elem1, elem2)
		for elem1, elem2 in list(zip(self.text_inputs, self.reac_text_inputs)):
			screen.blit(elem1, elem2)
		for elem1, elem2 in list(zip(self.text_inputs_name, self.reac_text_inputs_name)):
			screen.blit(elem1, elem2)
		for elem1, elem2 in list(zip(self.text_saidas_name, self.reac_text_saidas_name)):
			screen.blit(elem1, elem2)
		
		screen.blit(self.text_score, self.reac_text_score)
		screen.blit(self.text_Hi, self.reac_text_Hi)
		screen.blit(self.text_geracao, self.reac_text_geracao)
		screen.blit(self.text_qtd_dinos_vivos, self.reac_text_qtd_dinos_vivos)