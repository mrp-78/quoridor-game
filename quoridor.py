import pygame
import random
from Quoridor2P import *
from Quoridor4P import *
from roundRect import *
from position import *
from player import *
from AI2P import *

colors = {"black": (0, 0, 0), "white": (234, 236, 238), "brawn": (102, 51, 0), "light-brawn": (255, 138, 101),
          "gray": (44, 62, 80), "light-gray": (128, 139, 150), "red": (255, 0, 0), "blue": (0, 0, 255),
          "green": (0, 255, 0), "yellow": (255, 255, 0), "aqua": (0, 255, 255)}


class Board:
    def __init__(self, numOfPlayer):
        self.winner = -1
        self.tryAgein = None
        self.numOfPlayer = numOfPlayer
        self.turn = random.randint(0, numOfPlayer - 1)
        self.possibleMove = []
        if numOfPlayer == 2:
            self.logic = Main()
        else:
            self.logic = Main4()
        pygame.init()
        pygame.display.set_caption('Quoridor')
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((850, 790))
        bg = pygame.image.load("bg.jpg").convert()
        bg = pygame.transform.scale(bg, (850, 790))
        self.screen.blit(bg, (0, 0))

        pygame.draw.rect(self.screen, colors["gray"], (100, 70, 650, 650))

        if numOfPlayer == 2:
            p1 = pygame.draw.circle(self.screen, colors["red"], self.circle_position(0, 4), 25)
            p2 = pygame.draw.circle(self.screen, colors["green"], self.circle_position(8, 4), 25)
            player1 = Player(Position(0, 4), p1, colors["red"])
            player2 = Player(Position(8, 4), p2, colors["green"])
            self.players = [player1, player2]
            # player1
            round_rect(self.screen, colors["red"], (360, 15, 155, 45))
            round_rect(self.screen, colors["brawn"], (520, 15, 50, 45))
            text = self.myfont.render('Player1', False, colors["black"])
            self.screen.blit(text, (375, 10))
            text = self.myfont.render('10', False, colors["white"])
            self.screen.blit(text, (525, 10))
            # player2
            round_rect(self.screen, colors["green"], (360, 730, 155, 45))
            round_rect(self.screen, colors["brawn"], (520, 730, 50, 45))
            text = self.myfont.render('Player2', False, colors["black"])
            self.screen.blit(text, (375, 725))
            text = self.myfont.render('10', False, colors["white"])
            self.screen.blit(text, (525, 725))
        if numOfPlayer == 4:
            p1 = pygame.draw.circle(self.screen, colors["red"], self.circle_position(0, 4), 25)
            p2 = pygame.draw.circle(self.screen, colors["green"], self.circle_position(8, 4), 25)
            p3 = pygame.draw.circle(self.screen, colors["yellow"], self.circle_position(4, 8), 25)
            p4 = pygame.draw.circle(self.screen, colors["aqua"], self.circle_position(4, 0), 25)
            player1 = Player(Position(0, 4), p1, colors["red"], 5)
            player2 = Player(Position(8, 4), p2, colors["green"], 5)
            player3 = Player(Position(4, 8), p3, colors["yellow"], 5)
            player4 = Player(Position(4, 0), p4, colors["aqua"], 5)
            self.players = [player1, player3, player2, player4]
            # player1
            round_rect(self.screen, colors["red"], (360, 15, 155, 45))
            round_rect(self.screen, colors["brawn"], (520, 15, 50, 45))
            text = self.myfont.render('Player1', False, colors["black"])
            self.screen.blit(text, (375, 10))
            text = self.myfont.render('5', False, colors["white"])
            self.screen.blit(text, (525, 10))
            # player2
            round_rect(self.screen, colors["yellow"], (750, 350, 155, 45))
            round_rect(self.screen, colors["brawn"], (780, 400, 50, 45))
            text = self.myfont.render('Player2', False, colors["black"])
            self.screen.blit(text, (750, 345))
            text = self.myfont.render('5', False, colors["white"])
            self.screen.blit(text, (790, 405))
            # player3
            round_rect(self.screen, colors["green"], (360, 730, 155, 45))
            round_rect(self.screen, colors["brawn"], (520, 730, 50, 45))
            text = self.myfont.render('Player3', False, colors["black"])
            self.screen.blit(text, (375, 725))
            text = self.myfont.render('5', False, colors["white"])
            self.screen.blit(text, (525, 725))
            # player4
            round_rect(self.screen, colors["aqua"], (0, 350, 100, 45))
            round_rect(self.screen, colors["brawn"], (15, 400, 50, 45))
            text = self.myfont.render('Player3', False, colors["black"])
            self.screen.blit(text, (0, 345))
            text = self.myfont.render('5', False, colors["white"])
            self.screen.blit(text, (20, 405))
        x = 165
        y = 135
        for i in range(8):
            pygame.draw.rect(self.screen, colors["white"], (x, 70, 8, 650), 1)
            pygame.draw.rect(self.screen, colors["white"], (100, y, 650, 8), 1)
            x += 73
            y += 73
        self.changeTurn()
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
        if self.tryAgein != None and self.tryAgein.collidepoint(pygame.mouse.get_pos()):
            self.__init__(self.numOfPlayer)
        elif self.winner == -1:
            if self.players[0].obj.collidepoint(pygame.mouse.get_pos()):
                if self.turn == 0:
                    if self.numOfPlayer == 2:
                        self.possibleMove = self.logic.possibleMoves(self.players[0], self.players[1])
                    else:
                        self.possibleMove = self.logic.possibleMoves(self.players[0], self.players[1], self.players[2],
                                                                     self.players[3])
                    if len(self.possibleMove) == 0 and self.players[self.turn].walls == 0:
                        changeTurn()
                    self.drawPossibleMoves()
            elif self.players[1].obj.collidepoint(pygame.mouse.get_pos()):
                if self.turn == 1:
                    if self.numOfPlayer == 2:
                        self.possibleMove = self.logic.possibleMoves(self.players[1], self.players[0])
                    else:
                        self.possibleMove = self.logic.possibleMoves(self.players[1], self.players[0], self.players[2],
                                                                     self.players[3])
                    if len(self.possibleMove) == 0 and self.players[self.turn].walls == 0:
                        changeTurn()
                    self.drawPossibleMoves()
            elif self.numOfPlayer == 4 and self.players[2].obj.collidepoint(pygame.mouse.get_pos()):
                if self.turn == 2:
                    self.possibleMove = self.logic.possibleMoves(self.players[2], self.players[1], self.players[0],
                                                                 self.players[3])
                    if len(self.possibleMove) == 0 and self.players[self.turn].walls == 0:
                        changeTurn()
                    self.drawPossibleMoves()
            elif self.numOfPlayer == 4 and self.players[3].obj.collidepoint(pygame.mouse.get_pos()):
                if self.turn == 3:
                    self.possibleMove = self.logic.possibleMoves(self.players[3], self.players[1], self.players[0],
                                                                 self.players[2])
                    if len(self.possibleMove) == 0 and self.players[self.turn].walls == 0:
                        changeTurn()
                    self.drawPossibleMoves()
            else:
                for pm in self.possibleMove:
                    if pm.obj.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(self.screen, colors["gray"],
                                         self.rect_position(self.players[self.turn].pos.row,
                                                            self.players[self.turn].pos.col))
                        self.deletePossibleMoves()
                        self.players[self.turn].obj = pygame.draw.circle(self.screen, self.players[self.turn].color,
                                                                         self.circle_position(pm.row, pm.col), 25)
                        self.players[self.turn].pos.row = pm.row
                        self.players[self.turn].pos.col = pm.col
                        if self.numOfPlayer == 2:
                            if self.turn == 0 and pm.row == 8:
                                self.winner = 0
                                self.printWinner()
                            elif self.turn == 1 and pm.row == 0:
                                self.winner = 1
                                self.printWinner()
                        else:
                            if self.turn == 0 and (pm.row == 8 or pm.col == 0 or pm.col == 8):
                                self.winner = 0
                                self.printWinner()
                            elif self.turn == 2 and (pm.row == 0 or pm.col == 0 or pm.col == 8):
                                self.winner = 2
                                self.printWinner()
                            elif self.turn == 1 and (pm.row == 0 or pm.row == 8 or pm.col == 0):
                                self.winner = 1
                                self.printWinner()
                            elif self.turn == 3 and (pm.row == 0 or pm.row == 8 or pm.col == 8):
                                self.winner = 3
                                self.printWinner()

                        self.changeTurn()
                        break
                else:
                    vx, vy = self.checkVwalls()
                    if vx != -1 and self.players[self.turn].walls > 0:
                        if vy == 8:
                            vy -= 1
                        if self.numOfPlayer == 2:
                            if self.logic.addVwall(vx, vx + 1, vy, vy + 1, self.players[self.turn],
                                                   self.players[0 if self.turn == 1 else 1],
                                                   8 if self.turn == 0 else 0):
                                pygame.draw.rect(self.screen, colors["light-brawn"], self.vwall_position(vx, vy))
                                self.decreaseWalls(self.players[self.turn])
                                self.changeTurn()
                        else:
                            if self.logic.addVwall(vx, vx + 1, vy, vy + 1, self.players):
                                pygame.draw.rect(self.screen, colors["light-brawn"], self.vwall_position(vx, vy))
                                self.decreaseWalls(self.players[self.turn])
                                self.changeTurn()
                    else:
                        hx, hy = self.checkHwalls()
                        if hx != -1 and self.players[self.turn].walls > 0:
                            if hx == 8:
                                hx -= 1
                            if self.numOfPlayer == 2:
                                if self.logic.addHwall(hx, hx + 1, hy, hy + 1, self.players[self.turn],
                                                       self.players[0 if self.turn == 1 else 1],
                                                       8 if self.turn == 0 else 0):
                                    pygame.draw.rect(self.screen, colors["light-brawn"], self.hwall_position(hx, hy))
                                    self.decreaseWalls(self.players[self.turn])
                                    self.changeTurn()
                            else:

                                if self.logic.addHwall(hx, hx + 1, hy, hy + 1, self.players):
                                    pygame.draw.rect(self.screen, colors["light-brawn"], self.hwall_position(hx, hy))
                                    self.decreaseWalls(self.players[self.turn])
                                    self.changeTurn()
                    self.deletePossibleMoves()

    def printWinner(self):
        pygame.draw.rect(self.screen, self.players[self.winner].color, (0, 305, 850, 50))
        textsurface = self.myfont.render('You win the game', False, colors["black"])
        self.screen.blit(textsurface, (315, 300))
        self.tryAgein = pygame.draw.rect(self.screen, colors["black"], (350, 420, 200, 45))
        textsurface = self.myfont.render('Play again', False, colors["white"])
        self.screen.blit(textsurface, (365, 415))

    def changeTurn(self):
        self.turn = (self.turn + 1) % self.numOfPlayer
        round_rect(self.screen, self.players[self.turn].color, (0, 0, 75, 35))
        textsurface = self.myfont.render('turn', False, colors["black"])
        self.screen.blit(textsurface, (5, -10))

    def decreaseWalls(self, player):
        player.walls -= 1
        if self.numOfPlayer == 2:
            if player == self.players[0]:
                round_rect(self.screen, colors["brawn"], (520, 15, 50, 45))
                textsurface = self.myfont.render(str(player.walls), False, colors["white"])
                self.screen.blit(textsurface, (535, 10))
            else:
                round_rect(self.screen, colors["brawn"], (520, 730, 50, 45))
                textsurface = self.myfont.render(str(player.walls), False, colors["white"])
                self.screen.blit(textsurface, (535, 725))
        else:
            if player == self.players[0]:
                round_rect(self.screen, colors["brawn"], (520, 15, 50, 45))
                textsurface = self.myfont.render(str(player.walls), False, colors["white"])
                self.screen.blit(textsurface, (535, 10))
            elif player == self.players[2]:
                round_rect(self.screen, colors["brawn"], (520, 730, 50, 45))
                textsurface = self.myfont.render(str(player.walls), False, colors["white"])
                self.screen.blit(textsurface, (535, 725))
            elif player == self.players[1]:
                round_rect(self.screen, colors["brawn"], (780, 400, 50, 45))
                textsurface = self.myfont.render(str(player.walls), False, colors["white"])
                self.screen.blit(textsurface, (790, 405))
            elif player == self.players[3]:
                round_rect(self.screen, colors["brawn"], (15, 400, 50, 45))
                textsurface = self.myfont.render(str(player.walls), False, colors["white"])
                self.screen.blit(textsurface, (20, 405))

    def checkVwalls(self):
        mx, my = pygame.mouse.get_pos()
        for i in range(8):
            x = 165 + i * 73
            if x <= mx <= x + 8:
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
                # print(shortestPath(self.logic, self.players[0], self.players[1], 8))
                self.handleClick()
            pygame.display.update()
            pygame.event.pump()
            self.clock.tick(60)


board = Board(int(input("Please enter number of players: ")))
board.play()
