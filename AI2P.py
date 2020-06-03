from collections import deque
from Quoridor2P import *
from player import *
from position import *


class AI2P:
    def __init__(self, logic: Main, goal: int):
        self.logic = logic
        self.goal = goal

    def chooseAnAction(self, player1: Player, player2: Player):
        p1 = Player(Position(player1.pos.row, player1.pos.col))
        p2 = Player(Position(player2.pos.row, player2.pos.col))
        alphaBeta = -1
        r = 0
        c = 0
        action = ""
        for pm in self.logic.possibleMoves(p1, p2):
            p = Player(Position(pm.row, pm.col))
            a = self.minimaxTree(p, p2, 1, 0, 1)
            print(a, "move", pm.row, pm.col)
            # self.printWalls()
            if a > alphaBeta:
                alphaBeta = a
                r = pm.row
                c = pm.col
                action = "move"
        lr = 0
        rr = p2.pos.row
        if self.goal == 0:
            lr = p2.pos.row
            rr = 8
        for row in range(8):
            for col in range(8):
                if self.logic.addHwall(col, row, p1, p2, self.goal):
                    a = self.minimaxTree(p1, p2, 1, 0, 1)
                    print(a, "add Hwall", row, col)
                    # self.printWalls()
                    if a > alphaBeta:
                        alphaBeta = a
                        r = row
                        c = col
                        action = "add Hwall"
                    self.logic.hwalls[row][col] = False
                if self.logic.addVwall(col, row, p1, p2, self.goal):
                    a = self.minimaxTree(p1, p2, 1, 0, 1)
                    print(a, "add Vwall", row, col)
                    # self.printWalls()
                    if a > alphaBeta:
                        alphaBeta = a
                        r = row
                        c = col
                        action = "add Vwall"
                    self.logic.vwalls[row][col] = False
        return action, r, c

    def minimaxTree(self, player1: Player, player2: Player, d, l, r):
        # TODO find the best depth for algorithm
        if d == 4:
            return self.heuristic(player1, player2)
        if player1.pos.row == self.goal:
            return 1
        g = 0 if self.goal == 8 else 8
        if player2.pos.row == g:
            return 0
        if d % 2 == 1:
            # min
            alphaBeta = 1
            for pm in self.logic.possibleMoves(player2, player1):
                p = Player(Position(pm.row, pm.col))
                a = self.minimaxTree(player1, p, d + 1, l, r)
                alphaBeta = min(alphaBeta, a)
                if a <= l:
                    return alphaBeta
                r = min(r, a)
            lr = 0
            rr = player2.pos.row
            if self.goal == 8:
                lr = player2.pos.row
                rr = 8
            for row in range(lr, rr):
                for col in range(8):
                    if self.logic.addHwall(col, row, player1, player2, self.goal):
                        a = self.minimaxTree(player1, player2, d + 1, l, r)
                        alphaBeta = min(alphaBeta, a)
                        if a <= l:
                            self.logic.vwalls[row][col] = False
                            return alphaBeta
                        r = min(r, a)
                        self.logic.hwalls[row][col] = False
                    if self.logic.addVwall(col, row, player1, player2, self.goal):
                        a = self.minimaxTree(player1, player2, d + 1, l, r)
                        alphaBeta = min(alphaBeta, a)
                        if a <= l:
                            self.logic.vwalls[row][col] = False
                            return alphaBeta
                        r = min(r, a)
                        self.logic.vwalls[row][col] = False

            return alphaBeta
        else:
            # max
            alphaBeta = 0
            for pm in self.logic.possibleMoves(player1, player2):
                p = Player(Position(pm.row, pm.col))
                a = self.minimaxTree(p, player2, d + 1, l, r)
                alphaBeta = max(alphaBeta, a)
                if a >= r:
                    return alphaBeta
                l = max(l, a)
            lr = 0
            rr = player2.pos.row
            if self.goal == 0:
                lr = player2.pos.row
                rr = 8
            for row in range(lr, rr):
                for col in range(8):
                    if self.logic.addHwall(col, row, player1, player2, self.goal):
                        a = self.minimaxTree(player1, player2, d + 1, l, r)
                        alphaBeta = max(alphaBeta, a)
                        if a >= r:
                            self.logic.hwalls[row][col] = False
                            return alphaBeta
                        l = max(l, a)
                        self.logic.hwalls[row][col] = False
                    if self.logic.addVwall(col, row, player1, player2, self.goal):
                        a = self.minimaxTree(player1, player2, d + 1, l, r)
                        alphaBeta = max(alphaBeta, a)
                        if a >= r:
                            self.logic.vwalls[row][col] = False
                            return alphaBeta
                        l = max(l, a)
                        self.logic.vwalls[row][col] = False
            return alphaBeta

    def heuristic(self, player1: Player, player2: Player):
        # TODO add more factors
        if player1.pos.row == self.goal:
            return 1
        g = 0 if self.goal == 8 else 8
        if player2.pos.row == g:
            return 0
        return (0.6 * self.shortestPath(player2, player1, 0 if self.goal == 8 else 8)
                / self.shortestPath(player1, player2, self.goal)) / 70 \
               + 0.2 * player1.walls / player2.walls / 10 \
               + 0.2 * self.countNearWalls(player1, player2) / 20

    def countNearWalls(self, player1: Player, player2: Player):
        w = 0
        for pm in self.logic.possibleMoves(player1, player2):
            if self.logic.isHwall(pm.row, pm.col):
                w += 1
            if self.logic.isHwall(pm.row - 1, pm.col):
                w += 1
            if self.logic.isVwall(pm.row, pm.col):
                w += 1
            if self.logic.isVwall(pm.row, pm.col - 1):
                w += 1
        return w

    def shortestPath(self, player1: Player, player2: Player, goal):
        mark = [[False for i in range(9)] for j in range(9)]
        p1 = Player(Position(player1.pos.row, player1.pos.col))
        q = deque()
        q.append((p1, 0))
        mark[p1.pos.row][p1.pos.col] = True

        while q:
            p, d = q.popleft()
            if p.pos.row == goal:
                return d
            for pm in self.logic.possibleMoves(p, player2):
                if not mark[pm.row][pm.col]:
                    mark[pm.row][pm.col] = True
                    p3 = Player(Position(p.pos.row, p.pos.col))
                    p3.pos.row = pm.row
                    p3.pos.col = pm.col
                    q.append((p3, d + 1))
        return -1

    def printWalls(self):
        print("--hwalls")
        for i in range(8):
            for j in range(9):
                print(self.logic.hwalls[i][j], end=" ")
            print()
        print("--vwalls")
        for i in range(9):
            for j in range(8):
                print(self.logic.vwalls[i][j], end=" ")
            print()
# logic = Main()
# ai = AI2P(logic, 8)
# p2 = Player(Position(5, 4))
# p1 = Player(Position(6, 4))
# # logic.addHwall(4, 5, p1, p2, 8)
# # logic.addHwall(2, 5, p1, p2, 8)
# print(ai.minimaxTree(p1, p2, 1, 0, 1))
# # p1 = Player(Position(5, 5))
# # print(ai.minimaxTree(p1, p2, 1, 0, 1))
# p1 = Player(Position(3, 4))
# print(ai.minimaxTree(p1, p2, 1, 0, 1))
# p1 = Player(Position(4, 3))
# print(ai.minimaxTree(p1, p2, 1, 0, 1))
# p1 = Player(Position(4, 5))
# print(ai.minimaxTree(p1, p2, 1, 0, 1))
# # logic.addHwall(2, 3, 1, 1, p2, p1, 8)
# # logic.addHwall(6, 7, 1, 1, p2, p1, 8)
# # logic.addHwall(4, 5, 0, 0, p2, p1, 8)
# # print(shortestPath(logic, p1, p2, 8))
