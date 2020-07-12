import random
import json

from AI2P import AI2P
from Logic2P import Logic2P
from Player import Player
from Position import Position


def createEarlyPopulation():
    print("generating early population ...")
    earlyPopulation = []
    for i in range(20):
        p = []
        for j in range(4):
            a = random.random()
            if a == 0:
                a = 1
            p.append(a)
        earlyPopulation.append(p)
    with open('population.txt', 'w') as file:
        json.dump(earlyPopulation, file)


def main():
    for i in range(1):
        print(50 * "-")
        print("Round", i + 1, " of evolution")
        winners = []
        with open('population.txt', 'r') as file:
            population = json.load(file)
        random.shuffle(population)
        j = 0
        while j < 20:
            print("finding winners of group", int(j/4+1), "...")
            for winner in finedWinners(population[j:j + 4]):
                winners.append(winner)
            j += 4
        winners = winners + childProduction(winners)
        print(winners)
        with open('population.txt', 'w') as file:
            json.dump(winners, file)


def finedWinners(population):
    scores = [0, 0, 0, 0]
    for i in range(4):
        for j in range(i+1, 4):
            logic = Logic2P()
            turn = 0
            player1 = Player(Position(0, 4))
            player2 = Player(Position(8, 4))
            players = [player1, player2]
            ai1 = AI2P(logic, 8, population[i])
            ai2 = AI2P(logic, 0, population[j])
            while True:
                if turn == 0:
                    action, row, col, tim = ai1.chooseAnAction(players[0], players[1])
                else:
                    action, row, col, tim = ai2.chooseAnAction(players[1], players[0])
                if action == "move":
                    players[turn].pos.row = row
                    players[turn].pos.col = col
                    if turn == 1 and row == 0:
                        winner = 1
                        break
                    elif turn == 0 and row == 8:
                        winner = 0
                        break
                elif action == "add Vwall":
                    if logic.addVwall(col, row, players[turn], players[0 if turn == 1 else 1], 8 if turn == 0 else 0):
                        players[turn].walls -= 1
                elif action == "add Hwall":
                    if logic.addHwall(col, row, players[turn], players[0 if turn == 1 else 1],
                                           8 if turn == 0 else 0):
                        players[turn].walls -= 1
            if winner == 0:
                scores[i] += 1
            else:
                scores[j] += 1

    # print score board
    print("\tplayer score")
    for i in range(4):
        print("\t", i+1, 4*" ", scores[i])
    return population[0], population[1]


def childProduction(winners):
    print("generating childes ...")
    random.shuffle(winners)
    childes = []
    numOfMutations = 0
    for i in range(0, len(winners), 2):
        break_point = random.choice([1, 2, 3])
        ch1 = []
        ch2 = []
        for j in range(break_point):
            ch1.append(winners[i][j])
            ch2.append(winners[i + 1][j])
        for j in range(break_point, 4):
            ch1.append(winners[i + 1][j])
            ch2.append(winners[i][j])
        if random.random() <= 0.1:
            numOfMutations += 1
            mutation = random.choice([0, 1, 2, 3])
            ch1[mutation] = random.random()
            if ch1[mutation] == 0:
                ch1[mutation] = 1
        if random.random() <= 0.1:
            numOfMutations += 1
            mutation = random.choice([0, 1, 2, 3])
            ch2[mutation] = random.random()
            if ch2[mutation] == 0:
                ch2[mutation] = 1
        childes.append(ch1)
        childes.append(ch2)
    print("\t", numOfMutations, "mutations")
    return childes


if __name__ == '__main__':
    createEarlyPopulation()
    main()
