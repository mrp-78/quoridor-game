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
    def possibleMoves(player1, player2):
        pm = [];
        
        def goUp():
            if player1.pos.row == 0 or Main.isHwall(player1.pos.row - 1, player1.pos.col):
                return;
            if player2.pos.row == player1.pos.row - 1 and player2.pos.col == player1.pos.col:
                if (player1.pos.row == 1 or Main.isHwall(player1.pos.row - 2, player1.pos.col)):
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
            if player2.pos.row == player1.pos.row + 1 and player2.pos.col == player1.pos.col:
                if (player1.pos.row == 7 or Main.isHwall(player1.pos.row + 1, player1.pos.col)):
                    if not(player1.pos.col == 0 or Main.isVwall(player1.pos.row + 1, player1.pos.col - 1)):
                        pm.append(Position(player1.pos.row + 1, player1.pos.col - 1));
                    if not(player1.pos.col == 8 or Main.isVwall(player1.pos.row + 1, player1.pos.col)):
                        pm.append(Position(player1.pos.row + 1, player1.pos.col + 1));
                else:
                    pm.append(Position(player1.pos.row + 2, player1.pos.col));
            else:
                pm.append(Position(player1.pos.row + 1, player1.pos.col));

        def goLeft():
            if player1.pos.col == 0 or Main.isVwall(player1.pos.row, player1.pos.col - 1):
                return;
            if player2.pos.row == player1.pos.row and player2.pos.col == player1.pos.col - 1:
                if (player1.pos.col == 1 or Main.isVwall(player1.pos.row, player1.pos.col - 2)):
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
            if player2.pos.row == player1.pos.row and player2.pos.col == player1.pos.col + 1:
                if (player1.pos.col == 7 or Main.isVwall(player1.pos.row, player1.pos.col + 1)):
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
        return pm;

    @staticmethod
    def isSurrounded(player2, player1, des):
        blocks = [];
        visited = [[False for x in range(9)] for y in range(9)];
        p = Player(player1.pos);    
        blocks.append(p.pos);
        while blocks:
            p.pos = blocks.pop();
            temp = Main.possibleMoves(p, player2);
            for t in temp:
                if not visited[t.row][t.col]:
                    if t.row == des:
                        return False;
                    visited[t.row][t.col] = True;
                    blocks.append(t); 
        return True;
        #TODO in khat paeen okeye ?
        # return isSurrounded(player1, player2, 0 if des == 8 else 8);

    @staticmethod
    def addHwall(c1, c2, r1, r2, player1, player2, des):
        if Main.hwalls[r1][c1 - 1] or Main.hwalls[r1][c1] or Main.hwalls[r1][c2] or Main.vwalls[r1][c1]:
            return False;
        Main.hwalls[r1][c1] = True;
        if Main.isSurrounded(player1, player2, des) or Main.isSurrounded(player2, player1, 0 if des == 8 else 8):
            Main.hwalls[r1][c1] = False;
            return False;
        return True;
    
    @staticmethod
    def addVwall(c1, c2, r1, r2, player1, player2, des):
        if Main.vwalls[r1 - 1][c1] or Main.vwalls[r1][c1] or Main.vwalls[r2][c1] or Main.hwalls[r1][c1]:
            return False;
        Main.vwalls[r1][c1] = True;
        if Main.isSurrounded(player1, player2, des) or Main.isSurrounded(player2, player1, 0 if des == 8 else 8):
            Main.vwalls[r1][c1] = False;
            return False;
        return True;
		