import pygame
from Quoridor2P import *
from roundRect import *
from position import *
from player import *


colors = {"black": (0, 0, 0), "white": (234, 236, 238), "brawn": (102, 51, 0), "light-brawn": (255, 138, 101), "gray": (44, 62, 80), "light-gray": (128, 139, 150),  "red": (255, 0, 0), "blue": (0, 0, 255), "green": (0, 255, 0), "yellow": (255, 255, 0), "aqua": (0, 255, 255)}

class Board:
	def __init__(self, numOfPlayer):
		self.numOfPlayer = numOfPlayer
		self.turn = 0
		self.possibleMove = []
		if numOfPlayer == 2:
			self.logic = Main()
		pygame.init()
		pygame.display.set_caption('Quoridor')
		pygame.font.init()
		self.myfont = pygame.font.SysFont('Comic Sans MS', 35)
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((850, 790))
		bg = pygame.image.load("bg.jpg").convert()
		bg = pygame.transform.scale(bg, (850, 790))
		self.screen.blit(bg, (0, 0))
		#player1
		round_rect(self.screen, colors["red"], (360, 15, 155, 45))
		round_rect(self.screen, colors["brawn"], (520, 15, 50, 45))
		textsurface = self.myfont.render('Player1', False, colors["black"])
		self.screen.blit(textsurface,(375,10))
		textsurface = self.myfont.render('10', False, colors["white"])
		self.screen.blit(textsurface,(525,10))
		#player2
		round_rect(self.screen, colors["green"], (360, 730, 155, 45))
		round_rect(self.screen, colors["brawn"], (520, 730, 50, 45))
		textsurface = self.myfont.render('Player2', False, colors["black"])
		self.screen.blit(textsurface,(375,725))
		textsurface = self.myfont.render('10', False, colors["white"])
		self.screen.blit(textsurface,(525,725))

		pygame.draw.rect(self.screen, colors["gray"], (100, 70, 650, 650))

		if numOfPlayer == 2:
			p1 = pygame.draw.circle(self.screen, colors["red"], self.circle_position(0, 4), 25)
			p2 = pygame.draw.circle(self.screen, colors["green"], self.circle_position(8, 4), 25)
			player1 = Player(Position(0, 4), p1, colors["red"])
			player2 = Player(Position(8, 4), p2, colors["green"])
			self.players = [player1, player2]
		if numOfPlayer == 4:
			p1 = pygame.draw.circle(self.screen, colors["red"], self.circle_position(0, 4), 25)
			p2 = pygame.draw.circle(self.screen, colors["green"], self.circle_position(8, 4), 25)
			p3 = pygame.draw.circle(self.screen, colors["yellow"], self.circle_position(4, 8), 25)
			p4 = pygame.draw.circle(self.screen, colors["aqua"], self.circle_position(4, 0), 25)
			player1 = Player(Position(0, 4), colors["red"], p1, 5)
			player2 = Player(Position(8, 4), colors["green"], p2, 5)
			player3 = Player(Position(4, 8), colors["yellow"], p3, 5)
			player4 = Player(Position(4, 0), colors["aqua"], p4, 5)
			self.players = [player1, player2, player3, player4]
		x = 165
		y = 135
		for i in range(8):
			pygame.draw.rect(self.screen, colors["white"], (x, 70, 8, 650), 1)
			pygame.draw.rect(self.screen, colors["white"], (100, y, 650, 8), 1)
			x += 73
			y += 73
		pygame.display.update()

	def circle_position(self, x, y):
		px = (int)(70 + (x) * (73) + 32)
		py = (int)(100 + (y) * (73) + 32)
		return tuple([py, px])

	def rect_position(self, x, y):
		px = 70 + x * 73
		py = 100 + y * 73
		return py, px, 65, 65

	def vwall_position(self, x, y):
		px = 165 + x * 73
		py = 70 + y * 73
		return px, py, 8, 138

	def hwall_position(self, x, y):
		px = 100 + x * 73
		py = 135 + y * 73
		return px, py, 138, 8

	def handleClick(self):
		if self.players[0].obj.collidepoint(pygame.mouse.get_pos()):
			if self.turn == 0:
				self.possibleMove = self.logic.possibleMoves(self.players[0], self.players[1])
				self.drawPossibleMoves()
		elif self.players[1].obj.collidepoint(pygame.mouse.get_pos()):
			if self.turn == 1:
				self.possibleMove = self.logic.possibleMoves(self.players[1], self.players[0])
				self.drawPossibleMoves()
		else:
			for pm in self.possibleMove:
				if pm.obj.collidepoint(pygame.mouse.get_pos()):
					pygame.draw.rect(self.screen, colors["gray"], self.rect_position(self.players[self.turn].pos.row, self.players[self.turn].pos.col))
					self.deletePossibleMoves()
					self.players[self.turn].obj = pygame.draw.circle(self.screen, self.players[self.turn].color, self.circle_position(pm.row, pm.col), 25)
					self.players[self.turn].pos.row = pm.row
					self.players[self.turn].pos.col = pm.col
					if self.turn == 0:
						self.turn = 1
					else:
						self.turn = 0
					break;
			else:
				vx, vy = self.checkVwalls()
				if vx != -1 and self.players[self.turn].walls > 0:
					if vy == 8:
						vy -= 1
					if self.logic.addVwall(vx, vx+1, vy, vy+1, self.players[self.turn], self.players[0 if self.turn == 1 else 1], 8 if self.turn == 0 else 0):
						pygame.draw.rect(self.screen, colors["light-brawn"], self.vwall_position(vx, vy))
						self.decreaseWalls(self.players[self.turn])
						if self.turn == 0:
							self.turn = 1
						else:
							self.turn = 0
				else:
					hx, hy = self.checkHwalls()
					if hx != -1 and self.players[self.turn].walls > 0:
						if hx == 8:
							hx -= 1
						if self.logic.addHwall(hx, hx+1, hy, hy+1, self.players[self.turn], self.players[0 if self.turn == 1 else 1], 8 if self.turn == 0 else 0):
							pygame.draw.rect(self.screen, colors["light-brawn"], self.hwall_position(hx, hy))
							self.decreaseWalls(self.players[self.turn])
							if self.turn == 0:
								self.turn = 1
							else:
								self.turn = 0
				self.deletePossibleMoves()

	def decreaseWalls(self, player):
		player.walls -= 1
		if player == self.players[0]:
			round_rect(self.screen, colors["brawn"], (520, 15, 50, 45))
			textsurface = self.myfont.render(str(player.walls), False, colors["white"])
			self.screen.blit(textsurface,(535,10))
		else:
			round_rect(self.screen, colors["brawn"], (520, 730, 50, 45))
			textsurface = self.myfont.render(str(player.walls), False, colors["white"])
			self.screen.blit(textsurface,(535,725))


	def checkVwalls(self):
		mx, my = pygame.mouse.get_pos()
		for i in range(8):
			x = 165 + i * 73
			if x <= mx <= x+8:
				for j in range(9):
					y = 70 + j * 73
					if y <= my <= y + 65:
						return i, j
		return -1, -1

	def checkHwalls(self):
		mx, my = pygame.mouse.get_pos()
		for i in range(9):
			x = 100 + i * 73
			if x <= mx <= x + 65:
				for j in range(8):
					y = 135 + j * 73
					if y <= my <= y + 8:
						return i, j
		return -1, -1

	def drawPossibleMoves(self):
		for p in self.possibleMove:
			p.obj = pygame.draw.rect(self.screen, colors["light-gray"], (self.rect_position(p.row, p.col)))

	def deletePossibleMoves(self):
		for p in self.possibleMove:
			p.obj = pygame.draw.rect(self.screen, colors["gray"], (self.rect_position(p.row, p.col)))
		self.possibleMove = []


	def play(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
			if pygame.mouse.get_pressed()[0]:
				self.handleClick()
			pygame.display.update()
			pygame.event.pump()
			self.clock.tick(60)


board = Board(2)
board.play()