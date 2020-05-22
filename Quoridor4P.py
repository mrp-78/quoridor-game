from position import *
from player import *
class Main:

    # horizontal walls
    hwalls = [[False for i in range(9)] for j in range(8)];
    # vertical walls
    vwalls = [[False for i in range(8)] for j in range(9)];

    @staticmethod
    def isHwall(r, c):
        return (Main.hwalls[r][c] or Main.hwalls[r][c - 1]);

    @staticmethod
    def isVwall(r, c):
        return (Main.vwalls[r][c] or Main.vwalls[r - 1][c]);

    @staticmethod
    def possibleMoves(player1, player2, player3, player4):
        pm = [];

        def goUp():
            if player1.pos.row == 0 or Main.isHwall(player1.pos.row - 1, player1.pos.col):
                return;
            if (player2.pos.row == player1.pos.row - 1 and player2.pos.col == player1.pos.col) or (player3.pos.row == player1.pos.row - 1 and player3.pos.col == player1.pos.col) or (player4.pos.row == player1.pos.row - 1 and player4.pos.col == player1.pos.col):
                if player1.pos.row == 1 or Main.isHwall(player1.pos.row - 2, player1.pos.col) or (player3.pos.row == player1.pos.row - 2 and player3.pos.col == player1.pos.col) or (player4.pos.row == player1.pos.row - 2 and player4.pos.col == player1.pos.col) or (player2.pos.row == player1.pos.row - 2 and player2.pos.col == player1.pos.col):
                    if not(player1.pos.col == 0 or Main.isVwall(player1.pos.row - 1, player1.pos.col - 1)):
                        pm.append(Position(player1.pos.row - 1, player1.pos.col - 1));
                    if not(player1.pos.col == 8 or Main.isVwall(player1.pos.row - 1, player1.pos.col)):
                        pm.append(Position(player1.pos.row - 1, player1.pos.col + 1));
                else:
                    pm.append(Position(player1.pos.row - 2, player1.pos.col));
            else:
                pm.append(Position(player1.pos.row - 1, player1.pos.col));
        
        def goDown():
            if player1.pos.row == 8 or Main.isHwall(player1.pos.row, player1.pos.col):
                return;
            if (player2.pos.row == player1.pos.row + 1 and player2.pos.col == player1.pos.col) or (player3.pos.row == player1.pos.row + 1 and player3.pos.col == player1.pos.col) or (player4.pos.row == player1.pos.row + 1 and player4.pos.col == player1.pos.col):
                if player1.pos.row == 7 or Main.isHwall(player1.pos.row + 1, player1.pos.col) or (player3.pos.row == player1.pos.row + 2 and player3.pos.col == player1.pos.col) or (player4.pos.row == player1.pos.row + 2 and player4.pos.col == player1.pos.col) or (player2.pos.row == player1.pos.row + 2 and player2.pos.col == player1.pos.col):
                    if not(player1.pos.col == 0 or Main.isVwall(player1.pos.row + 1, player1.pos.col - 1)):
                        pm.append(Position(player1.pos.row + 1, player1.poscol - 1));
                    if not(player1.pos.col == 8 or Main.isVwall(player1.pos.row + 1, player1.pos.col)):
                        pm.append(Position(player1.pos.row + 1, player1.pos.col + 1));
                else:
                    pm.append(Position(player1.pos.row + 2, player1.pos.col));
            else:
                pm.append(Position(player1.pos.row + 1, player1.pos.col));

        def goLeft():
            if player1.pos.col == 0 or Main.isVwall(player1.pos.row, player1.pos.col - 1):
                return;
            if (player2.pos.row == player1.pos.row and player2.pos.col == player1.pos.col - 1) or (player3.pos.row == player1.pos.row and player3.pos.col == player1.pos.col - 1) or (player4.pos.row == player1.pos.row and player4.pos.col == player1.pos.col - 1):
                if player1.pos.col == 1 or Main.isVwall(player1.pos.row, player1.pos.col - 2) or (player2.pos.row == player1.pos.row and player2.pos.col == player1.pos.col - 2) or (player3.pos.row == player1.pos.row and player3.pos.col == player1.pos.col - 2) or (player4.pos.row == player1.pos.row and player4.pos.col == player1.pos.col - 2):
                    if not(player1.pos.row == 0 or Main.isHwall(player1.pos.row - 1, player1.pos.col - 1)):
                        pm.append(Position(player1.pos.row - 1, player1.pos.col - 1));
                    if not(player1.pos.row == 8 or Main.isHwall(player1.pos.row, player1.pos.col - 1)):
                        pm.append(Position(player1.pos.row + 1, player1.pos.col - 1));
                else:
                    pm.append(Position(player1.pos.row, player1.pos.col - 2));
            else:
                pm.append(Position(player1.pos.row, player1.pos.col - 1));
        
        def goRight():
            if player1.pos.col == 8 or Main.isVwall(player1.pos.row, player1.pos.col):
                return;
            if (player2.pos.row == player1.pos.row and player2.pos.col == player1.pos.col + 1) or (player3.pos.row == player1.pos.row and player3.pos.col == player1.pos.col + 1) or (player4.pos.row == player1.pos.row and player4.pos.col == player1.pos.col + 1):
                if player1.pos.col == 7 or Main.isVwall(player1.pos.row, player1.pos.col + 1) or (player2.pos.row == player1.pos.row and player2.pos.col == player1.pos.col + 2) or (player3.pos.row == player1.pos.row and player3.pos.col == player1.pos.col + 2) or (player4.pos.row == player1.pos.row and player4.pos.col == player1.pos.col + 2):
                    if not(player1.pos.row == 0 or Main.isHwall(player1.pos.row - 1, player1.pos.col + 1)):
                        pm.append(Position(player1.pos.row - 1, player1.pos.col + 1));
                    if not(player1.pos.row == 8 or Main.isHwall(player1.pos.row, player1.pos.col + 1)):
                        pm.append(Position(player1.pos.row + 1, player1.pos.col + 1));
                else:
                    pm.append(Position(player1.pos.row, player1.pos.col + 2));
            else:
                pm.append(Position(player1.pos.row, player1.pos.col + 1));
        
        goUp();
        goDown();
        goLeft();
        goRight();
        
        if player2.pos in pm:
            pm.remove(player2.pos);
        if player3.pos in pm:
            pm.remove(player3.pos);
        if player4.pos in pm:
            pm.remove(player4.pos);

        return pm;

    def isSurrounded(self, player1, player2, player3, player4, rdes, cdes):
        blocks = [];
        visited = [[False for x in range(9)] for y in range(9)];
        p = Player(player1.pos);    
        blocks.append(p.pos);
        while blocks:
            p.pos = blocks.pop();
            temp = self.possibleMoves(p, player2, player3, player4);
            for t in temp:
                if not visited[t.row][t.col]:
                    if t.row in rdes or t.col in cdes:
                        return False;
                    visited[t.row][t.col] = True;
                    blocks.append(t); 
        return True;    

    @staticmethod
    def addHwall(c1, c2, r1, r2, player1, player2, player3, player4):
        if Main.hwalls[r1][c1 - 1] or Main.hwalls[r1][c1] or Main.hwalls[r1][c2] or Main.vwalls[r1][c1]:
            return False;
        Main.hwalls[r1][c1] = True;
        if Main.isSurrounded(player1, player2, player3, player4, [8], [0, 8]) or Main.isSurrounded(player2, player1, player3, player4, [0, 8], [0]) or Main.isSurrounded(player3, player2, player1, player4, [0], [0, 8]) or Main.isSurrounded(player4, player2, player3, player1, [0, 8], [8]):
            Main.hwalls[r1][c1] = False;
            return False;
        return True;

    def addVwall(self, c1, c2, r1, r2, player1, player2, player3, player4):
        if self.vwalls[r1 - 1][c1] or self.vwalls[r1][c1] or self.vwalls[r2][c1] or self.hwalls[r1][c1]:
            return False;
        self.vwalls[r1][c1] = True;
        if Main.isSurrounded(player1, player2, player3, player4, [8], [0, 8]) or Main.isSurrounded(player2, player1, player3, player4, [0, 8], [0]) or Main.isSurrounded(player3, player2, player1, player4, [0], [0, 8]) or Main.isSurrounded(player4, player2, player3, player1, [0, 8], [8]):
            self.vwalls[r1][c1] = False;
            return False;
        return True;