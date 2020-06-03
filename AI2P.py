from collections import deque
from Quoridor2P import *
from player import *
from position import *


def heuristic(logic: Main, player1: Player, player2: Player, goal: int):
    # TODO add more factors
    return 2 * shortestPath(logic, player1, player2, goal) + (player1.walls / player2.walls)


def shortestPath(logic: Main, player1: Player, player2: Player, goal: int):
    mark = [[False for i in range(9)] for j in range(9)]
    p1 = Player(Position(player1.pos.row, player1.pos.col))
    q = deque()
    q.append((p1, 0))
    mark[p1.pos.row][p1.pos.col] = True

    while q:
        p, d = q.popleft()
        if p.pos.row == goal:
            return d
        for pm in logic.possibleMoves(p, player2):
            if not mark[pm.row][pm.col]:
                mark[pm.row][pm.col] = True
                p3 = Player(Position(p.pos.row, p.pos.col))
                p3.pos.row = pm.row
                p3.pos.col = pm.col
                q.append((p3, d + 1))
    return -1

# logic = Main()
# p1 = Player(Position(0, 4))
# p2 = Player(Position(8, 4))
# logic.addHwall(2, 3, 1, 1, p2, p1, 8)
# logic.addHwall(6, 7, 1, 1, p2, p1, 8)
# logic.addHwall(4, 5, 0, 0, p2, p1, 8)
# print(shortestPath(logic, p1, p2, 8))
