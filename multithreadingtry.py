
from time import sleep
import sys, pygame
import numpy as np
import threading
import pygame
from pygame import mouse
from pygame.locals import *


global running
running=1

class CountThread(threading.Thread):   
	def run(self):
		while running:
			self.data=np.random.rand(2,1)
			print running
			sleep(0.1)


pygame.init()

clock = pygame.time.Clock()

size = width, height = 320, 240
speed = [2, 2]
black = 0, 0, 0
red = (255,0,0,120)

screen = pygame.display.set_mode(size)

a = CountThread()
b = CountThread()
a.start()
b.start()
X=100
Y=100
X1=200
Y1=200


while running:

	print running

	screen.fill(black)
	x1,y1=b.data
	x,y=a.data
	#x1,y1=b.data
	X+=10*x-5
	Y+=10*y-5
	X1+=10*x1-5
	Y1+=10*y1-5
	pygame.draw.circle(screen, red, (X,Y),10)
	pygame.draw.circle(screen, red, (X1,Y1),10)
	msElapsed = clock.tick(30)
	pygame.display.update()
	for event in pygame.event.get():                        
		if event.type==QUIT:
			pygame.quit()
			break
		if event.type==KEYDOWN:
			if event.key==pygame.K_q: #quits entirely
				pygame.quit()
				running=0
				break


pygame.quit()
