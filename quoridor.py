from pygame import *
import pygame

def circle_position(x, y):
	px = (int)(125 + (x-1) * (78.75) + 35)
	py = (int)(125 + (y-1) * (78.75) + 35)
	return tuple([py, px])

def rect_position(x, y):
	px = 125 + (x-1) * (78.75)
	py = 125 + (y-1) * (78.75)
	return py, px, 70, 70

colors = {"white": (234, 236, 238), "brawn": (186, 74, 0), "gray": (44, 62, 80), "light-gray": (128, 139, 150),  "red": (255, 0, 0), "blue": (0, 0, 255), "green": (0, 255, 0), "yellow": (255, 255, 0), "aqua": (0, 255, 255)}

pygame.init()
screen = pygame.display.set_mode((950, 950))
bg = pygame.image.load("bg.jpg").convert()
bg = pygame.transform.scale(bg, (950, 950))
screen.blit(bg, (0, 0))
pygame.draw.rect(screen, colors["gray"], (125, 125, 700, 700))
x = 195
y = 195
pygame.draw.circle(screen, colors["red"], circle_position(1, 5), 25)
pygame.draw.circle(screen, colors["green"], circle_position(9, 5), 25)
pygame.draw.circle(screen, colors["yellow"], circle_position(5, 9), 25)
pygame.draw.circle(screen, colors["aqua"], circle_position(5, 1), 25)
for i in range(8):
	pygame.draw.rect(screen, colors["white"], (x, 125, 8.75, 700), 1)
	pygame.draw.rect(screen, colors["white"], (125, y, 700, 8.75), 1)
	x += 78.75
	y += 78.75
pygame.draw.rect(screen, (255, 138, 101 ), (195, 195, 8.75, 86.5))
pygame.draw.rect(screen, (255, 138, 101 ), (195, 125, 8.75, 86.5))
pygame.draw.rect(screen, colors["light-gray"], (rect_position(1, 4)))
pygame.draw.rect(screen, colors["light-gray"], (rect_position(1, 6)))
pygame.draw.rect(screen, colors["light-gray"], (rect_position(2, 5)))
pygame.display.update()

while True:
    pygame.event.pump()
