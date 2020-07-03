import pygame
import os

from dino import dino
from IAdino import dino_IA
from ground import ground
from obstaculo import Obstaculo
from informacao import Inf
from tqdm import tqdm
import numpy as np
import random

CHANCE_MUT =  .2
CHANCE_CO = .25
NUM_INDIVIDUOS = 100
NUM_MELHORES = 5
FEATURES = 7
LABELS = 8
LEARNING_RATE = 0.1

def populacao_aleatoria(n):
    populacao = []
    for i in range(n):
        populacao.append(np.random.uniform(-15, 15, (LABELS, FEATURES)))
    return populacao

def valor_das_acoes(individuo, estado):
    return individuo @ estado # Multiplicação de matrizes

def melhor_jogada(individuo, estado):
    valores = valor_das_acoes(individuo, estado)
    return np.argmax(valores)

def mutacao(individuo):
    for i in range(LABELS):
        for j in range(FEATURES):
            if np.random.uniform(0, 1) < CHANCE_MUT:
                individuo[i][j] *= np.random.uniform(-1 + LEARNING_RATE, 1 + LEARNING_RATE)

def crossover(individuo1, individuo2):
    filho = individuo1.copy()
    for i in range(LABELS):
        for j in range(FEATURES):
            if np.random.uniform(0, 1) < CHANCE_CO:
                filho[i][j] = individuo2[i][j]
    return filho


def calcular_fitness(individuo):
    return individuo.score

def ordenar_lista(lista, ordenacao, decrescente=True):
    return [x for _, x in sorted(zip(ordenacao, lista), key=lambda p: p[0], reverse=decrescente)]

def proxima_geracao(populacao, fitness):
    ordenados = ordenar_lista(populacao, fitness)
    proxima_ger = ordenados[:NUM_MELHORES]
    best_ind = proxima_ger[0]

    while len(proxima_ger) < NUM_INDIVIDUOS:
        ind1, ind2 = random.choices(populacao, k=2)
        filho = crossover(best_ind, ind2)
        mutacao(filho)
        proxima_ger.append(filho)

    return proxima_ger


background_colour = (255,255,255)
size = width, height = (1300, 400)
FPS = 60 + NUM_INDIVIDUOS
CHAO = 350
GAME_OVER = False
qtd_dino_mortos = 0

screen = pygame.display.set_mode(size)
pygame.display.set_caption('T-rex rush')
screen.fill(background_colour)
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 24)
text = font.render('Trex Rush', True, (0, 255, 0))
textRect = text.get_rect()		
textRect.center = (width/5, 25) 

pygame.display.flip()

populacao = populacao_aleatoria(NUM_INDIVIDUOS)

all_sprites = []
ground = ground([0,CHAO], width*2,40)
info = Inf([width - width/3,CHAO-180], 619, 256, FEATURES, width, height, LABELS)
all_sprites.append(ground)

dinos = []
for i in range(NUM_INDIVIDUOS):
	dino = dino_IA(i, [50+random.randint(0,350),CHAO], 44,47, populacao[i]) 
	dinos.append(dino)
	all_sprites.append(dino)

obstaculo = Obstaculo([width,CHAO], 44,40)
obstaculo2 = Obstaculo([width+width/2,CHAO], 44,40)

obstaculos = []
obstaculos.append(obstaculo)
obstaculos.append(obstaculo2)

all_sprites.append(obstaculo)
all_sprites.append(obstaculo2)

best_score = 0
best_dino_score = 0
running = True
ger = 0

reset = np.vectorize(lambda obj: obj.reset())
update = np.vectorize(lambda obj: obj.update())
set_neuronios = np.vectorize(lambda dino: dino.set_neuronios(populacao))
dino_calcular_fitness = np.vectorize(lambda obj: calcular_fitness(obj))
draw_obj = np.vectorize(lambda obj: obj.draw(screen))
update_dino = np.vectorize(lambda obj: obj.update(obstaculos[obj.proximo_obstaculo_ind]))
update_score = np.vectorize(lambda obj: obj.update_score(obstaculos[obj.proximo_obstaculo_ind]))
dino_is_collided_with = np.vectorize(lambda obj: obj.is_collided_with(obstaculo) or obj.is_collided_with(obstaculo2))
best_dino = np.vectorize(lambda obj: obj.score)
qtd_dino_em_jogo = np.vectorize(lambda obj: obj.update_flag)
proximo_obstaculo_ind = np.vectorize(lambda obj: obj.obj_proximo(obstaculo, obstaculo2))
obstaculo_set_speed = np.vectorize(lambda obj: obj.obstaculo_set_speed(ground.speed))

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	if GAME_OVER:
		ger += 1

		best_score = np.max(best_dino(dinos))
		if best_score > best_dino_score:
			best_dino_score = best_score

		fitness = dino_calcular_fitness(dinos)

		populacao = proxima_geracao(populacao, fitness)

		reset(dinos)
		set_neuronios(dinos)
		
		obstaculo_set_speed(obstaculos)
		
		reset(obstaculos)
		ground.speed = -5
		GAME_OVER = False
		qtd_dino_mortos = 0

	ground.update()
	obstaculo.update()
	obstaculo2.update()

	point = (100, 100)
	
	proximo_obstaculo_ind(dinos)
	
	update_dino(dinos)
	
	best_dino_ger_ind = np.argmax(best_dino(dinos))
	
	info.update( dinos[best_dino_ger_ind], obstaculos, best_dino_score, ger, sum(qtd_dino_em_jogo(dinos)))

	if sum(qtd_dino_em_jogo(dinos)) <= 0:
		GAME_OVER = True
		continue

	update_score(dinos)
	obstaculo_set_speed(obstaculos)
	screen.fill(background_colour)
	
	draw_obj(all_sprites)
	screen.blit(text, textRect)
	info.draw(screen)
	pygame.display.flip()
	
	clock.tick(FPS)