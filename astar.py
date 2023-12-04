import heapq
from GeradorGrafo import GeradorGrafo
from FunctionObjetivo import Objetivo
import numpy as np
import time


class Astar:
    def __init__(self, board):
        self.G = GeradorGrafo(board=board)
        self.root = self.G.root
        self.bestSolution = self.G.bestSolution
        self.worstSolution = self.G.worstSolution
        self.strategy_decision = Objetivo.strategy_decision
        self.AccessCount = 0

    def heuristic(self,node, strategy):
        player_wins = 1/node.stepsPlayer if node.stepsPlayer != 0 else float('inf')
        opponent_wins = 1/node.stepsOpponent if node.stepsOpponent != 0 else float('inf')
        return player_wins - opponent_wins if strategy == 'vence' else opponent_wins - player_wins

    def a_star(self,initial_node, best_solution, worst_solution, strategy):
        print('astar', strategy)
        open_set = [(self.heuristic(initial_node, strategy), initial_node)]
        closed_set = set()
        objetivo = None

        while open_set:
            _, current_node = heapq.heappop(open_set)
            self.AccessCount += 1

            if ((strategy == 'vence' and current_node.stepsPlayer == best_solution) or (strategy == 'impede' and current_node.stepsOpponent == worst_solution)):
                objetivo = current_node
                break

            closed_set.add(map(tuple, current_node.board))

            for child in current_node.children:
                if map(tuple, child.board) not in closed_set:
                    heapq.heappush(open_set, (self.heuristic(child, strategy), child))

        return self.get_path(objetivo)

    def astar(self):
        time_inicio = time.time()
        strategy = Objetivo().strategy_decision(self.root)
        caminho = self.a_star(self.root, self.bestSolution, self.worstSolution, strategy)
        print('A* acessos: ', self.AccessCount)

        if len(caminho) > 1:
            origin = np.array(caminho[-2].board)
            moved = np.array(caminho[-1].board)
            posicao_diferenca = np.where(origin != moved)
            if len(posicao_diferenca[0]) > 0:
                pos = tuple(zip(posicao_diferenca[0], posicao_diferenca[1]))
                time_fim = time.time()
                print("Astar ", time_fim-time_inicio)
                return pos[0][1]
            else:
                return None
        else:
            for i in range(7):
                if caminho[0].board[0][i] == ' ':
                    return i

    def get_path(self,node):
        path = []
        while node is not None:
            path.insert(0, node)
            node = node.parent
        return path