import pygame
import os

from dino import dino
from IAdino import dino_IA
from ground import ground
from obstaculo import Obstaculo

background_colour = (255,255,255)
size = width, height = (600, 400)
FPS = 30
CHAO = 350
GAME_OVER = False

screen = pygame.display.set_mode(size)
pygame.display.set_caption('T-rex rush')
screen.fill(background_colour)
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 32)
text = font.render('Score:', True, (0, 255, 0))
textRect = text.get_rect()		
textRect.center = (width - width/3, 25) 

pygame.display.flip()

dino = dino([100,CHAO], 44,47)
ground = ground([0,CHAO], width*2,40)
obstaculo = Obstaculo([width,CHAO], 44,40)
obstaculo2 = Obstaculo([width+width/2,CHAO], 44,40)

dino_ia = dino_IA([100,CHAO], 44, 47)   
print(dino_ia.neuronios)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.KEYDOWN: 
			if event.key == pygame.K_DOWN:
				dino.down = True
			if event.key == pygame.K_UP:
				dino.jump = True
			
		else:
			dino.down = False	

	dino.update()
	ground.update()
	obstaculo.update()
	obstaculo2.update()

	if dino.is_collided_with(obstaculo) or dino.is_collided_with(obstaculo2):
		dino.dino_dead()
		GAME_OVER = True

	dino.update_score(obstaculo)
	dino.update_score(obstaculo2)

	if GAME_OVER:
		text = font.render(f'Game Over Score: {dino.score}', True, (0, 255, 0))
		textRect.center = (width - width/2, 40) 
	else:
		text = font.render(f'Score: {dino.score}', True, (0, 255, 0))

	screen.fill(background_colour)
	screen.blit(ground.images, ground.rect)
	screen.blit(ground.images1, ground.rect1)
	screen.blit(dino.image, dino.rect)
	screen.blit(obstaculo.image, obstaculo.rect)
	screen.blit(obstaculo2.image, obstaculo2.rect)
	screen.blit(text, textRect)
	pygame.display.flip()
	clock.tick(FPS)