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
		pygame.init()
		pygame.display.set_caption('Quoridor')
		pygame.font.init()
		self.myfont = pygame.font.SysFont('Comic Sans MS', 50)
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((950, 950))
		bg = pygame.image.load("bg.jpg").convert()
		bg = pygame.transform.scale(bg, (950, 950))
		self.screen.blit(bg, (0, 0))
		#player1
		round_rect(self.screen, colors["red"], (360, 45, 155, 45))
		round_rect(self.screen, colors["brawn"], (520, 45, 50, 45))
		textsurface = self.myfont.render('Player1', False, colors["black"])
		self.screen.blit(textsurface,(375,50))
		textsurface = self.myfont.render('10', False, colors["white"])
		self.screen.blit(textsurface,(525,50))
		#player2
		round_rect(self.screen, colors["green"], (360, 870, 155, 45))
		round_rect(self.screen, colors["brawn"], (520, 870, 50, 45))
		textsurface = self.myfont.render('Player2', False, colors["black"])
		self.screen.blit(textsurface,(375,875))
		textsurface = self.myfont.render('10', False, colors["white"])
		self.screen.blit(textsurface,(525,875))

		pygame.draw.rect(self.screen, colors["gray"], (125, 125, 700, 700))

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
		x = 195
		y = 195
		for i in range(8):
			pygame.draw.rect(self.screen, colors["white"], (x, 125, 8.75, 700), 1)
			pygame.draw.rect(self.screen, colors["white"], (125, y, 700, 8.75), 1)
			x += 78.75
			y += 78.75
		pygame.display.update()

	def circle_position(self, x, y):
		px = (int)(125 + (x) * (78.75) + 35)
		py = (int)(125 + (y) * (78.75) + 35)
		return tuple([py, px])

	def rect_position(self, x, y):
		px = 125 + x * 78.75
		py = 125 + y * 78.75
		return py, px, 70, 70

	def vwall_position(self, x, y):
		px = 195 + x * 78.75
		py = 125 + y * 78.75
		return px, py, 8.75, 148.75

	def hwall_position(self, x, y):
		px = 125 + x * 78.75
		py = 195 + y * 78.75
		return px, py, 148.75, 8.75

	def handleClick(self):
		if self.players[0].obj.collidepoint(pygame.mouse.get_pos()):
			if self.turn == 0:
				self.possibleMove = Main.possibleMoves(self.players[0], self.players[1])
				self.drawPossibleMoves()
		elif self.players[1].obj.collidepoint(pygame.mouse.get_pos()):
			if self.turn == 1:
				self.possibleMove = Main.possibleMoves(self.players[1], self.players[0])
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
					if Main.addVwall(vx, vx+1, vy, vy+1, self.players[self.turn], self.players[0 if self.turn == 1 else 1], 8 if self.turn == 0 else 0):
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
						if Main.addHwall(hx, hx+1, hy, hy+1, self.players[self.turn], self.players[0 if self.turn == 1 else 1], 8 if self.turn == 0 else 0):
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
			round_rect(self.screen, colors["brawn"], (520, 45, 50, 45))
			textsurface = self.myfont.render(str(player.walls), False, colors["white"])
			self.screen.blit(textsurface,(525,50))
		else:
			round_rect(self.screen, colors["brawn"], (520, 870, 50, 45))
			textsurface = self.myfont.render(str(player.walls), False, colors["white"])
			self.screen.blit(textsurface,(525,875))


	def checkVwalls(self):
		mx, my = pygame.mouse.get_pos()
		for i in range(8):
			x = 195 + i * 78.75
			if x <= mx <= x+8.75:
				for j in range(9):
					y = 125 + j * 78.75
					if y <= my <= y + 70:
						return i, j
		return -1, -1

	def checkHwalls(self):
		mx, my = pygame.mouse.get_pos()
		for i in range(9):
			x = 125 + i * 78.75
			if x <= mx <= x + 70:
				for j in range(8):
					y = 195 + j * 78.75
					if y <= my <= y + 8.75:
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
			if pygame.mouse.get_pressed()[0]:
				self.handleClick()
			pygame.display.update()
			pygame.event.pump()
			self.clock.tick(60)


board = Board(2)
board.play()