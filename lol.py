
from time import sleep
import sys, pygame
import numpy as np
import threading


class CountThread(threading.Thread):   
	def run(self):
		while 1:
			self.data=np.random.rand(2,1)
			sleep(0.1)


def function(x,y,X,Y):
	X=X+10*x-5
	Y=Y+10*y-5
	return X,Y


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


while 1:
	screen.fill(black)
	x,y=a.data
	x1,y1=b.data
	X,Y=function(x,y,X,Y)
	X1,Y1,=function(x,y,X1,Y1)
	pygame.draw.circle(screen, red, (X,Y),10)
	pygame.draw.circle(screen, red, (X1,Y1),10)
	msElapsed = clock.tick(30)
	pygame.display.update()


